import datetime as dt
import unicodedata
import re
import os
from django.utils import timezone
from googlemaps import Client as GoogleMaps
import herepy


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


def getCoord(location):

    msj = ''
    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))

    wk = ('street', 'house_num', 'suburb', 'city', 'province', 'country', 'pos_code')
    address = re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1)
    geocode_result = gmaps.geocode(address)

    if geocode_result:
        for data in geocode_result:
            for item in data['address_components']:
                for category in item['types']:
                    data[category] = {}
                    data[category] = item['long_name']
    else:
        msj = 'Coordinates not found. Please check Address sent'

    if data.get('country') == location['country'] and normalizeWord(data.get('locality')) == normalizeWord(location['city']) and data.get('route'):
        location['street'] = data.get('route')
        location['city'] = data.get('locality')
        location['province'] = data.get('administrative_area_level_1')
        location['latitude'] = data.get('geometry').get('location').get('lat')
        location['longitude'] = data.get('geometry').get('location').get('lng')
    else:
        msj ='Address not Validated'

    print(msj)

    return location, msj


def calcDeliveryTime(ori, dest):

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

    return deltime, distance


def calcPrice(km, disc, pack, info):

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

    return total