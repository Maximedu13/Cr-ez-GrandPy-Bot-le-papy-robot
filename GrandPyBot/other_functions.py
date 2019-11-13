"""other_functions.py"""
import urllib.request
import json
from flask import request, redirect, url_for, flash, Flask
from flask_mail import Mail
from flask_mail import Message as Msg

app = Flask(__name__)

app.config.update(dict(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 25,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'maxim95470@gmail.com',
        MAIL_PASSWORD = 'Maximcleveland1'
    ))
mail = Mail(app)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')

def get_geolocalisation():
    """ get geographical information"""
    try:
        with urllib.request.urlopen("https://geoip-db.com/json") as url:
            data = json.loads(url.read().decode())
            city, country, state = data['city'], data['country_name'], data['state']
    except:
        city = country = state = "?"
    return city, country, state

def send_mail(msg, stock_value_and_history):
    # send the email
    this_email = request.form['email']
    msg = Msg("GrandPyBotte", sender="maxim95470@gmail.com", recipients=[this_email])
    msg.body = 'Bonjour jeune homme ! Voici les informations que vous m‘avez demandées.' + \
    '\r\n\r\n' + stock_value_and_history[0] + '\r\n\r\n' + stock_value_and_history[1]
    mail.send(msg)
    # message flash success
    flash("Votre email a été envoyé", "success")
    """except:
        # message flash fail
        flash("Erreur", "warning")"""
