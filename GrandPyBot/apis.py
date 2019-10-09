"""apis"""
import wikipediaapi
import requests
import json
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
            #print(wiki_page.sections)
            return {
                "title": wiki_page.title,
                "summary": wiki_page.summary,
            }

        except:
            return "no result"

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
        return result["weather"][0]["main"], round(result["main"]["temp"] - 273.15)
        