# from django.shortcuts import render
#
# # Create your views here.
# from rest_framework import generics
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
#
# from .models import *
# from django.contrib.auth.models import User
#
# class ClientList(APIView):
#     """
#     List all tasks, or create a new task.
#     """
#     def get (self, request, format=None):
#         client = Client.objects.all()
#         serializer = ClientSerializer(client, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ClientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class  ClientDetail(APIView):
#     """
#     Retrieve, update or delete an order.
#     """
#     def get_object(self, pk):
#
#         try:
#             client = Client.objects.get(pk=pk)
#             return client
#         except Client.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format_=None):
#
#         try:
#             client = Client.objects.get(pk=pk)
#             serializer = ClientSerializer(client)
#             return Response(serializer.data)
#         except Client.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk, format=None):
#
#         try:
#             client = Client.objects.get(pk=pk)
#             serializer = ClientSerializer(client, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Client.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, pk, format=None):
#
#         try:
#             client = Client.objects.get(pk=pk)
#             client.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Client.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
# class ProviderList(APIView):
#     """
#     List all tasks, or create a new task.
#     """
#     def get (self, request, format=None):
#         provider = Provider.objects.all()
#         serializer = ClientSerializer(provider, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ProviderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class  ProviderDetail(APIView):
#     """
#     Retrieve, update or delete an order.
#     """
#     def get_object(self, pk):
#
#         try:
#             provider = Provider.objects.get(pk=pk)
#             return provider
#         except Provider.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format_=None):
#
#         try:
#             provider = Provider.objects.get(pk=pk)
#             serializer = ProviderSerializer(provider)
#             return Response(serializer.data)
#         except Provider.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk, format=None):
#
#         try:
#             provider = Provider.objects.get(pk=pk)
#             serializer = ProviderSerializer(provider, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Provider.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, pk, format=None):
#
#         try:
#             provider = Provider.objects.get(pk=pk)
#             provider.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Provider.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)