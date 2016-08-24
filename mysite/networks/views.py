import boto
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import InstanceForm, SubnetForm, VpcForm
from django.db.models import Prefetch
from models import Vpc, Subnet, Instance
from pprint import pprint

class IndexView(ListView):
    model = Vpc
    template_name = "networks/index.html"

class VpcDeploy(View):
    model = Vpc

    def get(self, request, *args, **kwargs):
        deploy = get_object_or_404(self.model, id=kwargs['pk'])
        deploy.deploy()
        return redirect("/networks")

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
                    'Instances': [],
                }
            subnets[instance.subnet_id]['Instances'].append({
                'name': instance.name,
                'type': instance.type,
            })

        vpc_data = {
                'name': vpc_instance.name,
                'cidr': vpc_instance.cidr,
                'Subnets': subnets.values(),
            }

        # http://makina-corpus.com/blog/metier/2015/how-to-improve-prefetch_related-performance-with-the-prefetch-object
        # https://timmyomahony.com/blog/misconceptions-select_related-in-django/
        #subnet_vpc = Subnet.objects.prefetch_related(Prefetch('vpc', queryset=Vpc.objects.filter(id=kwargs['pk']))).all()
        #subnet_vpc.filter(id=4)
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
