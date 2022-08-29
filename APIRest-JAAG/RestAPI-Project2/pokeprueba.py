import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')


#Creación de Base de datos con tablas Usuario y Pokemon_History
###########################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))

class Pokemon_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    pokemon_id = db.Column(db.Integer)
###########################################################################

# Variable global de tipo user.
actual_user_id = ""

#Ruta principal
@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

#Ruta para ingresar y agregar usuario
@app.route('/pokedex', methods=['POST'])
def add_user():

    global actual_user_id

    new_user = User(username = request.form['username'], email = request.form['email'])
    db.session.add(new_user)
    db.session.commit()

    actual_user_id = new_user.id

    info_pokemon = {}
    info_pokemon['id'] = ""
    info_pokemon['name'] = ""
    info_pokemon['height'] = ""
    info_pokemon['weight'] = ""
    info_pokemon['hp'] = ""
    info_pokemon['p_attack'] = ""
    info_pokemon['p_defense'] = ""
    info_pokemon['p_speed'] = ""
    info_pokemon['p_s_attack'] = ""
    info_pokemon['p_s_defense'] = ""
    info_pokemon['abilities'] = ""
    info_pokemon['type'] = ""
    info_pokemon['img'] = ""

    return render_template("index.html",data = info_pokemon)

#Ruta para ingresar datos asociados al recurso
@app.route('/pokedex/', methods=['POST'])
def show_pokemon():
    url = url='https://pokeapi.co/api/v2/pokemon/' + request.form['pokefound']
    res = requests.get(url)

    abilities = []
    type = []
    info_pokemon = {}
    info_pokemon['id'] = str(res.json()['id'])
    info_pokemon['name'] = str(res.json()['name']).upper()
    info_pokemon['height'] = str(res.json()['height']).upper()
    info_pokemon['weight'] = str(res.json()['weight']).upper()
    info_pokemon['hp'] = str(res.json()['stats'][0]['base_stat']).upper()
    info_pokemon['p_attack'] = str(res.json()['stats'][1]['base_stat']).upper()
    info_pokemon['p_defense'] = str(res.json()['stats'][2]['base_stat']).upper()
    info_pokemon['p_speed'] = str(res.json()['stats'][5]['base_stat']).upper()
    info_pokemon['p_s_attack'] = str(res.json()['stats'][3]['base_stat']).upper()
    info_pokemon['p_s_defense'] = str(res.json()['stats'][4]['base_stat']).upper()
    for i in range(len(res.json()['abilities'])):
        j = str(res.json()['abilities'][i]['ability']['name']).upper()
        abilities.append(j)
    info_pokemon['abilities'] = abilities
    for k in range(len(res.json()['types'])):
        l = str(res.json()['types'][k]['type']['name']).upper()
        type.append(l)
    info_pokemon['type'] = type
    info_pokemon['img'] = res.json()['sprites']['front_default']

    new_pokemon = Pokemon_History(user_id = actual_user_id, pokemon_id = info_pokemon['id'])
    db.session.add(new_pokemon)
    db.session.commit()

    return render_template("index.html",data=info_pokemon)

#Ruta de prueba de primera interfaz - Insomnia
@app.route('/insomnia/', methods=['GET'])
def home_ins():
    return render_template("home.html")

#Ruta de prueba de registro de usuario - Insomnia
@app.route('/insomnia/pokedex', methods=['POST'])
def post_ins():

    new_user = User(username = request.json['username'], email = request.json['email'])
    db.session.add(new_user)
    db.session.commit()

    info_pokemon = {}
    info_pokemon['id'] = ""
    info_pokemon['name'] = ""
    info_pokemon['height'] = ""
    info_pokemon['weight'] = ""
    info_pokemon['hp'] = ""
    info_pokemon['p_attack'] = ""
    info_pokemon['p_defense'] = ""
    info_pokemon['p_speed'] = ""
    info_pokemon['p_s_attack'] = ""
    info_pokemon['p_s_defense'] = ""
    info_pokemon['abilities'] = ""
    info_pokemon['type'] = ""
    info_pokemon['img'] = ""

    return render_template("index.html",data = info_pokemon)


@app.route('/insomnia/pokedex/', methods=['POST'])
def pokemon_ins():

    user_id=request.json['user_id']

    url = url='https://pokeapi.co/api/v2/pokemon/' + request.json['pokefound']
    res = requests.get(url)

    abilities = []
    type = []
    info_pokemon = {}
    info_pokemon['id'] = str(res.json()['id'])
    info_pokemon['name'] = str(res.json()['name']).upper()
    info_pokemon['height'] = str(res.json()['height']).upper()
    info_pokemon['weight'] = str(res.json()['weight']).upper()
    info_pokemon['hp'] = str(res.json()['stats'][0]['base_stat']).upper()
    info_pokemon['p_attack'] = str(res.json()['stats'][1]['base_stat']).upper()
    info_pokemon['p_defense'] = str(res.json()['stats'][2]['base_stat']).upper()
    info_pokemon['p_speed'] = str(res.json()['stats'][5]['base_stat']).upper()
    info_pokemon['p_s_attack'] = str(res.json()['stats'][3]['base_stat']).upper()
    info_pokemon['p_s_defense'] = str(res.json()['stats'][4]['base_stat']).upper()
    for i in range(len(res.json()['abilities'])):
        j = str(res.json()['abilities'][i]['ability']['name']).upper()
        abilities.append(j)
    info_pokemon['abilities'] = abilities
    for k in range(len(res.json()['types'])):
        l = str(res.json()['types'][k]['type']['name']).upper()
        type.append(l)
    info_pokemon['type'] = type
    info_pokemon['img'] = res.json()['sprites']['front_default']

    new_pokemon = Pokemon_History(user_id = user_id, pokemon_id = info_pokemon['id'])
    db.session.add(new_pokemon)
    db.session.commit()

    return render_template("index.html",data=info_pokemon)


if __name__ == '__main__':
    app.run(debug=True, port=8000)