"""views.py"""
import random
import urllib.request
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message as Msg
from GrandPyBot.apis import Wiki, GoogleMaps, Weather
from GrandPyBot.messages import Message
from GrandPyBot.other_functions import get_geolocalisation, send_simple_message

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'maxim95470@gmail.com',
    MAIL_PASSWORD = 'Maximcleveland1',
))

mail = Mail(app)
app.config.from_object('config')

@app.route('/search', methods=['POST'])
def search():
    """launch a search"""
    # instanciation
    wiki, message, weather, g_m = Wiki(), Message(), Weather(), GoogleMaps()
    question = request.form['search']
    grd_py_msg, msg_fails, the_question = message.grandpy_msg, message.grandpy_msg_fails, message.parse_msg(question)
    g_m.get_position(the_question)
    list_values = []
    the_weather, degrees, wind = weather.get_the_weather(the_question)
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
            "<br/>" + wiki.get_wiki_result(return_to_adress)[0] + "<br/>" + wiki.get_wiki_result(return_to_adress)[1]

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
    # Recup geolocalisation
    city, country, state = get_geolocalisation()
    if request.method == "POST" and stock_value_and_history:
        #if post request
        this_email = request.form['email']
        try: 
            send_simple_message(this_email, stock_value_and_history)
            return redirect(url_for('index'))
        except:
            flash("Hum. Il semble qu'il y ait eu une erreur.", "error")
            return redirect(url_for('index'))
    return render_template('startbootstrap/contact.html', city=city, country=country, state=state)

if __name__ == "__main__":
    app.run()
