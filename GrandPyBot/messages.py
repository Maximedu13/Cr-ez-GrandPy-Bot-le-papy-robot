from GrandPyBot import stopword

class Message():
    def __init__(self):
        self.GrandPy_msg = [
        "Jeune homme, t'ai-je déjà raconté l'histoire de \n",
        "Je me souviens que ....\n",
        "Si tu as deux minutes , je peux te raconter la petite histoire de.. \n",
        "Est-ce que tu savais que....\n",
        ]

        self.GrandPy_msg_fails = [
        "Ça ne me dit rien du tout jeune homme, désolé...",
        "Je zappe sur ce sujet, fais bien attention à l'orthographe dans la barre de recherche..."
        ]

    def parse_msg(self, message):
        list_word_input = []
        message = message.lower()
        message = message.replace("'", " ")
        for word in message.split(" "):
            list_word_input.append(word)
            if word in stopword.list_of_stop_words or word in stopword.list_of_stop_words_personnalized:
                list_word_input.remove(word)
            if word in stopword.list_of_super_words:
                list_word_input.remove(word)
                word = "(" + word + ")"
                list_word_input.append(word)
        for i in range(1):
            message = " ".join(list_word_input)
        return message

    def parse_google_maps(self, message):
        list_word_input = []
        for word in message.split(" "):
            word = word.capitalize()
            list_word_input.append(word)
        for i in range(1):
            message = " ".join(list_word_input)
        message = message.replace(" ", "+")
        message.capitalize()
        return message