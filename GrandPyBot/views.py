from flask import Flask, request, render_template
from datetime import date

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/afficher')
@app.route('/afficher/mon_nom_est_<nom>_et_mon_prenom_<prenom>')
def afficher(nom=None, prenom=None):
    if nom is None or prenom is None:
        return "Entrez votre nom et votre prénom comme il le faut dans l'url"
    return "Vous vous appelez {} {} !".format(prenom, nom)


@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.data.decode('utf-8')
    print(request.data)
    return render_template('startbootstrap/index.html')
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('startbootstrap/index.html')

if __name__ == "__main__":
        app.run()