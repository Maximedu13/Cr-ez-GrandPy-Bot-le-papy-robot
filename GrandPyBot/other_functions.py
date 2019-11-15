"""other_functions.py"""
import urllib.request
import json
import requests
from flask import request, redirect, url_for, flash, Flask
from flask_mail import Mail
from flask_mail import Message as Msg
from urllib.parse import urlencode

app = Flask(__name__)
app.config['MAILGUN_KEY'] = '99b4bc222660bfe5cd379fc42721c17a-1df6ec32-48122113'
app.config['MAILGUN_DOMAIN'] = 'sandbox1e01da76c20f44f8b45c7c01d2c34431.mailgun.org'
"""app.config.update(dict(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'maxim95470@gmail.com',
        MAIL_PASSWORD = 'Maximcleveland1'
    ))
mail = Mail(app)"""
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



def send_simple_message(this_email, stock_value_and_history):
    msg = Msg(
          'GrandPyBotte',
    sender = 'maxim95470@gmail.com',
    recipients = [this_email])
    msg.html = '<b>Bonjour jeune homme, voici les informations que vous m‘avez demandées. </b>' + \
    '<br/>'*2 + stock_value_and_history[0] + '<br/>'*3 + stock_value_and_history[1]
    with app.app_context():
        mail.send(msg)
    flash("Votre email a été envoyé", "success")

"""
def send_simple_message(recipient):
    http = httplib2.Http()
    http.add_credentials('api', '99b4bc222660bfe5cd379fc42721c17a-1df6ec32-48122113')

    url = 'https://api.mailgun.net/v3/{}/messages'.format('sandbox1e01da76c20f44f8b45c7c01d2c34431.mailgun.org')
    data = {
        'from': 'Example Sender <mailgun@{}>'.format('sandbox1e01da76c20f44f8b45c7c01d2c34431.mailgun.org'),
        'to': recipient,
        'subject': 'This is an example email from Mailgun',
        'text': 'Test message from Mailgun'
    }

    resp, content = http.request(
        url, 'POST', urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))"""