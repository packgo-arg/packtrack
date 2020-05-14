import pandas as pd
import datetime as dt
import unicodedata
import re
import os
from django.utils import timezone
from googlemaps import Client as GoogleMaps


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


def getCoord(location):

    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))

    wk = ('street', 'house_num', 'suburb', 'city', 'country', 'pos_code')
    address = re.sub(',', '', ', '.join(value for value in dict(zip(wk, [location[k] for k in wk])).values() if value), 1)
    geocode_result = gmaps.geocode(address)

    if geocode_result:
        for data in geocode_result:
            for item in data['address_components']:
                for category in item['types']:
                    data[category] = {}
                    data[category] = item['long_name']
    else:
        print('COORDINATES NOT FOUND')

    if data.get('country') == 'Argentina' and normalizeWord(data.get('locality')) == normalizeWord(location['city']):
        location['latitude'] = data.get('geometry').get('location').get('lat')
        location['longitude'] = data.get('geometry').get('location').get('lng')
    else:
        print('COORDINATES NOT VALIDATED')
        print(data.get('locality'), '-', location['city'])

    return location


def calcDeliveryTime(ori, dest):

    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))

    wk = ('latitude', 'longitude')
    orAd = ','.join(str(value) for value in dict(zip(wk, [ori[k] for k in wk])).values() if value)
    desAd = ','.join(str(value) for value in dict(zip(wk, [dest[k] for k in wk])).values() if value)

    directions_result = gmaps.directions(orAd, desAd, mode="driving", avoid="ferries", departure_time=dt.datetime.now(), traffic_model="pessimistic")
    distance = directions_result[0]['legs'][0]['distance']['value'] / 1000

    if distance < 51:
        deltime = 6
    elif distance > 50 and distance < 701:
        deltime = 24
    elif distance > 700 and distance < 1400:
        deltime = 48
    else:
        deltime = 72

    return ori, dest, deltime


def calc_time(ori, dest):

    ori['country'] = 'Argentina'
    dest['country'] = 'Argentina'

    timecut = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

    if not ori['latitude'] or not ori['longitude']: ori = getCoord(ori)
    if not dest['latitude'] or not dest['longitude']: dest = getCoord(dest)

    try:
        ori, dest, r = calcDeliveryTime(ori, dest)
    except:
        print('ERROR GMAPS')
        r = 99

    if timezone.now() <= timecut:
        st = timecut
        et = st + dt.timedelta(hours=r)
    else:
        st = timecut + dt.timedelta(days=1)
        et = st + dt.timedelta(hours=r)

    return ori, dest, st, et, r