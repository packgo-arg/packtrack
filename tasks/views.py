from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Order, OrderStatus
from utils.models import Client
from .serializers import OrderSerializer, ReturnSerializer, OrderStatusSerializer, OrderPriceSerializer
import time
import io


class OrderList(APIView):
    """
    List all tasks, or create a new task
    """
    def get(self, request, format=None):
       
        client_id = Client.objects.get(username=self.request.user).id
        orders = Order.objects.filter(client=client_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        start_time = time.time()
        ord_serializer = OrderSerializer(data=request.data, context={'request': request})
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
        client_id = Client.objects.get(username=self.request.user).id
        try:
            order = Order.objects.get(pk=pk, client=client_id)
            return order
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format_=None):
        client_id = Client.objects.get(username=self.request.user).id
        try:
            order = Order.objects.get(pk=pk, client=client_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        client_id = Client.objects.get(username=self.request.user).id
        try:
            order = Order.objects.get(pk=pk, client=client_id)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        client_id = Client.objects.get(username=self.request.user).id
        try:
            order = Order.objects.get(pk=pk, client=client_id)
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
            Order.objects.get(pk=request.data['order'], client=Client.objects.get(username=self.request.user).id)
            order_status = OrderStatus.objects.filter(order_id=request.data['order']).last()
            serializer = OrderStatusSerializer(order_status)
            return Response(serializer.data)
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
            Order.objects.get(pk=request.data['order'], client=Client.objects.get(username=self.request.user).id)
            order = Order.objects.get(pk=request.data['order'])
            serializer = OrderPriceSerializer(order)
            return Response(serializer.data)
        except:
            return Response({"Fail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class PriceCalculator(APIView):
    """
    Retrieve, update or delete an order.
    """

    def post(self, request, format=None):
        start_time = time.time()
        ord_serializer = OrderSerializer(data=request.data, context={'request': request})
        if ord_serializer.is_valid():
            data = JSONParser().parse(io.BytesIO(JSONRenderer().render(ord_serializer.data)))
            ret_serializer = OrderPriceSerializer(data=data, context={'request': request})
            ret_serializer.is_valid()
            print('--- Tiempo de ejecucion TOTAL: {} segundos ---'.format((time.time() - start_time)))
            return Response(ret_serializer.data, status=status.HTTP_200_OK)
        return Response(ord_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
