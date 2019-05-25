"""parser"""
from GrandPyBot import stopword

class Message():
    """class message"""
    def __init__(self):
        self.grandpy_msg = [
            "Jeune homme, t'ai-je déjà raconté l'histoire de \n",
            "Je me souviens que ....\n",
            "Si tu as deux minutes , je peux te raconter la petite histoire de.. \n",
            "Est-ce que tu savais que....\n",
        ]

        self.grandpy_msg_fails = [
            "Ça ne me dit rien du tout jeune homme, désolé...",
            "Je zappe sur ce sujet, fais bien attention à l'orthographe dans la \
            barre de recherche..."
        ]

    def parse_msg(self, message):
        """main method"""
        list_word_input = []
        message = message.lower()
        message = message.replace("'", " ")
        for word in message.split(" "):
            list_word_input.append(word)
            if word in stopword.LIST_OF_STOP_WORDS or word in \
            stopword.LIST_OF_STOP_WORDS_PERSONALIZED:
                list_word_input.remove(word)
            if word in stopword.LIST_OF_SUPER_WORDS:
                list_word_input.remove(word)
                word = "(" + word + ")"
                list_word_input.append(word)
        for i in range(1):
            message = " ".join(list_word_input)
        message = message.lstrip()
        return message.title()

    def return_to_adress(self, message):
        """method to get the street if the address is numeric"""
        message = message[:message.find(",")]
        ret = ""
        for i in message:
            for j in i:
                if not j.isnumeric():
                    ret += j
        return ret
