"""apis"""
import wikipediaapi
import requests
import json
import re
from requests import get

WIKI_WIKI = wikipediaapi.Wikipedia('fr')

class Wiki():
    """ wikipedia api """
    def __init__(self):
        pass

    @classmethod
    def get_wiki_result(cls, question):
        """ main method """
        try:
            wiki_page = WIKI_WIKI.page(question)
            # We want to get the history section
            txt = "Histoire"
            # The history section of Wikipedia is always followed by the section "Politics"
            end = 'Politique et administration'
            history_section = wiki_page.text\
            [wiki_page.text.index(txt) + len(txt):wiki_page.text.index(end)]

            

        except:
            return "no result"
        return wiki_page.title, wiki_page.summary, history_section

class GoogleMaps():
    """ google maps api """
    def __init__(self):
        self.key_api = "AIzaSyDEexokSoTAXo8lWdcuCF1ia1cw8m2fcRk"

    def get_position(self, question):
        """ main method """
        parameters = {
            'address': " ".join(question),
            'key': self.key_api,
            "language" : 'fr',
            "region" : "fr"
        }

        response = get('https://maps.googleapis.com/maps/api/geocode/json?',
                       params=parameters)

        data = response.json()
        try:
            address = data["results"][0]["formatted_address"]
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lng = data["results"][0]["geometry"]["location"]["lng"]
            info = {
                "address":  address,
                "latitude": lat,
                "longitude": lng
            }
            return info

        except:
            return "no result"

class Weather():
    """ https://openweathermap.org/api """
    def __init__(self):
        self.key_api = "3cf63bac22ea72262bb10f739247a998"

    def get_the_weather(self, question):
        req = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + question \
        + "&appid=" + self.key_api)
        result = json.loads(req.text)
        print(result)
        return result["weather"][0]["main"], round(result["main"]["temp"] - 273.15), \
        round(result["wind"]["speed"] * 3.6)
        
        