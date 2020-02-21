from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Providers(models.Model):
    # required fields
    prov_id = models.AutoField(primary_key=True)
    prov_name = models.CharField(max_length=200)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        """A string representation of the model."""
        return self.id


class Clients(models.Model):
    # required fields
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=200)
    city_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        """A string representation of the model."""
        return self.id