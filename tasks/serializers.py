from rest_framework import serializers
from rest_framework.response import Response
from drf_extra_fields.geo_fields import PointField
from django.utils import timezone
from tasks.models import Order, Origin, Destination, OrderStatus, OrderPackage
from tasks.services import DataService, ValidateService, LocationService, CalcService
from utils.models import Status, State, Client, Package, Driver
import datetime as dt
import time, os
import geocoder
import logging

logger = logging.getLogger('api')

class ReturnSerializer(serializers.ModelSerializer):

    """
    Serializer for returning Order Post Information
    """
    tag = serializers.SerializerMethodField('get_order_id')

    class Meta:
        model = Order
        fields = (
            'id',
            'tag',
            'request_id',
            'start_time',
            'end_time',
            'duration'
        )
    
    def get_order_id(self, obj):
        return obj.order_id


class OrderStatusSerializer(serializers.ModelSerializer):

    """
    Serializer for handling Status query requests

    Raises:
        serializers.ValidationError: 'Could not validate Locality'

    Returns:
        string: location instance
    """
    driver = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatus
        fields = (
            'order',
            'status',
            'driver',
            'location',
            'st_update'
        )
    
    def get_driver(self, obj):
        if not obj.driver_id: return None
        try:
            driver_inst = Driver.objects.get(pk=obj.driver_id)
            return driver_inst.driv_name
        except Driver.DoesNotExist:
            raise serializers.ValidationError('Could not validate Driver')

    def get_location(self, obj):
        if not obj.location_id: return None
        try:
            location_inst = State.objects.get(pk=obj.location_id)
            return location_inst.city
        except State.DoesNotExist:
            raise serializers.ValidationError('Could not validate Locality')


