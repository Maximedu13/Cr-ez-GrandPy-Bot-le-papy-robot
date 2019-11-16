"""unit tests"""
import unittest
from unittest.mock import patch
from flask_mail import Mail, BadHeaderError, Message as Msg
from GrandPyBot.messages import Message
from GrandPyBot.apis import Wiki, GoogleMaps, Weather
from GrandPyBot.views import app
from GrandPyBot.other_functions import get_geolocalisation
from flask import Flask

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

    def test_contact_url(self):
        """test /contact"""
        status = self.app.get('/contact')
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

    def setUp(self):
        self.title = "Bonifacio"
        self.summary = "Bonifacio est une commune française située dans la circonscription départementale de la Corse-du-Sud et le territoire de la collectivité de Corse. Elle appartient à l'ancienne piève de Bonifacio dont elle était le chef-lieu."
        self.history = ""

    def test_openclassrooms(self):
        """test Openclassrooms"""
        messages = "La cité Paradis est une voie publique située dans le 10e arrondissement de " + \
        "Paris."
        title, summary, history_section = self.wiki.get_wiki_result("Cité Paradis")
        self.assertEqual(messages, summary)

    # no result from wikipedia api
    @patch('GrandPyBot.apis.wikipediaapi.Wikipedia.page')
    def test_fail(self, result):
        """test fail"""
        result.return_value = ""
        title, summary, history_section = self.wiki.get_wiki_result("knldsskl")
        self.assertEqual(summary, "?")

    # result from wikipedia api
    @patch('GrandPyBot.apis.get')
    def test_success(self, result):
        """test success"""
        result.return_value = ''
        title, summary, history_section = self.wiki.get_wiki_result("Bonifacio")
        self.assertEqual(title, self.title)
        self.assertEqual(self.summary, summary)
        self.assertNotEqual(self.history, history_section)

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

class TheWeather(unittest.TestCase):
    """class Weather"""
    instance = Weather()
    @patch('GrandPyBot.apis.get')
    def test_cloud(self, mock_api):
        """test cloud"""
        cloud, temperature, wind = self.instance.get_the_weather('Lattes')
        self.assertIn(cloud, ('Clouds', 'Sun', 'Rain', 'Clear', 'Drizzle', \
        'Dust', 'Mist', 'Haze', 'Fog', 'Snow', 'Storm', 'Thunderstorm'))
        self.assertTrue(-10 <= temperature <= 50)
        self.assertTrue(0 <= wind <= 150)

class HistorySection(unittest.TestCase):
    """class HistorySection"""
    wiki = Wiki()
    def setUp(self):
        self.history = "Histoire \
        Pas d'histoire \
        Politique et administration "

    def test_fail(self):
        test = Wiki.get_history_section(self.history)
        self.assertEqual(test, "?")

    @patch('GrandPyBot.apis.get')
    def test_paris(self, mock_api):
        paris = Wiki.get_history_section("Paris")
        self.assertTrue(paris)
        self.assertNotEqual(paris, "")

    @patch('GrandPyBot.apis.get')
    def test_birmingham(self, mock_api):
        uk = Wiki.get_history_section("Birmingham")
        self.assertTrue(uk)
        self.assertNotEqual(uk, "")

    @patch('GrandPyBot.apis.get')
    def test_moscou(self, mock_api):
        moscou = Wiki.get_history_section("moscou")
        self.assertTrue(moscou)
        self.assertNotEqual(moscou, "")

class Geolocalisation(unittest.TestCase):
    """class Geolocalisation"""
    def setUp(self):
        self.result = get_geolocalisation()
    
    def test_tuple_result(self):
        self.assertEqual(len(get_geolocalisation()), 3)
    
    def test_not_empty(self):
        self.assertNotEqual(get_geolocalisation()[0], None)
        self.assertNotEqual(get_geolocalisation()[0], "")
        self.assertNotEqual(get_geolocalisation()[1], None)
        self.assertNotEqual(get_geolocalisation()[1], "")
        self.assertNotEqual(get_geolocalisation()[2], None)
        self.assertNotEqual(get_geolocalisation()[2], "")
    """
    def test_my_house_in_lattes(self):
        self.assertEqual(get_geolocalisation()[0], 'Lattes')
        self.assertEqual(get_geolocalisation()[1], 'France')
        self.assertEqual(get_geolocalisation()[2], 'Hérault')
    """

class SendEmail(unittest.TestCase):
    """SendEmail"""
    def setUp(self):
        TESTING = True
        self.app = Flask(__name__)
        self.app.config.update(dict(
            DEBUG = True,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 587,
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False,
            MAIL_USERNAME = 'maxim95470@gmail.com',
            MAIL_PASSWORD = ''
        ))
        self.app.config.from_object(self)
        self.mail = Mail(self.app)
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.subject = "testing"
        self.body= "testing"
        self.sender = "from@example.com"
        self.recipients = ["to@example.com"]

    def test_bad_header_subject(self):
        msg = Msg(subject="testing\r\n",
                  sender=self.sender,
                  body=self.body,
                  recipients=self.recipients)
        self.assertRaises(BadHeaderError, self.mail.send, msg)

    def test_send_without_recipients(self):
        msg = Msg(subject=self.subject,
                  recipients=self.recipients,
                  body=self.body)
        self.assertRaises(AssertionError, self.mail.send, msg)

    def test_multiline_subject(self):
        msg = Msg(subject=self.subject,
                  sender=self.sender,
                  body=self.body,
                  recipients=self.recipients)
        self.assertIn("From: " + self.sender, str(msg))
        self.assertIn(self.recipients[0], str(msg))
        self.assertIn(self.subject, str(msg))

if __name__ == '__main__':
    unittest.main()
