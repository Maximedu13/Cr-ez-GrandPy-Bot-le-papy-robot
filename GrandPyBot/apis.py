import wikipediaapi
from requests import get

wiki_wiki = wikipediaapi.Wikipedia('fr')


class Wiki():
    def __init__(self):
        #wiki_wiki.set_api_url("https://fr.wikipedia.org/w/api.php")
        pass
    def get_wiki_result(self, question):
        try:
            wiki_page = wiki_wiki.page(question)
            
            return {
                "title": wiki_page.title,
                "summary": wiki_page.summary
            }

        except IndexError:
            return "no result"

class GoogleMaps():
    def __init__(self):
        self.key_api = "AIzaSyAvKqgiwO0HqqCVxdRgeiJG8yXbM9k4UhU"
    
    def get_position(self, question):
        parameters = {
        'address': " ".join(question),
        'key': self.key_api
        }

        response = get('https://maps.googleapis.com/maps/api/geocode/json',
        params=parameters)

        data = response.json()
        try:
            address = data["results"][0]["formatted_address"]
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lng = data["results"][0]["geometry"]["location"]["lng"]
            global info
            info = {
                "address":  address,
                "latitude": lat,
                "longitude": lng
            }
            print(info["latitude"])
            return info

        except IndexError:
            return "no result"