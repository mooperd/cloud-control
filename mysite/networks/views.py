from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from .forms import InstanceForm, SubnetForm, VpcForm
from models import Vpc, Subnet, Instance

class IndexView(ListView):
    model = Vpc
    template_name = "networks/index.html"

class VpcDeploy(View):
    model = Vpc


    # def get(self, request, *args, **kwargs):
    #     deploy = get_object_or_404(self.model, id=kwargs['pk'])
    #     deploy.deploy()
    #     return redirect("/networks")

class VpcUndeploy(View):
    model = Vpc

    def get(self, request, *args, **kwargs):
        undeploy = get_object_or_404(self.model, id=kwargs['pk'])
        undeploy.undeploy()
        return redirect("/networks")

class VpcView(DetailView):
    model = Vpc
    template_name = "networks/vpc.html"

    def get(self, request, *args, **kwargs):
        subnets = {}

        vpc_instance = Vpc.objects.prefetch_related('subnet_set').get(pk=self.kwargs['pk'])

        for instance in Instance.objects.filter(subnet__vpc=vpc_instance).select_related('subnet'):
            if instance.subnet_id not in subnets:
                subnets[instance.subnet_id] = {
                    'cidr': instance.subnet.cidr,
                    'name': instance.subnet.name,
                    'zone': instance.subnet.availability_zone,
                    'object': instance.subnet,
                    'Instances': [],
                }
            subnets[instance.subnet_id]['Instances'].append({
                'name': instance.name,
                'type': instance.type,
                'object': instance,
            })

        vpc_data = {
                'name': vpc_instance.name,
                'cidr': vpc_instance.cidr,
                'Subnets': subnets.values(),
                'object': vpc_instance,
            }

        # deploy stuff. this should probably be a seperate function in a new sexy "deploy" class.
        # deploying the VPC object is simple enough but we have to tell the Subnet.deploy() the vpc ID
        # and the Instance.deploy the subnet ID. These ID's are picked up by kwargs on the model.
        # Are kwargs lazy? Is this spaghetti?
        vpc_data["object"].deploy()
        for subnet in  vpc_data["Subnets"]:
            subnet["object"].deploy(vpc_id=vpc_data["object"].aws_id)

        # http://makina-corpus.com/blog/metier/2015/how-to-improve-prefetch_related-performance-with-the-prefetch-object
        # https://timmyomahony.com/blog/misconceptions-select_related-in-django/
        # subnet_vpc = Subnet.objects.prefetch_related(Prefetch('vpc', queryset=Vpc.objects.filter(id=kwargs['pk']))).all()
        # subnet_vpc.filter(id=4)
        # Maybe prefetch_related will be needed here some day.
        # subnet_vpc = Vpc.objects.prefetch_related('subnet_set').get(pk=self.kwargs['pk'])
        # pprint(subnet_vpc)
        return TemplateResponse( request, 'networks/vpc.html', {'subnets': subnets, 'vpc_data': vpc_data})

class VpcCreate(CreateView):
    model = Vpc
    fields = ['name', 'cidr']

class VpcUpdate(UpdateView):
    model = Vpc
    fields = ['name', 'cidr']

class VpcDelete(DeleteView):
    model = Vpc
    success_url = reverse_lazy('vpc-list')

class VpcFormView(View):
    template_name = "networks/vpc_form.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        context['formA'] = VpcForm()
        context['formB'] = SubnetForm()
        context['formC'] = InstanceForm()
        return TemplateResponse(request, template=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        vpc = VpcForm(request.POST)
        subnet = SubnetForm(request.POST)
        instance = InstanceForm(request.POST)
        if vpc.is_valid() and subnet.is_valid() and instance.is_valid():
            vpc = vpc.save()
            subnet.instance.vpc = vpc
            subnet = subnet.save()
            instance.instance.subnet = subnet
            instance.save()
            return redirect("/networks")


        return TemplateResponse(request, template=self.template_name,
                                context={'formA': vpc, 'formB': subnet, 'formC': instance})


class VpcView(View):
    """
    In this class we will put together the data structure into a single data object so that we can run deploy and undeploy
    operations on it. This datastructure should be "cloud provider agnostic" and should be able to be used to deploy
    infrastructure to any cloud provider with an appropriate feature set.

    Currently this is far too AWS centric for my liking but we should be able to work this out later without
    too much pain.

    An Instance (virtual machine) is a child of a Subnet which is a child of VPC (virtual private cloud)

    """

    # model = Vpc

    """
    This function is nessasary to reinitialise the infrastructure datastructure once something has happened to it.
    """
    def build_infrastructure(self):
        subnets = {}

        # Get the main Vpc instance and its subnet. Prefetch_related is supposedly not nessasary
        vpc_instance = Vpc.objects.prefetch_related('subnet_set').get()

        # Build the rest of the data structure by iterating through the various entities
        # Subnets without instances are not selected which is probably a bug.
        for instance in Instance.objects.filter(subnet__vpc=vpc_instance).select_related('subnet'):
            if instance.subnet_id not in subnets:
                subnets[instance.subnet_id] = {
                    'id': instance.subnet.pk,
                    'cidr': instance.subnet.cidr,
                    'name': instance.subnet.name,
                    'zone': instance.subnet.availability_zone,
                    'aws_id': instance.subnet.aws_id,
                    'object': instance.subnet,
                    'Instances': [],
                }
            subnets[instance.subnet_id]['Instances'].append({
                'name': instance.name,
                'type': instance.type,
                'aws_id': instance.aws_id,
                'object': instance,
            })

        # add on the attributes of the VPC.
        infrastructure = {
            'name': vpc_instance.name,
            'cidr': vpc_instance.cidr,
            'aws_id': vpc_instance.aws_id,
            'Subnets': subnets.values(),
            'object': vpc_instance,
        }

        return infrastructure

    """
    This function receives the request and routes it to the appropriate function depending on the URL
    """
    def post(self, request, **kwargs):
        template_name = "networks/vpc.html"
        if self.kwargs['action']=='deploy':
            self.deploy()
        elif self.kwargs['action']=='undeploy':
            self.undeploy()
        else:
            error = "%s is not a valid action" % self.kwargs['action']
            raise ValueError(error)

        # pick up the changes in the model before returning the call.
        infrastructure = self.build_infrastructure()
        return TemplateResponse(request, 'networks/vpc.html', {'vpc_data': infrastructure})

    def get(self, request, **kwargs):
        template_name = "networks/vpc.html"
        if self.kwargs['action']=='view':
            # pick up the changes in the model before returning the call.
            infrastructure = self.build_infrastructure()
            return TemplateResponse(request, 'networks/vpc.html', {'vpc_data': infrastructure})
        else:
            error = "%s is not a valid action" % self.kwargs['action']
            raise ValueError(error)

    # Not sure this is the most efficient way of referencing the objects that should be created but it works :)
    def deploy(self):
        infrastructure = self.build_infrastructure()
        infrastructure["object"].deploy()
        for subnet in infrastructure["Subnets"]:
            subnet["object"].deploy(vpc_id=infrastructure["object"].aws_id)
            for instance in subnet["Instances"]:
                instance["object"].deploy(subnet_id=subnet["object"].aws_id)

    # We dont need to pass anything to the undeploy as it will know its own aws_id.
    # undeploy should do things in the opposit order as deploy.
    def undeploy(self):
        infrastructure = self.build_infrastructure()
        for subnet in infrastructure["Subnets"]:
            for instance in subnet["Instances"]:
                instance["object"].undeploy()
            subnet["object"].undeploy()
        infrastructure["object"].undeploy()
