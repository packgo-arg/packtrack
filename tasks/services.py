import unicodedata
import re
import os
from googlemaps import Client as GoogleMaps
import herepy
import requests
import time
from rest_framework import serializers


class DataService(object):

    @staticmethod
    def getOrigin():
        start_time = time.time()
        origin = {
            "name": "Deposito PackGo",
            "street": "Alvarez de Condarco",
            "house_num": 2199,
            "suburb": "",
            "city": "Córdoba",
            "province": "Córdoba",
            "country": "Argentina",
            "latitude": "-31.383496",
            "longitude": "-64.127273",
            "pos_code": "5012"
        }
        print('--- Tiempo de ejecucion popOrigin: {} segundos ---'.format((time.time() - start_time)))

        return origin

    @staticmethod
    def popData(data, location):

        start_time = time.time()

        if data.get('long').get('country') == location['country'] and data.get('short').get('route'):
            location['street'] = data.get('short').get('route')
            location['city'] = data.get('short').get('locality')
            location['province'] = data.get('long').get('administrative_area_level_1')
            location['latitude'] = data.get('location').get('lat')
            location['longitude'] = data.get('location').get('lng')
        else:
            raise serializers.ValidationError('Validation Error: Could not validate route')

        print('--- Tiempo de ejecucion popData: {} segundos ---'.format((time.time() - start_time)))
        return location


class ValidateService(object):

    @staticmethod
    def normalizeWord(word):
        return unicodedata.normalize('NFKD', word.lower()).encode('ASCII', 'ignore').decode('utf-8')

    @staticmethod
    def listToAddr(location):
        start_time = time.time()
        wk = [key for key in location.keys() if key in ('street', 'house_num', 'suburb', 'city', 'province', 'country', 'pos_code')]
        address = re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1)
        print('--- Tiempo de ejecucion listToAddr: {} segundos ---'.format((time.time() - start_time)))
        return address


class LocationService(object):

    @staticmethod
    def getLocal(endpoint, param):
        start_time = time.time()
        d = {}
        d[endpoint] = param
        if '_' in endpoint:
            url = re.sub("_", "-", endpoint)
        else:
            url = endpoint

        req = requests.post(f'{os.getenv("API_BASE_URL")}{url}', json=d).json()
        req = req.get('resultados', None)[0].get(endpoint, None)[0]

        print('--- Tiempo de ejecucion getLocal: {} segundos ---'.format((time.time() - start_time)))
        return req

    @staticmethod
    def getCoord(address):
        start_time = time.time()
        gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))
        geocode_result = gmaps.geocode(address)

        data = {'long': {}, 'short': {}, 'location': {}}

        if geocode_result:
            for geolist in geocode_result:
                for item in geolist['address_components']:
                    for category in item['types']:
                        data['long'].update([(category, item['long_name'])])
                        data['short'].update([(category, item['short_name'])])
                data['location'] = geolist['geometry']['location']
        else:
            raise serializers.ValidationError('GeoCoding Error: Could not parse coordinates')

        print('--- Tiempo de ejecucion getCoord: {} segundos ---'.format((time.time() - start_time)))

        return data

    @staticmethod
    def getDeliveryTime(ori, dest):
        start_time = time.time()

        routingApi = herepy.RoutingApi(os.getenv("HERE_KEY"))

        response = routingApi.truck_route([ori.get('latitude'), ori.get('longitude')], [dest.get('latitude'), dest.get('longitude')], [herepy.RouteMode.truck, herepy.RouteMode.fastest]).as_dict()
        distance = response.get('response').get('route')[0].get('summary').get('distance') / 1000

        if distance < 51:
            deltime = 6
        elif distance > 50 and distance < 701:
            deltime = 24
        elif distance > 700 and distance < 1400:
            deltime = 48
        else:
            deltime = 72

        print('--- Tiempo de ejecucion calcDeliveryTime: {} segundos ---'.format((time.time() - start_time)))

        return deltime, distance


class CalcService(object):

    @staticmethod
    def calcPrice(km, disc, package, pkgType):

        start_time = time.time()

        km = int(round(km))
        r = [1, 2, 3, 3]
        if km >= 100:
            mult = int(km // 100 + 3)**pkgType.pkg_coef
        else:
            mult = int(r[km // 25])**pkgType.pkg_coef

        if 10 < package.get('quantity') < 20:
            disc += 0.1
        elif 20 < package.get('quantity') < 30:
            disc += 0.2
        elif 30 < package.get('quantity') < 40:
            disc += 0.3
        elif 40 < package.get('quantity'):
            disc += 0.4

        base = pkgType.pkg_price - (pkgType.pkg_price * disc)
        total = (base * mult) * package.get('quantity')

        print('--- Tiempo de ejecucion calcPrice: {} segundos ---'.format((time.time() - start_time)))

        return total