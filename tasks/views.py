from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Order, OrderStatus
from utils.models import Client
from .serializers import OrderSerializer, ReturnSerializer, OrderStatusSerializer, OrderPriceSerializer
import time
import unicodedata
import io


class OrderList(APIView):
    """
    List all tasks, or create a new task
    """
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        start_time = time.time()
        ord_serializer = OrderSerializer(data=request.data)
        if ord_serializer.is_valid():
            ord_serializer.save()
            ret_serializer = ReturnSerializer(Order.objects.get(pk=ord_serializer.data['id']))
            print('--- Tiempo de ejecucion TOTAL: {} segundos ---'.format((time.time() - start_time)))
            return Response(ret_serializer.data, status=status.HTTP_201_CREATED)
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
            return Response({"Fail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class PriceDetail(APIView):
    """
    Retrieve, update or delete an order.
    """
    def get_object(self, pk):

        try:
            order = Order.objects.get(pk=pk)
            return order
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format_=None):

        try:
            if Order.objects.get(pk=request.data['order']).client_id == Client.objects.get(client_code=request.data['client']).id:
                order = Order.objects.get(pk=request.data['order'])
                serializer = OrderPriceSerializer(order)
                return Response(serializer.data)
            else:
                return Response({"Fail": "Client ID does not match with Order"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Fail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class PriceCalculator(APIView):
    """
    Retrieve, update or delete an order.
    """

    def post(self, request, format=None):
        start_time = time.time()
        ord_serializer = OrderSerializer(data=request.data)
        if ord_serializer.is_valid():
            data = JSONParser().parse(io.BytesIO(JSONRenderer().render(ord_serializer.data)))
            ret_serializer = OrderPriceSerializer(data=data)
            ret_serializer.is_valid()
            print('--- Tiempo de ejecucion TOTAL: {} segundos ---'.format((time.time() - start_time)))
            return Response(ret_serializer.data, status=status.HTTP_200_OK)
        return Response(ord_serializer.errors, status=status.HTTP_400_BAD_REQUEST)