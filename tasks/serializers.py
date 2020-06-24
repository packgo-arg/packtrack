from rest_framework import serializers
from django.utils import timezone
from .models import Order, Origin, Destination, OrderStatus, OrderPackage
from utils.models import Status, State, Client, Package
import datetime as dt
import time
from .services import DataService, ValidateService, LocationService, CalcService


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
            return location_inst.city
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
        print('--- INICIO ORIGIN_TO_INTERNAL ---')
        start_time = time.time()

        try:
            req = LocationService.getLocal('localidades_censales', [dict(nombre=value['city'], provincia=value['province'])])
            value['city'] = req.get('nombre', None)
            value['province'] = req.get('provincia', None).get('nombre', None)
            if 'suburb' in value.keys() and 'barrio' not in ValidateService.normalizeWord(value['suburb']):
                value['suburb'] = 'Barrio ' + value['suburb']
        except IndexError:
            raise serializers.ValidationError('Could not validate Locality')

        if 'latitude' not in value.keys() or 'longitude' not in value.keys() or not value['latitude'] or not value['longitude']:
            orAdd = ValidateService.listToAddr(value)
            orData = LocationService.getCoord(orAdd)
            value = DataService.popData(orData, value)
        print('--- Tiempo de ejecucion Origin_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate_city(self, value):
        start_time = time.time()
        print('--- INICIO ORDER_VALIDATE_CITY ---')
        try:
            State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(value))
            print('--- Tiempo de ejecucion Origin_validate_city: {} segundos ---'.format((time.time() - start_time)))
            return value
        except:
            print('--- Tiempo de ejecucion Origin_validate_city (fail): {} segundos ---'.format((time.time() - start_time)))
            raise serializers.ValidationError('Origin address: Pack GO does not provide services in that location')


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
        start_time = time.time()
        print('--- INICIO DEST_TO_INTERNAL ---')
        try:
            req = LocationService.getLocal('localidades_censales', [dict(nombre=value['city'], provincia=value['province'])])
            value['city'] = req.get('nombre', None)
            value['province'] = req.get('provincia', None).get('nombre', None)
            if 'suburb' in value.keys() and 'barrio' not in ValidateService.normalizeWord(value['suburb']):
                value['suburb'] = 'Barrio ' + value['suburb']
        except IndexError:
            raise serializers.ValidationError('Could not validate locality')

        if 'latitude' not in value.keys() or 'longitude' not in value.keys() or not value['latitude'] or not value['longitude']:
            destAdd = ValidateService.listToAddr(value)
            destData = LocationService.getCoord(destAdd)
            value = DataService.popData(destData, value)
        print('--- Tiempo de ejecucion Dest_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate_city(self, value):
        start_time = time.time()
        print('--- INICIO DEST_VALIDATE_CITY ---')
        try:
            State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(value))
            print('--- Tiempo de ejecucion Dest_validate_city: {} segundos ---'.format((time.time() - start_time)))
            return value
        except:
            print('--- Tiempo de ejecucion Dest_validate_city (fail): {} segundos ---'.format((time.time() - start_time)))
            raise serializers.ValidationError('Destination address: Pack GO does not provide services in that location')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPackage
        fields = (
            'pak_type',
            'quantity',
            'ord_pak_price'
        )


class OrderPriceSerializer(serializers.ModelSerializer):

    packages = PackageSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'request_id',
            'created_at',
            'ord_price',
            'packages'
        )


