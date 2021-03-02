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
from random import randint

class ReturnSerializer(serializers.ModelSerializer):

    """
    Serializer for returning Order Post Information
    """

    class Meta:
        model = Order
        fields = (
            'id',
            'request_id',
            'start_time',
            'end_time',
            'duration'
        )


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
            'pack_price',
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
        client_inst = Client.objects.get(id=self.root.initial_data['client'])

        if pk_info.id == 1:
            value['pack_price'] = client_inst.base_price * value['quantity']
        elif pk_info.id == 3:
            value['height'] = 2000
            value['width'] = 1000
            value['length'] = 1000
            value['volume'] = value.get('height') * value.get('width') * value.get('length') / 1000**3
            value['pack_price'] = client_inst.base_price + (value['quantity'] * client_inst.unit_price * value['volume'])
        else:
            if client_inst.price_calc == 1:
                value['pack_price'] = client_inst.base_price * value['quantity']
            else:
                if client_inst.unit_type == 0:
                    try:
                        value['volume'] = value.get('height') * value.get('width') * value.get('length') / 1000**3
                    except Exception as e:
                        raise serializers.ValidationError(e.message)

                    value['pack_price'] = client_inst.base_price + (value['quantity'] * client_inst.unit_price * value['volume'])

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
            #'request_id',
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
        print(f"INICIO DE RUTINA: {start_time}")
        print('--- INICIO ORDER_TO_INTERNAL ---')

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

        value['ord_price'] = 0

        for pack in value['packages']:
            pk_info = Package.objects.get(pkg_name=pack['pack_type'])
            pack['pack_price'] = CalcService.calcOrderPrice(distance, pack, pk_info)
            value['ord_price'] += pack['pack_price']
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
