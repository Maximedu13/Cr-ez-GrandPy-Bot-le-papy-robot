"""views.py"""
import random
from flask import Flask, request, render_template
from flask_mail import Mail, Message
from GrandPyBot.apis import Wiki, GoogleMaps, Weather
from GrandPyBot.messages import Message
import os

app = Flask(__name__)
mail = Mail(app)
mail_settings = {
    "MAIL_SERVER": 'localhost',
    "MAIL_PORT": 25,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": None, #os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": None #os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)
print(mail)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/search', methods=['POST'])
def search():
    """launch a search"""
    # instanciation
    wiki, message, weather, g_m = Wiki(), Message(), Weather(), GoogleMaps()

    question = request.form['search']
   
    grd_py_msg = message.grandpy_msg
    msg_fails = message.grandpy_msg_fails
    the_question = message.parse_msg(question)
    
    g_m.get_position(the_question)
    list_values = []
    
    the_weather, degrees = weather.get_the_weather(the_question)
    print(the_weather)
    print(degrees)
    this_image = "../static/images/" + the_weather + ".svg"
    print(this_image)
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
            "'" + the_question + "'" +");display_map(); </script>" + "<b>"  + \
            "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>" + \
            "<img src="+ this_image + "/>" + \
            "<br/>" + "<b>" + str(degrees) + "</b>" + "°C" +"<br/>" \
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
