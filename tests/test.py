import unittest
import sys
from GrandPyBot.messages import Message
from GrandPyBot import stopword
from GrandPyBot.apis import Wiki, GoogleMaps

class Input_and_Parse_Test(unittest.TestCase):
    msg = Message()
    parse_msg = msg.parse_msg

    def test_le(self):
        messages = "openclassrooms"
        self.assertEqual(messages, self.parse_msg("Le Openclassrooms"))

    def test_empty(self):
        messages = ""
        self.assertEqual(messages, self.parse_msg(""))
    
    def test_stopword(self):
        messages = ""
        self.assertEqual(messages, self.parse_msg("ainsi ailleurs"))
    
    def test_msg_oc_1(self):
        messages = "adresse openclassrooms"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"))

    def test_diacritics(self):
        messages = "pyrénées"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! Est-ce que tu connais les Pyrénées ?"))
    
    def test_city(self):
        messages = "panama (ville)"
        self.assertEqual(messages, self.parse_msg("Salut GrandPy ! Connais tu Panama ville ?"))

class Wiki_Api(unittest.TestCase):
    wiki = Wiki()
    wiki_result = wiki.get_wiki_result

    def test_city(self):
        messages = "Paris"
        for key, value in self.wiki_result("Paris").items():
            pass
        self.assertEqual(messages, value)

class Google_Maps(unittest.TestCase):
    msg = Message()
    parse_gmaps = msg.parse_google_maps

    def test_streer(self):
        messages = "Rue+Chateaubriand"
        self.assertEqual(messages, self.parse_gmaps("rue chateaubriand"))

if __name__ == '__main__': 
    unittest.main()