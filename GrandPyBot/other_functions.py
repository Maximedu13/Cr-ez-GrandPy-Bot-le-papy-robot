"""other_functions.py"""
import urllib.request
import json
import requests
from flask import request, redirect, url_for, flash, Flask
from flask_mail import Mail
from flask_mail import Message as Msg
from urllib.parse import urlencode


def get_geolocalisation():
    """ get geographical information"""
    try:
        with urllib.request.urlopen("https://geoip-db.com/json") as url:
            data = json.loads(url.read().decode())
            city, country, state = data['city'], data['country_name'], data['state']
    except:
        city = country = state = "?"
    return city, country, state
