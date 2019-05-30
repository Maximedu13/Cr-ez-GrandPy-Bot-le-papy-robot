"""views.py"""
import random
from flask import Flask, request, render_template
from GrandPyBot.apis import Wiki, GoogleMaps
from GrandPyBot.messages import Message

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/search', methods=['POST'])
def search():
    """launch a search"""
    question = request.form['search']
    wiki = Wiki()
    message = Message()
    grd_py_msg = message.grandpy_msg
    msg_fails = message.grandpy_msg_fails
    the_question = message.parse_msg(question)
    g_m = GoogleMaps()
    g_m.get_position(the_question)
    list_values = []

    # If google maps api returns something not null
    try:
        for key, value in g_m.get_position(the_question).items():
            list_values.append(value)
        return_to_adress = message.return_to_adress(str(list_values[0]))

    # If google maps api returns something null
    except AttributeError:
        return "<b>" + "Vous m‘avez posé comme question : " + \
            request.form['search'] + "</b>" + "<br/>" + "<em>" + (random.choice(msg_fails)) \
            + "</em>" + "<script>$('#map').hide();</script>"

    # If media wiki api returns something not null
    try:
        for key, value in wiki.get_wiki_result(the_question).items():
            pass

    # If media wiki api returns something null
    except KeyError:
        return "<b>" + "Vous m‘avez posé comme question : " + \
            request.form['search'] + "</b>" + "<br/>" + "<em>" + (random.choice(msg_fails)) \
            + return_to_adress + "</em>"

    # If it returns a right information from media wiki and google maps
    if value and g_m.get_position(the_question) != "no result":
        return "<script>initMap(" + str(list_values[1]) + ',' + str(list_values[2]) + ',' + \
            "'" + the_question + "'" +");display_map(); </script>" + "<b>" + \
            "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>" \
            + "<em>" + (random.choice(grd_py_msg)) + "</em>" + value +  "<br/>"

    # If it returns no information from media wiki, only from google maps (address)
    elif not value and return_to_adress:
        return_to_adress = return_to_adress.replace("Av.", "Avenue")
        return "<script>initMap(" + str(list_values[1]) + ',' + str(list_values[2]) + ',' + \
            "'" + the_question + "'" +");display_map(); </script>" + "<b>" + \
            "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>" \
            + "<em>" + (random.choice(grd_py_msg)) + "</em>" + \
            wiki.get_wiki_result(return_to_adress)["summary"] + "<br/>"

    # If it returns no information from media wiki, and none from google maps.
    else:
        return "<b>" + "Vous m‘avez posé comme question : " + request.form['search'] + \
            "</b>" + "<br/>" + "<em>" + (random.choice(msg_fails)) + question + "</em>"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """index"""
    return render_template('startbootstrap/index.html')

if __name__ == "__main__":
    app.run()
