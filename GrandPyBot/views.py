"""views.py"""
import random
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail
from flask_mail import Message as Msg
from GrandPyBot.apis import Wiki, GoogleMaps, Weather
from GrandPyBot.messages import Message
import urllib.request
import json
import os



app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'maxim95470@gmail.com',
    MAIL_PASSWORD = 'Maximcleveland1'
))

mail = Mail(app)

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
    
    the_weather, degrees, wind = weather.get_the_weather(the_question)
    print(the_weather)
    this_image = "../static/images/" + the_weather + ".svg"
    icon_temperature = "../static/images/119085.svg"
    icon_wind = "../static/images/2151268.svg"
    
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
    global stock_value_and_history
    stock_value_and_history = []
    try:
        key, value, history = wiki.get_wiki_result(the_question)
        stock_value_and_history.append(value)
        stock_value_and_history.append(history)

    # If media wiki api returns something null
    except:
        return "<b>" + "Vous m‘avez posé comme question : " + \
            request.form['search'] + "</b>" + "<br/>" + "<em>" + (random.choice(msg_fails)) \
            + return_to_adress + "</em>"
            
    
    # If it returns a right information from media wiki and google maps
    if value and g_m.get_position(the_question) != "no result":
        the_text = "<script>initMap(" + str(list_values[1]) + ',' + str(list_values[2]) + ',' + \
            "'" + the_question + "'" +");display_map(); </script>" + "<b>"  + \
            "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>" + \
            "<img src="+ this_image + " class='weather' />" + \
            "<br/>" + "<img src="+ icon_temperature + " class='icons'/>" + "<b>" + str(degrees) + "</b>" + "°C" + \
            "<img src="+ icon_wind + " class='icons'/>" + "<b>" + " " +str(wind) + "</b>" + " km/h" + "<br/>" \
            + "<em>" + (random.choice(grd_py_msg)) + "</em>" + value + \
            "<br/>"*2 + "<b>" +"HISTOIRE DE " +  the_question + "</b>" + "<br/>" + history + "<br/>"
        return the_text

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

@app.route('/contact', methods=['POST', 'GET'])
def send_e_mail():
    """contact"""

    try:
        with urllib.request.urlopen("https://geoip-db.com/json") as url:
            data = json.loads(url.read().decode())
            city = data['city']
            country = data['country_name']
            state = data['state']
    except:
        result = " adresse introuvable. "

    if request.method == "POST":
        this_email = request.form['email']
        try:
            msg = Msg("GrandPyBotte",
                    sender="maxim95470@gmail.com",
                    recipients=[this_email])
            msg.body = 'Bonjour jeune homme ! Voici les informations que vous m‘avez demandées.' + \
            '\r\n\r\n' + stock_value_and_history[0] + '\r\n\r\n' + stock_value_and_history[1]
            mail.send(msg)
            flash("Votre email a été envoyé", "success")
            return redirect(url_for('index'))
        except:
            flash("Erreur.", "warning")
            return redirect(url_for('index'))

    return render_template('startbootstrap/contact.html', city=city, country=country, state=state)

if __name__ == "__main__":
    app.run()
