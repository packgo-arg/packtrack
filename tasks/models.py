from django.db import models

class Order(models.Model):

    CHOICES = (
        ('PP', 'Popack'),
    )
    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    request_id = models.IntegerField(null=True)
    client_id = models.CharField(max_length=2, choices=CHOICES)
    prov_id = models.IntegerField(null=True)

    # internal
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    assignee = models.TextField(null=True)
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