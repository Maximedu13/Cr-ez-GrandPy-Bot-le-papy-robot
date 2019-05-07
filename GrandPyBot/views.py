from flask import Flask, request, render_template
from datetime import date
import cgi, cgitb
import json
import random
from GrandPyBot.apis import Wiki, GoogleMaps
from GrandPyBot.messages import Message

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/search', methods=['POST'])
def search():
    question = request.form['search']
    wiki=Wiki()
    message = Message()
    GrdPy_msg=message.GrandPy_msg
    msg_fails=message.GrandPy_msg_fails
    the_question = message.parse_msg(question)
    google_maps_question = message.parse_google_maps(the_question)
    gm = GoogleMaps()
    gm.get_position(the_question)
    print(gm.get_position(the_question))
    list_values = []
    for key,value in gm.get_position(the_question).items():
        list_values.append(value)
    print(the_question)
    print(google_maps_question)
    print(list_values[1], list_values[2])
    print("https://www.google.com/maps/place/" + google_maps_question + str('/') +  str(list_values[1]) + str(",") + str(list_values[2])) 
    try:
        for key, value in wiki.get_wiki_result(the_question).items():
            pass
    except KeyError:
        return "<b>" + "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>"  \
        + "<em>" + (random.choice(msg_fails)) + question + "</em>"
   
    if value:
        return "<script>initMap(" + str(list_values[1]) + ',' + str(list_values[2]) + ',' + "'" + google_maps_question + "'" +");display_map(); </script>" + "<b>" + "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>" \
        + "<em>" + (random.choice(GrdPy_msg)) + "</em>" + value +  "<br/>" 
        
    else:
        return "<b>" + "Vous m‘avez posé comme question : " + request.form['search'] + "</b>" + "<br/>"  \
            + "<em>" + (random.choice(msg_fails)) + question + "</em>" + \
            '<div style="width: 700px;position: relative;"><iframe width="700" height="440" src="https://maps.google.com/maps?width=700&amp;height=440&amp;hl=en&amp;q=' + google_maps_question + '&amp;ie=UTF8&amp;t=&amp;z=10&amp;iwloc=B&amp;output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><div style="position: absolute;width: 80%;bottom: 10px;left: 0;right: 0;margin-left: auto;margin-right: auto;color: #000;text-align: center;"><small style="line-height: 1.8;font-size: 2px;background: #fff;">Powered by <a href="http://www.googlemapsgenerator.com/da/">Googlemapsgenerator.com/da/</a> & <a href="https://opwaarderenlebara.nl/netwerkbereik-lebara-nl/">https://opwaarderenlebara.nl/netwerkbereik-lebara-nl/</a></small></div><style>#gmap_canvas img{max-width:none!important;background:none!important}</style></div><br />'       
              

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('startbootstrap/index.html')

if __name__ == "__main__":
        app.run()