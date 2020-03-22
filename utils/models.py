from django.db import models
from django.contrib.auth.models import User
#from tasks.models import *

# Create your models here.
class Provider(models.Model):
    # required fields
    prov_name = models.CharField(max_length=200)
    prov_code = models.CharField(max_length=2, unique=True)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """A string representation of the model."""
        return self.prov_name


class Client(models.Model):
    # required fields
    client_name = models.CharField(max_length=100)
    client_code = models.CharField(max_length=2, unique=True)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """A string representation of the model."""
        return self.client_name

class Package(models.Model):
    pkg_name = models.CharField(max_length=100)
    pkg_code = models.CharField(max_length=2, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #size = models.CharField(max_length=2, choices=PK_SIZE)
    def __str__(self):
        return self.pkg_name