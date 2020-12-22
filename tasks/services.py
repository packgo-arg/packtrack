import unicodedata
import re
import os
from googlemaps import Client as GoogleMaps
import herepy
import requests
import time
from rest_framework import serializers


class DataService(object):

    """ Class for declaring Service related functions.

    """

    @staticmethod
    def getOrigin():

        """Get ORIGIN data if no origin was specified in the post request

        Returns:
            json: returns fixed origin values.
        """

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

        """ Populate Location Dictionary with data extracted from Google Maps API.
        This Location can be for both Origin and Destination.

        Raises:
            serializers.ValidationError: Validates that the returned country Geocoding values from Google API
            are the same as the one sent by the client.

        Returns:
            dictionary: location data.
        """

        start_time = time.time()

        location['street'] = data.get('short').get('route')
        location['location'] = dict(latitude=data.get('location').get('lat'), longitude=data.get('location').get('lng'))

        print('--- Tiempo de ejecucion popData: {} segundos ---'.format((time.time() - start_time)))
        return location


class ValidateService(object):

    """ Class for declaring Validation functions.

    """

    @staticmethod
    def normalizeWord(word):

        """ Return word converted to lowercase and stripped from accents.

        Returns:
            string: string normalized with lowercase and without accents.
        """

        return unicodedata.normalize('NFKD', word.lower()).encode('ASCII', 'ignore').decode('utf-8')

    @staticmethod
    def listToAddr(location):

        """ Returns an address string constructed from a Location dictionary.

        Returns:
            string: address string constructed from a Location dictionary.
        """

        start_time = time.time()
        wk = [key for key in location.keys() if key in ('street', 'house_num', 'suburb', 'city', 'province', 'country', 'pos_code')]
        address = re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1)
        print('--- Tiempo de ejecucion listToAddr: {} segundos ---'.format((time.time() - start_time)))
        return address


class LocationService(object):

    """ Class for declaring functions related to location services and APIs.

    """

    @staticmethod
    def getLocal(endpoint, param):

        """ Validate Locality or City using https://datosgobar.github.io/georef-ar-api/

        Returns:
            json: response with city normalization from https://datosgobar.github.io/georef-ar-api/ 
        """

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

        """ Get coordinates for location using Google Maps Geolocation API.

        Raises:
            serializers.ValidationError: Google Maps API could not find pair of
            coordinates suitable for address passed as input.

        Returns:
            dictionary: Geocoding information.
        """

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

        """ Get routing time based on coordinates for origin and destination using HERE routing API.

        Returns:
            string: Returns delivery time and distance calculated with Here API.
        """

        start_time = time.time()

        routingApi = herepy.RoutingApi(os.getenv("HERE_KEY"))

        response = routingApi.truck_route(ori.coords[::-1], dest.coords[::-1], [herepy.RouteMode.truck, herepy.RouteMode.fastest]).as_dict()
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
    def calcOrderPrice(km, package, pkgType):

        """ Calculate Delivery price

        Returns:
            int: Total price calculation based on size and quantity of packages in order
        """

        start_time = time.time()

        km = int(round(km))
        r = [1, 2, 3, 3]
        if km >= 100:
            mult = int(km // 100 + 3)**pkgType.pkg_coef
        else:
            mult = int(r[km // 25])**pkgType.pkg_coef

        ''' DEPRECATED
        if 10 < package.get('quantity') < 20:
            disc += 0.1
        elif 20 < package.get('quantity') < 30:
            disc += 0.2
        elif 30 < package.get('quantity') < 40:
            disc += 0.3
        elif 40 < package.get('quantity'):
            disc += 0.4

        base = pkgType.pkg_price - (pkgType.pkg_price * disc)
        '''
        total = package.get('pack_price') * mult

        print('--- Tiempo de ejecucion calcPrice: {} segundos ---'.format((time.time() - start_time)))

        return total