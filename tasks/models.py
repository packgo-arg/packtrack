from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from utils.models import Package, Status, State, Client, Provider, Driver
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.html import format_html
import uuid


class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=10,
                                validators=[RegexValidator(regex='^[A-Z]{4}[0-9]{6}$',
                                                           message='Length has to be 10',
                                                           code='nomatch')],
                                default='AAAA000000')
    # required fields
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    request_id = models.CharField(max_length=50, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    delay = models.IntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)

    last_status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    last_provider = models.ForeignKey(Provider,
                                      on_delete=models.CASCADE,
                                      default='4fd1d932-f86a-456b-9f39-f9919ad22040')
    last_driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    last_location = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    last_description = models.CharField(max_length=150, null=True, blank=True)

    accidental_delivery_duration = models.PositiveIntegerField(null=True, blank=True)
    ord_price = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        """A string representation of the model."""
        return f"Cliente: {self.client} - ID: {self.id}"

    def status(self):
        status = self.last_status.id
        if 1 <= status <= 5:
            color = '#2a00fc'
        elif 6 <= status <= 7:
            color = '#fc0000'
        elif status == 8:
            color = '#00c407'
        return format_html(
            '<span style="color: {};"><strong>{}</strong></span>',
            color,
            self.last_status
        )

    def update_status_record(self):

        OrderStatus.objects.create(
            order=self,
            status=self.last_status,
            provider=self.last_provider,
            driver=self.last_driver,
            location=self.last_location,
            description=self.last_description
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_status_record()


class Origin(models.Model):

    order = models.OneToOneField(Order,
                                 related_name='origins',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_num = models.CharField(max_length=10)
    ap_unit = models.CharField(max_length=10, null=True, blank=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    pos_code = models.IntegerField(null=True, blank=True)
    geo_data = models.JSONField(null=True, blank=True)
    is_covered = models.BooleanField(default=False)

    def __int__(self):
        """A string representation of the model."""
        return None


class Destination(models.Model):

    order = models.OneToOneField(Order,
                                 related_name='destinations',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100)
    house_num = models.CharField(max_length=10)
    ap_unit = models.CharField(max_length=50, null=True, blank=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    pos_code = models.IntegerField(null=True, blank=True)
    geo_data = models.JSONField(null=True, blank=True)
    is_covered = models.BooleanField(default=False)

    def __int__(self):
        """A string representation of the model."""
        return None


class OrderPackage(models.Model):

    order = models.ForeignKey(Order, related_name='packages', on_delete=models.CASCADE)
    pack_type = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    height = models.PositiveIntegerField(default=0, verbose_name='Height in mm')
    width = models.PositiveIntegerField(default=0, verbose_name='Width in mm')
    length = models.PositiveIntegerField(default=0, verbose_name='Length in mm')
    volume = models.FloatField(default=0, validators=[MinValueValidator(0)])
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0,
                                           validators=[MaxValueValidator(99)])
    package_id = models.CharField(max_length=13,
                                  validators=[RegexValidator(regex='^.[A-Z]{4}[0-9]{6}-[0-9]{2}$',
                                                             message='Length has to be 13',
                                                             code='nomatch')],
                                  default='AAAA000000-00')

    def __int__(self):
        return self.id


class OrderStatus(models.Model):

    order = models.ForeignKey(Order, related_name='ord_status', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, default='4fd1d932-f86a-456b-9f39-f9919ad22040')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    st_update = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.id
