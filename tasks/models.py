from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    assignee = models.TextField(default='')

    start_time = models.DateField(auto_now_add=True, null=True)
    end_time = models.DateField(null=True)
    address = models.CharField(max_length=200, default='')

    # lat long delivery coordinates
    latitude = models.CharField(max_length=50, default='')
    longitude = models.CharField(max_length=50, default='')

    delay = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    request_id = models.IntegerField(default=0)
    accidental_delivery_duration = models.IntegerField(default=0)

    def __str__(self):
        """A string representation of the model."""
        return self.title
