from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import *

class Order(models.Model):

    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    request_id = models.IntegerField(null=True)
    client = models.ForeignKey(Client, to_field='client_code', on_delete=models.CASCADE, default='NA')
    provider = models.ForeignKey(Provider, to_field='prov_code', on_delete=models.SET_DEFAULT, default='PG')

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

#    assignee = models.TextField(null=True)
    delay = models.IntegerField(null=True)
    duration = models.CharField(max_length=8, null=True)
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

class OrderStatus(models.Model):
    STATUS_CH = [
        ('01', 'En Proceso'),
        ('02', 'En Colecta'),
        ('03', 'En Centro de distribucion'),
        ('04', 'En Transito'),
        ('05', 'En Entrega'),
        ('06', 'Demorado'),
        ('07', 'Cancelado'),
        ('08', 'Entregado'),
        ]
    order = models.ForeignKey(Order, related_name='ord_status', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CH)
    provider = models.ForeignKey(Provider, to_field='prov_code', on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=150, null=True)
    st_update = models.DateTimeField(auto_now_add=True)