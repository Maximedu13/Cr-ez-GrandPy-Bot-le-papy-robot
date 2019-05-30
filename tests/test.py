"""unit tests"""
import unittest
from unittest.mock import patch
import re
from GrandPyBot.messages import Message
from GrandPyBot.apis import Wiki, GoogleMaps
from GrandPyBot.views import app

class FlaskBookshelfTests(unittest.TestCase):
    """TestFlaskApp"""
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index_by_default_url(self):
        """test /"""
        status = self.app.get('/')
        self.assertEqual(status.status_code, 200)

    def test_index_by_index_url(self):
        """test /index"""
        status = self.app.get('/index')
        self.assertEqual(status.status_code, 200)

    def test_fictive_url(self):
        """test /fictive"""
        status = self.app.get('/fictive')
        self.assertEqual(status.status_code, 404)

class InputAndParseTest(unittest.TestCase):
    """class InputAndParseTest"""
    maxDiff = None
    msg = Message()
    parse_msg = msg.parse_msg

    def test_le(self):
        """test article"""
        messages = "Openclassrooms"
        self.assertEqual(messages, self.parse_msg("Le Openclassrooms"))

    def test_empty(self):
        """test empty"""
        messages = ""
        self.assertEqual(messages, self.parse_msg(""))

    def test_stopword(self):
        """test stopwords"""
        messages = ""
        self.assertEqual(messages, self.parse_msg("ainsi ailleurs"))

    def test_msg_oc_1(self):
        """test openclassrooms 1"""
        messages = "Adresse Openclassrooms"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! \
        Est-ce que tu connais l'adresse d'OpenClassrooms ?"))

    def test_diacriticals(self):
        """test diacriticals"""
        messages = "Pyrénées"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! \
        Est-ce que tu connais les Pyrénées ?"))

    def test_city(self):
        """test panama city"""
        messages = "Panama (Ville)"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! Connais tu Panama ville ?"))

    def new_york(self):
        """test new york"""
        messages = "New York"
        self.assertEqual(messages, self.parse_msg("new york"))

class WikiApi(unittest.TestCase):
    """class WikiApi"""
    wiki = Wiki()
    msg = Message()
    address = msg.return_to_adress
    maxDiff = None

    def test_city(self):
        """test Bonifacio"""
        messages = "Bonifacio est une commune française située dans la circonscription \
        départementale de la Corse-du-Sud et le territoire de la collectivité de Corse. \
        Elle appartient à l'ancienne piève de Bonifacio dont elle était le chef-lieu. \
        Ses habitants sont les Bonifaciens et les Bonifaciennes."
        value = None
        for _, value in self.wiki.get_wiki_result("Bonifacio").items():
            pass
        regex = re.search("Bonifacio est une commune française située", value)
        if regex:
            print("YES! We have a match!")
        else:
            print("No match")

    def test_openclassrooms(self):
        """test Openclassrooms"""
        messages = "La cité Paradis est une voie publique située dans le 10e arrondissement de " + \
        "Paris."
        self.assertEqual(messages, self.wiki.get_wiki_result("Cité Paradis")["summary"])

    # no result from wikipedia api
    @patch('GrandPyBot.apis.wikipediaapi.Wikipedia.page')
    def test_fail(self, result):
        """test fail"""
        result.return_value = ""
        response = self.wiki.get_wiki_result("knldsskl")
        self.assertEqual(response, "no result")

    # result from wikipedia api
    @patch('GrandPyBot.apis.wikipediaapi.Wikipedia.page')
    def test_success(self, result):
        """test success"""
        class WikiPage():
            """creating a objet Page to return for wikipidia page mock"""
            def __init__(self):
                self.title = 'titre'
                self.summary = 'summary'

        result.return_value = WikiPage()
        response = self.wiki.get_wiki_result("Openclassrooms")

        self.assertEqual(response, {
            "title": "titre",
            "summary": "summary",
            })

class GoogleMapsApi(unittest.TestCase):
    """class GoogleMapsApi"""
    g_m = GoogleMaps()
    gm_result = g_m.get_position

    def test_openclassrooms(self):
        """test Openclassrooms"""
        messages = {'address': '7 Cité Paradis, 75010 Paris, France', 'latitude': 48.8748465, \
        'longitude': 2.3504873}
        self.assertEqual(messages, self.g_m.get_position("Openclassrooms"))

    # result from google maps
    @patch('GrandPyBot.apis.get')
    def test_valid_return(self, mock_api):
        """test result from google maps"""
        result = {
            "results" :[
                {
                    'formatted_address' : "Paris",
                    'geometry' :
                    {
                        'location' :
                        {
                            'lat' : 12.437,
                            'lng' : 23.9
                        }
                    }
                }
            ],
            "status" : 'OK'
        }
        mock_api.return_value.json.return_value = result
        response = self.g_m.get_position('Test')
        self.assertEqual(response, {
            "address": 'Paris',
            "latitude": 12.437,
            "longitude": 23.9
            })

    # no result from google maps
    @patch('GrandPyBot.apis.get')
    def test_error_return(self, mock_api):
        """test no result from google maps"""
        result = {
            "status" : 'Denied'
        }
        mock_api.return_value.json.return_value = result
        response = self.g_m.get_position('Test')
        self.assertEqual(response, "no result")

    @patch('GrandPyBot.apis.get')
    def test_city(self, result):
        """test Bonifacio"""
        mock_result = {"results": [{"geometry": {"location": \
            {"lat": 41.38717399999999, "lng": 9.159269}}, "formatted_address": \
            "Bonifacio, France"}]}
        result.return_value.json.return_value = mock_result
        properties = []
        for _, value in self.g_m.get_position("Bonifacio, France").items():
            properties.append(value)
        address, test_lat, test_long = properties[0], properties[1], properties[2]
        self.assertEqual(address, mock_result["results"][0]["formatted_address"])
        self.assertEqual(test_lat, mock_result["results"][0]["geometry"]["location"]["lat"])
        self.assertEqual(test_long, mock_result["results"][0]["geometry"]["location"]["lng"])

if __name__ == '__main__':
    unittest.main()