class OriginSerializer(serializers.ModelSerializer):

    """Process Origin information"""

    location = PointField()

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
            'location',
            'pos_code',
            'geo_data',
            'is_covered',
        )

    def to_internal_value(self, value):
        print('--- INICIO ORIGIN_TO_INTERNAL ---')
        start_time = time.time()

        """Validate Origin location using Validation Service
        Check if Coordinates data were passed in request.
        If not, populate dict with Location Services.

        Raises:
            serializers.ValidationError: Could not validate
            if locality received is among localities where
            service is provided

        Returns:
            json: Origin model serializer
        """
        if 'latitude' not in value.keys() or 'longitude' not in value.keys() or not value['latitude'] or not value['longitude']:
            origin_address = ValidateService.listToAddr(value)
            geo_data = geocoder.google(origin_address, key=os.getenv("GOOGLE_KEY"))
            if geo_data.ok:
                value['geo_data'] = geo_data.json
                value['location'] = dict(latitude=geo_data.latlng[0], longitude=geo_data.latlng[1])
            else:
                raise serializers.ValidationError({'Error': 'Could not get coordinates from data', 'Geodata': value})
        else:
            value['location'] = dict(latitude=float(value['latitude']), longitude=float(value['longitude']))
            geo_data = geocoder.google(list(value['location'].values()), key=os.getenv("GOOGLE_KEY"), method='reverse')
            value['geo_data'] = geo_data.json
            
        print('--- Tiempo de ejecucion Origin_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate(self, value):

        """Validate if Pack GO provide services in the area requested.
        This is done consulting the db.

        Raises:
            serializers.ValidationError: 'Origin address: Pack GO
            does not provide services in that location'

        Returns:
            string : Origin city
        """

        start_time = time.time()
        print('--- INICIO ORIGIN_VALIDATE_LOCATION ---')
        query = State.objects.filter(mpoly__intersects=value['location'])
        if not query:
            print('--- Tiempo de ejecucion Origin_validate_city (fail): {} segundos ---'.format((time.time() - start_time)))
            value['is_covered'] = False
        else:
            print('--- Tiempo de ejecucion Origin_validate_city: {} segundos ---'.format((time.time() - start_time)))
            value['is_covered'] = True
        return value


class DestinationSerializer(serializers.ModelSerializer):

    """Process Destination information"""

    location = PointField()

    class Meta:
        model = Destination
        fields = (
            'name',
            'email',
            'phone',
            'street',
            'house_num',
            'ap_unit',
            'suburb',
            'city',
            'province',
            'country',
            'location',
            'pos_code',
            'geo_data',
            'is_covered',
        )

    def to_internal_value(self, value):
        start_time = time.time()
        print('--- INICIO DEST_TO_INTERNAL ---')

        """Validate Destination location using Validation Service.
        Check if Coordinates data were passed in request.
        If not, populate dict with Location Services.

        Raises:
            serializers.ValidationError: 'Destination address: Pack GO
            does not provide services in that location'

        Returns:
            json: Destination model serializer
        """

        if 'latitude' not in value.keys() or 'longitude' not in value.keys() or not value['latitude'] or not value['longitude']:
            destination_address = ValidateService.listToAddr(value)
            geo_data = geocoder.google(destination_address, key=os.getenv("GOOGLE_KEY"))
            if geo_data.ok:
                value['geo_data'] = geo_data.json
                value['location'] = dict(latitude=geo_data.latlng[0], longitude=geo_data.latlng[1])
            else:
                raise serializers.ValidationError({'Error': 'Could not get coordinates from data', 'Geodata': value})
        else:
            value['location'] = dict(latitude=float(value['latitude']), longitude=float(value['longitude']))
            geo_data = geocoder.google(list(value['location'].values()), key=os.getenv("GOOGLE_KEY"), method='reverse')
            value['geo_data'] = geo_data.json
            
        print('--- Tiempo de ejecucion destination_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate(self, value):

        """Validate if Pack GO provide services in the area requested.
        This is done consulting the db.

        Raises:
            serializers.ValidationError: 'Destination address: Pack GO
            does not provide services in that location'

        Returns:
            string : Destination city
        """

        start_time = time.time()
        print('--- INICIO Destination_VALIDATE_LOCATION ---')
        query = State.objects.filter(mpoly__intersects=value['location'])
        if not query:
            print('--- Tiempo de ejecucion Destination_validate_city (fail): {} segundos ---'.format((time.time() - start_time)))
            value['is_covered'] = False
        else:
            print('--- Tiempo de ejecucion Destination_validate_city: {} segundos ---'.format((time.time() - start_time)))
            value['is_covered'] = True
        return value


class PackageSerializer(serializers.ModelSerializer):

    """ Package Serializer to receive nested order package information.
    """
    class Meta:
        model = OrderPackage
        fields = (
            'pack_type',
            'height', 
            'width',
            'length',
            'volume',
            'weight',
            'quantity',
        )
    
    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    def validate(self, value):

        """ Calculate delivery time and order price with services functions.

        Raises:
            serializers.ValidationError: Could not get delivery time.

        Returns:
            json: order request validated data.
        """

        start_time = time.time()
        print('--- INICIO PACKAGE_VALIDATE ---')
        pk_info = Package.objects.get(pkg_name=value['pack_type'])
        client = Client.objects.get(id=self.root.initial_data['client'])
        
        if client.price_calc == 0:
            if client.unit_type == 0:
                keys = ['height', 'width', 'length']
            elif client.unit_type == 1:
                keys = ['weight']

            if pk_info.id == 2 and (not all(key in value for key in keys) or not any(v>0 for k, v in value.items() if k in keys)):
                raise serializers.ValidationError({'Error': 'Must provide package measurements'})
            elif pk_info.id != 2 and client.unit_type == 0:
                for _, key in enumerate(keys):
                    value[key] = pk_info.__dict__.get(key)

        value['volume'] = value.get('height', 0) * value.get('width', 0) * value.get('length', 0) / (1000**3)

        print('--- Tiempo de ejecucion Package_validate: {} segundos ---'.format((time.time() - start_time)))
        return value

class PackCalcSerializer(serializers.ModelSerializer):

    """ Process Order Price Calculator requests with information regarding price of an estimated package delivery
    """
    class Meta:
        model = OrderPackage
        fields = (
            'pack_type',
            'quantity',
            'pack_price',
        )


class OrderPriceSerializer(serializers.ModelSerializer):

    """ Process Order Price Calculator requests with information regarding price of an estimated package delivery
    """

    packages = PackCalcSerializer(many=True) 
    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'ord_price',
            'packages'
        )

class OrderSerializer(serializers.ModelSerializer):

    """ Order Serializer. Serialize order information.

    """
    origins = OriginSerializer(required=False)
    destinations = DestinationSerializer()
    packages = PackageSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
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

        """ Convert client code to client_id for db write.


        Returns:
            json: order request pre processed data.
        """
        start_time = time.time()
        print('--- INICIO ORDER_TO_INTERNAL ---')
        client_instance = Client.objects.get(users=self.context['request'].user)
        last_order = Order.objects.filter(client=client_instance.id).latest('created_at')
        value['order_id'] = DataService.generateOrderId(last_order, client_instance.client_code)
        if 'origins' not in value.keys():
            value['origins'] = dict(DataService.getOrigin())
        print('--- Tiempo de ejecucion Order_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate(self, value):

        """ Calculate delivery time and order price with services functions.

        Raises:
            serializers.ValidationError: Could not get delivery time.

        Returns:
            json: order request validated data.
        """

        start_time = time.time()
        print('--- INICIO ORDER_VALIDATE ---')

        value['duration'], distance = LocationService.getDeliveryTime(value['origins']['location'], value['destinations']['location'])

        if bool('start_time' in value.keys()) != bool('end_time' in value.keys()):
            raise serializers.ValidationError({"time_fields": "Must enter both start and end time"})
        
        if 'start_time' not in value.keys():
            if timezone.localtime().time() < dt.time(15):
                value['start_time'] = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
            else:
                value['start_time'] = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)

        if 'end_time' not in value.keys():
            value['end_time'] = value['start_time'] + dt.timedelta(hours=int(value['duration']))
        else:
            if value['end_time'] < value['start_time']:
                raise serializers.ValidationError({"end_time": "End time cannot be before Start time"})

        client = Client.objects.get(id=self.root.initial_data['client'])
        order_volume = 0

        for idx, pack in enumerate(value['packages'], 1):
            order_volume += pack['volume'] * pack['quantity']
            pack['package_id'] = f"{value['order_id']}-{idx:02d}"
        if client.price_calc == 0:
            value['ord_price'] = client.base_price + (client.unit_price * order_volume)
        else:
            value['ord_price'] = client.base_price
            
        value['ord_price'] = round(CalcService.calcOrderPrice(distance, value['ord_price'], client.distance_coef), 2)

        print('--- Tiempo de ejecucion Order_validate: {} segundos ---'.format((time.time() - start_time)))
        return value

    def create(self, validated_data):

        """ Override default serializer create method to include nested serializers.

        Returns:
            serialized object: Order serialized data.
        """
        origin_data = validated_data.pop('origins')
        dest_data = validated_data.pop('destinations')
        pkg_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        Origin.objects.create(order=order, **origin_data)
        Destination.objects.create(order=order, **dest_data)
 #       OrderStatus.objects.create(order=order, location=State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(origin_data['city'])))
        for pkg in pkg_data:
            OrderPackage.objects.create(order=order, **pkg)
        return order
