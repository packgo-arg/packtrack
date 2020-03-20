from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Order(models.Model):

    CL_LIST = (
        ('PP', 'Popack'),
        ('DP', 'DeliPack'),
        ('GF', 'GoFriz')
    )

    CL_LIST = (
        ('PP', 'Popack'),
        ('DP', 'DeliPack'),
        ('GF', 'GoFriz')
    )

    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    request_id = models.IntegerField(null=True)
    client_id = models.CharField(max_length=2, choices=CL_LIST)
    prov_id = models.CharField(max_length=2, choices=PV_LIST)

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

#    assignee = models.TextField(null=True)
    delay = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    accidental_delivery_duration = models.IntegerField(null=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id

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

class Package(models.Model):

    PK_SIZE = (
        ('01', 'Sobre'),
        ('02', 'Caja pequeña'),
        ('03', 'Caja mediana'),
        ('04', 'Caja grande'),
        ('05', 'Pallet')
    )

    order = models.OneToOneField(Order, related_name='packages',on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=PK_SIZE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])

    def __int__(self):
        return self.id