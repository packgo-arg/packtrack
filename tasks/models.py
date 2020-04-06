from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import *

class Order(models.Model):

    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    request_id = models.IntegerField(null=True)
    client = models.ForeignKey(Client, to_field='client_code', on_delete=models.CASCADE, default='NA')


    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

#    assignee = models.TextField(null=True)
    delay = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=8, null=True, blank=True)
    accidental_delivery_duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title

class Origin(models.Model):

    order = models.OneToOneField(Order, related_name='origins', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    street = models.CharField(max_length=100, null=True)
    house_num = models.IntegerField(null=True)
    ap_unit = models.CharField(max_length=50, null=True, blank=True)
    suburb = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    pos_code = models.IntegerField(null=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id

class Destination(models.Model):

    order = models.OneToOneField(Order, related_name='destinations', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    street = models.CharField(max_length=100, null=True)
    house_num = models.IntegerField(null=True)
    ap_unit = models.CharField(max_length=50, null=True, blank=True)
    suburb = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    pos_code = models.IntegerField(null=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id

class OrderPackage(models.Model):

    order = models.ForeignKey(Order, related_name='packages', on_delete=models.CASCADE)
    pak_type = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])

    def __int__(self):
        return self.id

class OrderStatus(models.Model):

    order = models.ForeignKey(Order, related_name='ord_status', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=2)
    provider = models.ForeignKey(Provider, to_field='prov_code', on_delete=models.CASCADE, default='PG')
    location = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    st_update = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.id