from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'assignee',
            'created_at',
            'start_time',
            'end_time',
            'address',
            'latitude',
            'longitude',
            'delay',
            'duration',
            'request_id',
            'accidental_delivery_duration'
        )
        model = Task
