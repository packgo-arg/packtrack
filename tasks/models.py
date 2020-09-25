from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import Package, Status, State, Client, Provider, Driver


class Order(models.Model):

    # required fields
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    request_id = models.CharField(max_length=50, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    delay = models.IntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    accidental_delivery_duration = models.PositiveIntegerField(null=True, blank=True)
    ord_price = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        """A string representation of the model."""
        return self.title


class Origin(models.Model):

    order = models.OneToOneField(Order, related_name='origins', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50, null=True, blank=True)
    house_num = models.IntegerField(null=True, blank=True)
    ap_unit = models.CharField(max_length=50, null=True, blank=True)
    suburb = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    pos_code = models.IntegerField(null=True, blank=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id


class Destination(models.Model):

    order = models.OneToOneField(Order, related_name='destinations', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50, null=True, blank=True)
    house_num = models.IntegerField(null=True, blank=True)
    ap_unit = models.CharField(max_length=50, null=True, blank=True)
    suburb = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    pos_code = models.IntegerField(null=True, blank=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id


class OrderPackage(models.Model):

    order = models.ForeignKey(Order, related_name='packages', on_delete=models.CASCADE)
    pack_type = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    height = models.FloatField(default=0, validators=[MinValueValidator(0)])
    width = models.FloatField(default=0, validators=[MinValueValidator(0)])
    length = models.FloatField(default=0, validators=[MinValueValidator(0)])
    volume = models.FloatField(default=0, validators=[MinValueValidator(0)])
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])
    pack_price = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __int__(self):
        return self.id


class OrderStatus(models.Model):

    order = models.ForeignKey(Order, related_name='ord_status', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, default=1)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    st_update = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.id
