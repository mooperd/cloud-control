"""
An Instance (virtual machine) is a child of a Subnet which is a child of VPC (virtual private cloud)
"""

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from ext.amazon_aws import AWSProvider
from ext import log

class Vpc(models.Model):
    # It might be better to pass in AWSProvider when calling this function to support more than one cloud provider.
    amazon_aws = AWSProvider()
    name = models.CharField(max_length=30, verbose_name='Vpc Name')
    cidr = models.CharField(max_length=30, verbose_name='Vpc CIDR')
    region = models.CharField(max_length=30, default="")
    aws_id = models.CharField(max_length=30, default="")

    def get_absolute_url(self):
        return reverse('vpc-detail', kwargs={'pk': self.pk})

    # Check if the vpc is deployed.
    def is_active(self):
        return self.aws_id != ""

    def deploy(self):
        if self.is_active() == True:
            return True
        if self.is_active() == False:
            try:
                self.aws_id = self.amazon_aws.create_vpc(
                    self.name,
                    self.region,
                    self.cidr
                )
                self.save()
            except:
                raise

    def undeploy(self):
        if self.is_active() == True:
            try:
                self.amazon_aws.delete_vpc(
                    self.aws_id
                )
                self.aws_id = ""
                self.save()
            except:
                raise
        if self.is_active() == False:
            return False

# def __str__(self):              # __unicode__ on Python 2
#        return "%s %s" % (self.first_name, self.last_name)

class Subnet(models.Model):
    amazon_aws = AWSProvider()
    name = models.CharField(max_length=30, verbose_name='Subnet Name')
    cidr = models.CharField(max_length=30, verbose_name='Subnet CIDR')
    availability_zone = models.CharField(max_length=30, default="")
    aws_id = models.CharField(max_length=30, default="")
    vpc = models.ForeignKey(Vpc)

    # Test if the aws_id exists in the database.
    # If exists it might be a good idea to make a call to the provider to see if the entity really exists there
    # but the AWS api is so darn slow. Impliment queue?
    # Maybe Should be using @properties here
    def is_active(self):
        return self.aws_id != ""

    def deploy(self, **kwargs):
        if self.is_active() == True:
            return True
        if self.is_active() == False:
            try:
                self.aws_id = self.amazon_aws.create_subnet(
                    # kwargs['vpc_id'], # Is there a more elegant way to pass the subnet the VPC-ID?
                    self.name,
                    self.cidr,
                    # self.availability_zone,
                )
                self.save()
            except:
                raise

    def undeploy(self):
        if self.is_active() == True:
            try:
                self.amazon_aws.delete_subnet(
                    self.aws_id
                )
                self.aws_id = ""
                self.save()
            except:
                raise
        if self.is_active() == False:
            return False

    def get_absolute_url(self):
        return reverse('subnet-detail', kwargs={'pk': self.pk})


# def __str__(self):              # __unicode__ on Python 2
#        return "%s %s" % (self.name, self.cidr)

class Instance(models.Model):
    name = models.CharField(max_length=30, verbose_name='Instance Name')
    type = models.CharField(max_length=30, verbose_name='Instance Type')
    # the ID is only used for deployed instances
    aws_id = models.CharField(max_length=30, default="")
    subnet = models.ForeignKey(Subnet)

    def get_absolute_url(self):
        return reverse('instance-detail', kwargs={'pk': self.pk})

    class Deploy(models.Model):
        """
        In this class we will put together the data structure into a single data object so that we can run deploy and undeploy
        operations on it. This datastructure should be "cloud provider agnostic" and should be able to be used to deploy
        infrastructure to any cloud provider with an appropriate feature set.

        Currently this is far too AWS centric for my liking but we should be able to work this out later without
        too much pain.

        An Instance (virtual machine) is a child of a Subnet which is a child of VPC (virtual private cloud)

        """
        # Build the data object
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

        infrastructure = {
            'name': vpc_instance.name,
            'cidr': vpc_instance.cidr,
            'Subnets': subnets.values(),
            'object': vpc_instance,
        }

        # Not sure this is the most efficient way of referancing the objects that should be created but it works :)
        def deploy(self):
            self.infrastructure["object"].deploy()
            for subnet in infrastructure["Subnets"]:
                subnet["object"].deploy(vpc_id=vpc_data["object"].aws_id)

        # We dont need to pass anything to the undeploy as it will know its own aws_id.
        def undeploy(self):
            self.infrastructure["object"].undeploy()
            for subnet in infrastructure["Subnets"]:
                subnet["object"].undeploy()

