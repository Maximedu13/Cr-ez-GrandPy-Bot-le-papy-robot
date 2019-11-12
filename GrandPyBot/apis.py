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
    
    def get_history_section(question):
        try:
            wiki_page = WIKI_WIKI.page(question)
            try:
                # We want to get the history section
                txt = "Histoire"
                #History section of Wikipedia followed by the section Politics and administration
                end = 'Politique et administration'
                history_section = wiki_page.text[wiki_page.text.index(txt) + \
                len(txt):wiki_page.text.index(end)]
            except:
                try:
                    #History section of Wikipedia followed by the section "Administration"
                    end = 'Administration'
                    history_section = wiki_page.text[wiki_page.text.index(txt) + \
                    len(txt):wiki_page.text.index(end)]
                except:
                    try:
                        #History section of Wikipedia followed by the section "Urbanism"
                        end = 'Urbanisme'
                        history_section = wiki_page.text[wiki_page.text.index(txt) + \
                        len(txt):wiki_page.text.index(end)]
                    except:
                        history_section = "?"          
        except:
            history_section = "?"
        return history_section

    @classmethod
    def get_wiki_result(cls, question):
        """ main method """
        try:
            wiki_page = WIKI_WIKI.page(question)
            title = wiki_page.title
            summary = wiki_page.summary
            history_section = Wiki.get_history_section(question)
            history = history_section
        except:
            title = summary = history = "?"
        return title, summary, history

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
        try:
            req = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + question \
            + "&appid=" + self.key_api)
            result = json.loads(req.text)
            weather = result["weather"][0]["main"]
            temperature = round(result["main"]["temp"] - 273.15)
            wind = round(result["wind"]["speed"] * 3.6)
        except:
            weather = temperature = wind = "?"
        return weather, temperature, wind
        