class PriceCalcSerializer(serializers.ModelSerializer):

    packages = PackageSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'origin_city',
            'origin_province',
            'dest_city',
            'dest_province',
            'packages',
            'ord_price'
        )

    def to_internal_value(self, value):
        start_time = time.time()
        print('--- INICIO PRICE_CALC_TO_INT ---')
        try:
            ori = LocationService.getLocal('localidades_censales', [dict(nombre=value['origin_city'], provincia=value['province'])])
            value['origin_city'] = ori.get('nombre', None)
            value['origin_province'] = ori.get('provincia', None).get('nombre', None)
        except IndexError:
            raise serializers.ValidationError('Could not validate Origin locality')
        try:
            dest = LocationService.getLocal('localidades_censales', [dict(nombre=value['dest_city'], provincia=value['province'])])
            value['dest_city'] = dest.get('nombre', None)
            value['dest_province'] = dest.get('provincia', None).get('nombre', None)
        except IndexError:
            raise serializers.ValidationError('Could not validate Destnation locality')

        orCoord, destCoord = {}, {}
        orAdd = ValidateService.listToAddr(dict(city=value['origin_city'], province=value['origin_province']))
        orData = LocationService.getCoord(orAdd)
        orCoord['lat'] = orData.get('location', None).get('lat', None)
        orCoord['lng'] = orData.get('location', None).get('lng', None)
        destAdd = ValidateService.listToAddr(dict(city=value['dest_city'], province=value['dest_province']))
        destData = LocationService.getCoord(destAdd)
        destCoord['lat'] = destData.get('location', None).get('lat', None)
        destCoord['lng'] = destData.get('location', None).get('lng', None)

        try:
            duration, distance = LocationService.getDeliveryTime(dict(latitude=orCoord['lat'], longitude=orCoord['lng']), dict(latitude=destCoord['lat'], longitude=orCoord['lng']))
        except:
            raise serializers.ValidationError('Could not parse coordinates')

        value['ord_price'] = 0
        disc = Client.objects.get(client_name=value['client']).price_disc
        for pack in value['packages']:
            pk_info = Package.objects.get(pkg_name=pack['pak_type'])
            pack['ord_pak_price'] = CalcService.calcPrice(distance, disc, pack, pk_info)
            value['ord_price'] += pack['ord_pak_price']
        print('--- Tiempo de ejecucion Order_validate: {} segundos ---'.format((time.time() - start_time)))
        return value

        print('--- Tiempo de ejecucion priceCalc: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate_origin_city(self, value):
        start_time = time.time()
        print('--- INICIO VALIDATE_CALC_ORIGIN_CITY ---')
        try:
            State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(value))
            print('--- Tiempo de ejecucion Calc_Origin_City_Validation: {} segundos ---'.format((time.time() - start_time)))
            return value
        except:
            print('--- Tiempo de ejecucion Calc_Origin_City_Validation (fail): {} segundos ---'.format((time.time() - start_time)))
            raise serializers.ValidationError('Destination address: Pack GO does not provide services in that location')

    def validate_dest_city(self, value):
        start_time = time.time()
        print('--- INICIO VALIDATE_CALC_DEST_CITY ---')
        try:
            State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(value))
            print('--- Tiempo de ejecucion Calc_Dest_City_Validation: {} segundos ---'.format((time.time() - start_time)))
            return value
        except:
            print('--- Tiempo de ejecucion Calc_Dest_City_Validation (fail): {} segundos ---'.format((time.time() - start_time)))
            raise serializers.ValidationError('Destination address: Pack GO does not provide services in that location')


class OrderSerializer(serializers.ModelSerializer):
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
        start_time = time.time()
        print('--- INICIO ORDER_TO_INTERNAL ---')

        client_inst = Client.objects.get(client_code=value['client'])

        value['client'] = client_inst.id

        if 'origins' not in value.keys():
            value['origins'] = dict(DataService.getOrigin())
        print('--- Tiempo de ejecucion Order_to_internal: {} segundos ---'.format((time.time() - start_time)))
        return super().to_internal_value(value)

    def validate(self, value):
        start_time = time.time()
        print('--- INICIO ORDER_VALIDATE ---')
        try:
            value['duration'], distance = LocationService.getDeliveryTime(value['origins'], value['destinations'])
        except:
            value['duration'] = 99
            raise serializers.ValidationError('Could not parse coordinates')
        if timezone.localtime().time() < dt.time(15):
            value['start_time'] = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
        else:
            value['start_time'] = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)

        value['end_time'] = value['start_time'] + dt.timedelta(hours=int(value['duration']))

        value['ord_price'] = 0
        disc = Client.objects.get(client_name=value['client']).price_disc
        for pack in value['packages']:
            pk_info = Package.objects.get(pkg_name=pack['pak_type'])
            pack['ord_pak_price'] = CalcService.calcPrice(distance, disc, pack, pk_info)
            value['ord_price'] += pack['ord_pak_price']
        print('--- Tiempo de ejecucion Order_validate: {} segundos ---'.format((time.time() - start_time)))
        return value

    def create(self, validated_data):
        origin_data = validated_data.pop('origins')
        dest_data = validated_data.pop('destinations')
        pkg_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        Origin.objects.create(order=order, **origin_data)
        Destination.objects.create(order=order, **dest_data)
        OrderStatus.objects.create(order=order, location=State.objects.get(city__unaccent__iexact=ValidateService.normalizeWord(origin_data['city'])))
        for pkg in pkg_data:
            OrderPackage.objects.create(order=order, **pkg)
        return order
