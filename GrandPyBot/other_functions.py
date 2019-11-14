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

def send_mail(msg, stock_value_and_history):
    # send the email
    try:
        this_email = request.form['email']
        msg = Msg("GrandPyBotte", sender="maxim95470@gmail.com", recipients=[this_email])
        msg.body = 'Bonjour jeune homme ! Voici les informations que vous m‘avez demandées.' + \
        '\r\n\r\n' + stock_value_and_history[0] + '\r\n\r\n' + stock_value_and_history[1]
        mail.send(msg)
        # message flash success
        flash("Votre email a été envoyé", "success")
    except:
        # message flash fail
        flash("Erreur", "warning")

"""
def send_a_mail(to_address, from_address, subject, plaintext, html):
    this_email = request.form['email']
    "https://api.mailgun.net/v3/sandbox6247218655a94010b9840c23c2688fc7.mailgun.org/messages",
        auth=("api", "key-********"),
        data={"from": "Excited User <bb@gmail.com>",
              "to": ["bb@outlook.com", "bb4@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})
    r = requests.\
        post("https://api.mailgun.net/v2/%s/messages" % app.config['MAILGUN_DOMAIN'],
            auth=("api", app.config['MAILGUN_KEY']),
             data={
                 "from": from_address,
                 "to": to_address,
                 "subject": subject,
                 "text": plaintext,
                 "html": html
             }
         )
    print(r)
    return r"""

"""def send_simple_message():
    r = requests.post("https://api.mailgun.net/v3/sandbox1e01da76c20f44f8b45c7c01d2c34431.mailgun.org/messages",
		auth=("api", "99b4bc222660bfe5cd379fc42721c17a-1df6ec32-48122113"),
		data={"from": "Excited User <app131594032@heroku.com>",
			"to": ["app131594032@heroku.com", "maxim95470@gmail.com"],
			"subject": "KSNDSKLDKNDLASLNKDSANKL",
			"text": "Testing some Mailgun awesomness!"})
    print(r)
    return r

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