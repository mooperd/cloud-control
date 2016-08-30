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

    # Test if the aws_id exists in the database.
    # If exists it might be a good idea to make a call to the provider to see if the entity really exists there
    # but the AWS api is so darn slow. Impliment queue? Maybe should be using @properties here?
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
                    kwargs['vpc_id'], # Is there a more elegant way to pass the subnet the VPC-ID?
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
    amazon_aws = AWSProvider()
    name = models.CharField(max_length=30, verbose_name='Instance Name')
    type = models.CharField(max_length=30, verbose_name='Instance Type')
    # the ID is only used for deployed instances
    aws_id = models.CharField(max_length=30, default="")
    subnet = models.ForeignKey(Subnet)

    def is_active(self):
        return self.aws_id != ""

    def deploy(self, **kwargs):
        if self.is_active() == True:
            return True
        if self.is_active() == False:
            try:
                self.aws_id = self.amazon_aws.create_instance(
                    kwargs['subnet_id'], # Is there a more elegant way to pass the subnet ID?
                    self.name,
                    # self.availability_zone,
                )
                self.save()
            except:
                raise
    """
    The AWS boto function "terminate_instances() seems to be intended to terminate multiple instances at once.
    For the sake of a more simplistic application design we shall only call it with a singular instance however this
    will have an effect on the performance. A call per termination will be required rather than
    'one call to terminate them all'
    """
    def undeploy(self):
        if self.is_active() == True:
            try:
                self.amazon_aws.delete_instance(
                    self.aws_id
                )
                self.aws_id = ""
                self.save()
            except:
                raise
        if self.is_active() == False:
            return False


# FIN