#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains geolocation routines."""

import json
import pycountry
import sdconfig
import sdnetutils
from sdexception import SDException

def compute_distance(client_place,datanode_place):
    (cli_lat,cli_lng)=client_place
    (dn_lat,dn_lng)=datanode_place

    distance=haversine(cli_lng, cli_lat, dn_lng, dn_lat)

    return distance

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on the earth.

    Args:
        lng/lat of both places (specified in decimal degrees)

    Returns:
        distance in km

    From http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """
    from math import radians, cos, sin, asin, sqrt

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def get_datanode_place(data_node):
    country_code=domain_to_country_code(data_node)
    country_name=country_code_to_country_name(country_code)
    place=country_name_to_country_place(country_name)
    return place

def domain_to_country_code(domain):
    """
    Returns:
        code: ISO 3166 country code
    """
    ext=domain.split(".")[-1]

    if ext == 'gov':
        country_code='US'
    elif ext == 'com':
        country_code='US'
    elif ext == 'edu':
        country_code='US'
    elif ext == 'net':
        country_code='US'
    elif ext == 'org':
        country_code='US'
    elif ext == 'uk':
        # following this page => http://fr.wikipedia.org/wiki/ISO_3166-1
        # UK seems valid, but the module 'pycountry' doesn't support it,
        # so let's force it to 'GB'
        country_code='GB'
    else:
        country_code=ext.upper()

    return country_code

def country_name_to_country_place(country_name):
    """
    API doc => https://developers.google.com/maps/documentation/geocoding
    """
    url="http://maps.googleapis.com/maps/api/geocode/json?address=%s"%country_name.replace(" ","%20") # as parameters can contain spaces, we need to encode them 
    buf=sdnetutils.HTTP_GET(url,60)
    geodata=json.loads(buf)

    if len(geodata['results'])<1:
        raise SDException('SDNEARES-002','maps.googleapis.com error (response=%s,url=%s)'%(str(geodata),url))

    result=geodata['results'][0]
    location=result['geometry']['location']
    lat=location['lat']
    lng=location['lng']
    return (lat,lng)

def get_client_place():
    country=get_client_country()
    place=country_name_to_country_place(country)
    return place

def get_client_country():
    country=sdconfig.config.get('locale','country')

    # check
    if country == '':
        raise SDException('SDNEARES-001',"'country' is not set in configuration file")

    return country

def country_code_to_country_name(code):
    country=pycountry.countries.get(alpha_2=code)
    return country.name

