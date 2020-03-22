from rest_framework import serializers
from .models import *
from utils.models import *


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


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = (
            'name',
            'address',
            'city',
            'latitude',
            'longitude',
            'pos_code'
        )


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = (
            'name',
            'address',
            'city',
            'latitude',
            'longitude',
            'pos_code'
        )


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPackage
        fields = (
            'size',
            'quantity'
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
            'provider',
            'request_id',
            'title',
            'description',
            'created_at',
            'start_time',
            'end_time',
            'delay',
            'duration',
            'accidental_delivery_duration',
            'origins',
            'destinations',
            'packages'
        )

    def create(self, validated_data):
        origin_data = validated_data.pop('origins')
        dest_data = validated_data.pop('destinations')
        pkg_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        origin = Origin.objects.create(order=order, **origin_data)
        destination = Destination.objects.create(order=order, **dest_data)
        for pkg in pkg_data:
            OrderPackage.objects.create(order=order, **pkg)

        return order

    def get_object(self, instance, validated_data):
        origin, _ = Origin.objects.get(id=instance.origin.id, defaults=validated_data.pop('origins'))
        destination, _ = Destination.objects.get(id=instance.destination.id,
                                                 defaults=validated_data.pop('destinations'))
        new_order, _ = Order.objects.get(id=order.id, defaults=validated_data)

        return new_order
