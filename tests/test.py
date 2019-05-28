"""unit tests"""
import unittest
import re
from GrandPyBot.messages import Message
from GrandPyBot.apis import Wiki, GoogleMaps
from unittest.mock import MagicMock

mock = MagicMock()
print(mock.mock())

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
        for key, value in self.wiki.get_wiki_result("Bonifacio").items():
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

class GoogleMapsApi(unittest.TestCase):
    """class GoogleMapsApi"""
    g_m = GoogleMaps()
    gm_result = g_m.get_position

    def test_city(self):
        """test Bonifacio"""
        messages = {'address': 'Bonifacio, France', 'latitude': 41.38717399999999, \
        'longitude': 9.159269}
        self.assertEqual(messages, self.g_m.get_position("Bonifacio"))

    def test_openclassrooms(self):
        """test Openclassrooms"""
        messages = {'address': '7 Cité Paradis, 75010 Paris, France', 'latitude': 48.8748465, \
        'longitude': 2.3504873}
        self.assertEqual(messages, self.g_m.get_position("Openclassrooms"))

if __name__ == '__main__':
    unittest.main()
