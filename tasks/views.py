from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import TaskSerializer
from .lib.pg_library import *
from datetime import datetime, timezone, timedelta
from django.utils import timezone


class TaskList(APIView):
    """
    List all tasks, or create a new task.
    """
    def get (self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        st = calc_start_time(timezone.now())
        if serializer.is_valid():
            serializer.save(start_time=st)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  TaskDetail(APIView):
    """
    Retrieve, update or delete a task.
    """
    def get_object(self, pk):

        try:
            task = Task.objects.get(pk=pk)
            return task
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format_=None):

        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):

        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):

        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)