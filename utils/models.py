from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Provider(models.Model):
    # required fields
    prov_name = models.CharField(max_length=200)
    prov_code = models.CharField(max_length=2)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id


class Client(models.Model):
    # required fields
    client_name = models.CharField(max_length=200)
    client_code = models.CharField(max_length=2)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        """A string representation of the model."""
        return self.id