from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import OrderSerializer, ReturnSerializer
from .lib.pg_library import *
from datetime import datetime, timezone, timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class OrderList(APIView):
    """
    List all tasks, or create a new task.
    """
    def get (self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            st = calc_start_time(timezone.now())
            et, dur = calc_end_time(st, serializer.validated_data['origins']['pos_code'], serializer.validated_data['destinations']['pos_code'])
            serializer.save(start_time=st, end_time=et, duration=dur)
            retord = Order.objects.get(pk=serializer.data['id'])
            retser = ReturnSerializer(retord)
            return Response(retser.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  OrderDetail(APIView):
    """
    Retrieve, update or delete an order.
    """
    def get_object(self, pk):

        try:
            order = Order.objects.get(pk=pk)
            return order
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format_=None):

        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):

        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):

        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)