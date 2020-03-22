from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import *

class Order(models.Model):

    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    request_id = models.IntegerField(null=True)
    client = models.ForeignKey(Client, to_field='client_code', on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, to_field='prov_code', on_delete=models.SET_NULL, null=True)

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

#    assignee = models.TextField(null=True)
    delay = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    accidental_delivery_duration = models.IntegerField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title

class Origin(models.Model):

    order = models.OneToOneField(Order, related_name='origins', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    pos_code = models.IntegerField(null=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id

class Destination(models.Model):

    order = models.OneToOneField(Order, related_name='destinations', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    pos_code = models.IntegerField(null=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id

class OrderPackage(models.Model):

    order = models.ForeignKey(Order, related_name='packages', on_delete=models.CASCADE)
    size = models.ForeignKey(Package, to_field='pkg_code', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])

    def __int__(self):
        return self.id