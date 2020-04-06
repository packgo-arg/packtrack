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

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

class OrderStatusSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
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

    def get_status(self, obj):
        try:
            status_inst = Status.objects.get(pk=obj.status_id)
            return status_inst.status_name
        except Status.DoesNotExist:
            return print('ERROR STATUS')

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
            'latitude',
            'longitude',
            'pos_code'
        )


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
            'latitude',
            'longitude',
            'pos_code'
        )


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPackage
        fields = (
            'pak_type',
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
