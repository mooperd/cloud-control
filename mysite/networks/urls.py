from django.conf.urls import url
from views import Vpc, VpcDeploy, VpcCreate, VpcUpdate, VpcDelete, VpcView, IndexView, VpcFormView
from . import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
#    url(r'^vpc/(?P<pk>\d+)/?$', VpcView.as_view(), name='vpc-view'),
#    url(r'^vpc/add/?$', VpcCreate.as_view(), name='vpc-add'),

    url(r'^vpc/(?P<pk>\d+)/(?P<action>\w+)/?$', VpcView.as_view(), name='vpc-action'),

#    url(r'^vpc/undeploy/(?P<pk>\d+)/?$', VpcUndeploy.as_view(), name='vpc-undeploy'),
    url(r'^vpc/addall/?$',VpcFormView.as_view(), name='vpc-add-all'),
    url(r'^vpc/(?P<pk>[0-9]+)/?$', VpcUpdate.as_view(), name='vpc-update'),
    url(r'^vpc/(?P<pk>[0-9]+)/delete/?$', VpcDelete.as_view(), name='vpc-delete'),
]
