from django.db import models

class Task(models.Model):
    # required fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    request_id = models.IntegerField()

    address = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    # internal
    created_at = models.DateField(auto_now_add=True)
    start_time = models.DateField(null=True)
    end_time = models.DateField(null=True)

    assignee = models.TextField(null=True)
    delay = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    accidental_delivery_duration = models.IntegerField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title
