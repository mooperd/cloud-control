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

    model = Vpc
    subnets = {}
    # Build the data object
    vpc_instance = Vpc.objects.prefetch_related('subnet_set').get()

    for instance in Instance.objects.filter(subnet__vpc=vpc_instance).select_related('subnet'):
        if instance.subnet_id not in subnets:
            subnets[instance.subnet_id] = {
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

    infrastructure = {
        'name': vpc_instance.name,
        'cidr': vpc_instance.cidr,
        'aws_id': vpc_instance.aws_id,
        'Subnets': subnets.values(),
        'object': vpc_instance,
    }

    # once we have performed some action we need to reinitialise the class to fetch the new values from the database.
    # def reset(self, ??):
    #     ????


    # Find out what action was called in the URL.
    def get(self, request, **kwargs):
        template_name = "networks/vpc.html"
        if self.kwargs['action']=='deploy':
            self.deploy()
        elif self.kwargs['action']=='undeploy':
            self.undeploy()
        else:
            error = "%s is not a valid action" % self.kwargs['action']
            raise ValueError(error)

        return TemplateResponse(request, 'networks/vpc.html', {'subnets': self.subnets, 'vpc_data': self.infrastructure})

    # Not sure this is the most efficient way of referancing the objects that should be created but it works :)
    def deploy(self):
        self.infrastructure["object"].deploy()
        for subnet in self.infrastructure["Subnets"]:
            subnet["object"].deploy(vpc_id=self.infrastructure["object"].aws_id)

    # We dont need to pass anything to the undeploy as it will know its own aws_id.
    # undeploy should do things in the opposit order as deploy.
    def undeploy(self):
        for subnet in self.infrastructure["Subnets"]:
            subnet["object"].undeploy()
        self.infrastructure["object"].undeploy()
