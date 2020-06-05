# from rest_framework import generics
from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
# from ŕest_framework.permissions import AllowAny
from .models import Order, OrderStatus
from utils.models import Client
from .serializers import OrderSerializer, ReturnSerializer, OrderStatusSerializer
# from .lib.pg_library import *
# from django.contrib.auth.models import User


class OrderList(APIView):
    """
    List all tasks, or create a new task
    """
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        ord_serializer = OrderSerializer(data=request.data)
        if ord_serializer.is_valid():
            if ord_serializer.validated_data['duration'] == '99':
                return Response({'Fail': 'Address data not valid. Please resend Address/Coordinates'}, status=status.HTTP_400_BAD_REQUEST)
            ord_serializer.save()
            ret_serializer = ReturnSerializer(Order.objects.get(pk=ord_serializer.data['id']))
            return Response(ret_serializer.data, status=status.HTTP_201_CREATED)
        print(ord_serializer.errors)
        return Response(ord_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
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


class StatusDetail(APIView):
    """
    Retrieve, update or delete an order.
    """
    def get_object(self, order):

        try:
            order_status = OrderStatus.objects.filter(order=order).last()
            return order_status
        except OrderStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format_=None):

        try:
            if Order.objects.get(pk=request.data['order']).client_id == Client.objects.get(client_code=request.data['client']).id:
                order_status = OrderStatus.objects.filter(order_id=request.data['order']).last()
                serializer = OrderStatusSerializer(order_status)
                return Response(serializer.data)
            else:
                return Response({"Fail": "Client ID does not match with Order"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Fail": "Order not found"}, status=status.HTTP_404_NOTFOUND)