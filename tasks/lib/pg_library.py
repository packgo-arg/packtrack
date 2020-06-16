import datetime as dt
import unicodedata
import re
import os
from django.utils import timezone
from googlemaps import Client as GoogleMaps
import herepy
<<<<<<< HEAD
=======
import requests
import time

>>>>>>> a053084... commit changes


def normalizeWord(word):
    return unicodedata.normalize('NFKD', word.lower()).encode('ASCII', 'ignore').decode('utf-8')


def validateAddress(address):
    country = False
    for word in address.split():
        word = re.sub(',', '', word, 1)
        try:
            if word == 'Argentina': country = True
        except:
            pass

    if country:
        return True
    else:
        return False


def jsonForApi(local, city, apipoint):
    dictio = {
        apipoint: [
            {
                "nombre": local,
                "provincia": city,
            }
        ]
    }
    return dictio


<<<<<<< HEAD
def getCoord(location):

    msj = ''
    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))

    wk = ('street', 'house_num', 'suburb', 'city', 'province', 'country', 'pos_code')
    address = re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1)
=======
def popOrigin():
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


def getLocal(endpoint, param):
    d = {}
    d[endpoint] = param
    if '_' in endpoint:
        url = re.sub("_","-",endpoint)
    else:
        url = endpoint

    req = requests.post(f'{os.getenv("API_BASE_URL")}{url}', json=d).json()
    req = req.get('resultados', None)[0].get(endpoint, None)[0]
    return req


def getCoord(location):
    start_time = time.time()
    msj = ''
    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))

    wk = []
    for key in location.keys():
        if 'name' not in key:
            wk.append(key)
    address = normalizeWord(re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1))

    print(f"ADDRESS: {address}")
>>>>>>> a053084... commit changes
    geocode_result = gmaps.geocode(address)

    data = {'long': {}, 'short': {}, 'location': {}}

    if geocode_result:
        for geolist in geocode_result:
            for item in geolist['address_components']:
                for category in item['types']:
                    data['long'].update([(category,item['long_name'])])
                    data['short'].update([(category,item['short_name'])])
            data['location'] = geolist['geometry']['location']
    else:
        msj = 'Coordinates not found. Please check Address sent'

<<<<<<< HEAD
    if data.get('country') == location['country'] and normalizeWord(data.get('locality')) == normalizeWord(location['city']) and data.get('route'):
        location['street'] = data.get('route')
        location['city'] = data.get('locality')
        location['province'] = data.get('administrative_area_level_1')
        location['latitude'] = data.get('geometry').get('location').get('lat')
        location['longitude'] = data.get('geometry').get('location').get('lng')
    else:
        msj ='Address not Validated'

    print(msj)
=======
    try:
        data['long']['administrative_area_level_1'] = getLocal('provincias', [dict(nombre=data.get('long').get('administrative_area_level_1'))]).get('nombre', None)
    except IndexError:
        raise serializers.ValidationError('Could not validate Locality')

    #print('location country: {} - gmaps country: {}'.format(location['country'], data.get('long').get('country')))
    #print('gmaps route: {}'.format(data.get('short').get('route')))
    print(f"DATA: {data['long']['administrative_area_level_1']}")

    if data.get('long').get('country') == location['country'] and normalizeWord(data.get('long').get('administrative_area_level_1')) == normalizeWord(location['province']):
        if data.get('short').get('route'): location['street'] = data.get('short').get('route')
        if data.get('short').get('locality'): location['city'] = data.get('short').get('locality')
        location['province'] = data.get('long').get('administrative_area_level_1')
        location['latitude'] = data.get('location').get('lat')
        location['longitude'] = data.get('location').get('lng')
    else:
        msj = 'Address not Validated'

    print(data['long']['administrative_area_level_1'])
    print('--- Tiempo de ejecucion getCoord: {} segundos ---'.format((time.time() - start_time)))
    return location, msj
>>>>>>> a053084... commit changes

    return location, msj

<<<<<<< HEAD

def calcDeliveryTime(ori, dest):

=======
def calcDeliveryTime(ori, dest):
    start_time = time.time()

>>>>>>> a053084... commit changes
    routingApi = herepy.RoutingApi(os.getenv("HERE_KEY"))

    response = routingApi.truck_route([ori.get('latitude'), ori.get('longitude')],
                                  [dest.get('latitude'), dest.get('longitude')],
                                  [herepy.RouteMode.truck, herepy.RouteMode.fastest]).as_dict()
    distance = response.get('response').get('route')[0].get('summary').get('distance') / 1000

    if distance < 51:
        deltime = 6
    elif distance > 50 and distance < 701:
        deltime = 24
    elif distance > 700 and distance < 1400:
        deltime = 48
    else:
        deltime = 72

<<<<<<< HEAD
=======
    print(deltime)
    print('--- Tiempo de ejecucion calcDeliveryTime: {} segundos ---'.format((time.time() - start_time)))

>>>>>>> a053084... commit changes
    return deltime, distance


def calcPrice(km, disc, pack, info):
<<<<<<< HEAD
=======
    start_time = time.time()
>>>>>>> a053084... commit changes

    km = int(round(km))
    r = [1, 2, 3, 3]
    if km >= 100:
        mult = int(km // 100 + 3)**info.pkg_coef
    else:
        mult = int(r[km//25])**info.pkg_coef

    if 10 < pack.get('quantity') < 20:
        disc += 0.1
    elif 20 < pack.get('quantity') < 30:
        disc += 0.2
    elif 30 < pack.get('quantity') < 40:
        disc += 0.3
    elif 40 < pack.get('quantity'):
        disc += 0.4

    base = info.pkg_price - (info.pkg_price * disc)
    total = (base * mult) * pack.get('quantity')
<<<<<<< HEAD
=======
    print('--- Tiempo de ejecucion calcPrice: {} segundos ---'.format((time.time() - start_time)))
>>>>>>> a053084... commit changes

    return total