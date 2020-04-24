#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime as dt
#from datetime import timezone, timedelta
from django.utils import timezone
from googlemaps import Client as GoogleMaps
import unicodedata, re, os

def validateAddress(address, val):
    country = False
    prov = False
    for word in address.split():
        word = re.sub(',','',word,1)
        try:
            if word == 'Argentina': country=True
            if unicodedata.normalize('NFKD', word.lower()).encode('ASCII', 'ignore') == unicodedata.normalize('NFKD', val.lower()).encode('ASCII', 'ignore'): prov = True
        except:
            pass
        
    if country and prov:
        return True
    else:
        return False

def calcDeliveryTime(ori, dest):
    
    wk = ('street','house_num','suburb','city','latitude','longitude','pos_code')
    orAd = re.sub(',','',', '.join(str(value) for value in dict(zip(wk, [ori[k] for k in wk])).values() if value),1)
    desAd = re.sub(',','',', '.join(str(value) for value in dict(zip(wk, [dest[k] for k in wk])).values() if value),1)
    gmaps = GoogleMaps(os.getenv("GOOGLE_KEY"))
    print(orAd)
    print(desAd)
    directions_result = gmaps.directions(orAd, desAd, mode="driving", avoid="ferries", departure_time=timezone.now(), traffic_model="pessimistic")
    
    if validateAddress(directions_result[0]['legs'][0]['start_address'], ori['city']) and validateAddress(directions_result[0]['legs'][0]['end_address'], dest['city']):
        
        distance = directions_result[0]['legs'][0]['distance']['value']/1000
        ori['latitude'] = directions_result[0]['legs'][0]['start_location']['lat']
        ori['longitude'] = directions_result[0]['legs'][0]['start_location']['lng']
        dest['latitude'] = directions_result[0]['legs'][0]['end_location']['lat']
        dest['longitude'] = directions_result[0]['legs'][0]['end_location']['lng']
     
        if distance < 51:
            deltime = 6
        elif distance > 50 and distance < 701:
            deltime = 24
        elif distance > 700 and distance < 1400:
            deltime = 48
        else:
            deltime = 72    
    else:
        print('ADDRESS NOT VALIDATED')
        deltime = 99
    return ori, dest, deltime


def calc_time(ori, dest):


    timecut = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
    #a, b = calc_prov(cpo, cpd)
    ori, dest, r = calcDeliveryTime(ori, dest)

    if timezone.now() <= timecut:
        st = timecut
        et = st + dt.timedelta(hours=r)
    else:
        st = timecut + dt.timedelta(days=1)
        et = st + dt.timedelta(hours=r)

    return ori, dest, st, et, r