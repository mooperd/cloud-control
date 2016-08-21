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

from models import Vpc

"""
def index(request):
    #conn = boto.connect_vpc()
    #vpc_list = conn.get_all_vpcs()
    vpc_list = Vpc.objects.all()
    return TemplateResponse(request, 'networks/index.html', {'vpc_list': vpc_list})
"""

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
