from rest_framework import serializers
from django.utils import timezone
from .models import Order, Origin, Destination, OrderStatus, OrderPackage
from utils.models import Status, State, Client, Package
from .lib.pg_library import calcDeliveryTime, normalizeWord, getCoord, jsonForApi, calcPrice
import requests
import os
import datetime as dt


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'request_id',
            'start_time',
            'end_time',
            'duration'
        )


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):

    location = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatus
        fields = (
            'order',
            'status',
            'location',
            'description',
            'st_update'
        )

    def get_location(self, obj):
        try:
            location_inst = State.objects.get(pk=obj.location_id)
            return location_inst.state_name
        except Status.DoesNotExist:
            return print('ERROR LOCATION')


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = (
            'name',
            'street',
            'house_num',
            'ap_unit',
            'suburb',
            'city',
            'province',
            'country',
            'latitude',
            'longitude',
            'pos_code'
        )

    def to_internal_value(self, value):

        try:
            value['city'] = requests.post(f'{os.getenv("API_BASE_URL")}localidades-censales', json=jsonForApi(value['city'], value['province'], 'localidades_censales')).json().get('resultados', None)[0].get('localidades_censales', None)[0].get('nombre', None)
        except IndexError:
            raise serializers.ValidationError('Localidad no se pudo validar')

        if not value['latitude'] or not value['longitude']:
            value, msj = getCoord(value)
            if msj: raise serializers.ValidationError(msj)

        return super().to_internal_value(value)

    def validate_city(self, value):
        try:
            State.objects.get(city__unaccent__iexact=normalizeWord(value))
            return value
        except:
            raise serializers.ValidationError('Origin City Not found')


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = (
            'name',
            'street',
            'house_num',
            'ap_unit',
            'suburb',
            'city',
            'province',
            'country',
            'latitude',
            'longitude',
            'pos_code'
        )

    def to_internal_value(self, value):

        try:
            value['city'] = requests.post(f'{os.getenv("API_BASE_URL")}localidades-censales', json=jsonForApi(value['city'], value['province'], 'localidades_censales')).json().get('resultados', None)[0].get('localidades_censales', None)[0].get('nombre', None)
        except IndexError:
            raise serializers.ValidationError('Localidad no se pudo validar')

        if not value['latitude'] or not value['longitude']:
            value, msj = getCoord(value)
            print(msj)
            if msj: raise serializers.ValidationError(msj)

        return super().to_internal_value(value)

    def validate_city(self, value):
        try:
            State.objects.get(city__unaccent__iexact=normalizeWord(value))
            return value
        except:
            raise serializers.ValidationError('Destination City Not found')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPackage
        fields = (
            'pak_type',
            'quantity',
            'ord_pak_price'
        )


class OrderSerializer(serializers.ModelSerializer):
    origins = OriginSerializer()
    destinations = DestinationSerializer()
    packages = PackageSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'client',
            'request_id',
            'title',
            'description',
            'created_at',
            'start_time',
            'end_time',
            'delay',
            'duration',
            'accidental_delivery_duration',
            'ord_price',
            'origins',
            'destinations',
            'packages'
        )

    def to_internal_value(self, value):

        client_inst = Client.objects.get(client_code=value['client'])

        value['client'] = client_inst.id

        return super().to_internal_value(value)

    def validate(self, value):

        try:
            value['duration'], distance = calcDeliveryTime(value['origins'], value['destinations'])
        except:
            value['duration'] = 99
            print('Valor de Duration :', value['duration'])
            raise serializers.ValidationError('COULD NOT PARSE COORDINATES')
        if timezone.localtime().time() < dt.time(15):
            value['start_time'] = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
        else:
            value['start_time'] = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)

        value['end_time'] = value['start_time'] + dt.timedelta(hours=int(value['duration']))

        value['ord_price'] = 0
        disc = Client.objects.get(client_name=value['client']).price_disc
        for pack in value['packages']:
            pk_info = Package.objects.get(pkg_name=pack['pak_type'])
            pack['ord_pak_price'] = calcPrice(distance, disc, pack, pk_info)
            value['ord_price'] += pack['ord_pak_price']

        return value

    def create(self, validated_data):
        origin_data = validated_data.pop('origins')
        dest_data = validated_data.pop('destinations')
        pkg_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        Origin.objects.create(order=order, **origin_data)
        Destination.objects.create(order=order, **dest_data)
        OrderStatus.objects.create(order=order, location=State.objects.get(city__unaccent__iexact=normalizeWord(origin_data['city'])))
        for pkg in pkg_data:
            OrderPackage.objects.create(order=order, **pkg)
        return order
