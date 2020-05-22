from rest_framework import serializers
from .models import Order, Origin, Destination, OrderStatus, OrderPackage
from utils.models import Status, State, Client
from .lib.pg_library import calc_time, normalizeWord


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
            'country',
            'latitude',
            'longitude',
            'pos_code'
        )

    def validate_city(self, value):
        try:
            State.objects.get(state_name__unaccent__iexact=normalizeWord(value))
            return value
        except:
            raise serializers.ValidationError('City Not found')


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
            'country',
            'latitude',
            'longitude',
            'pos_code'
        )

    def validate_city(self, value):
        try:
            State.objects.get(state_name__unaccent__iexact=normalizeWord(value))
            return value
        except:
            raise serializers.ValidationError('City Not found')


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

    def to_internal_value(self, value):
        client_inst = Client.objects.get(client_code=value['client'])
        value['client'] = client_inst.id
        value['origins']['country'] = 'Argentina'
        value['destinations']['country'] = 'Argentina'
        value['origins'], value['destinations'], value['start_time'], value['end_time'], value['duration'] = calc_time(value['origins'], value['destinations'])
        return super().to_internal_value(value)

    def create(self, validated_data):
        origin_data = validated_data.pop('origins')
        dest_data = validated_data.pop('destinations')
        pkg_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        Origin.objects.create(order=order, **origin_data)
        Destination.objects.create(order=order, **dest_data)
        OrderStatus.objects.create(order=order, location=State.objects.get(state_name__unaccent__iexact=normalizeWord(origin_data['city'])))
        for pkg in pkg_data:
            OrderPackage.objects.create(order=order, **pkg)
        return order
