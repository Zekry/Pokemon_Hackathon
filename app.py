import pickle
import numpy as np
import pandas as pd
import random
from flask import Flask, request, render_template
from jinja2 import Template

import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model/pipe.pkl', 'rb'))
df = pickle.load(open('model/poke.pkl', 'rb'))

global player_1
global player_1_name_html
global base

@app.route('/')
def index():
    #Goes to html
    global player_1
    global player_1_name_html
    global base

    player_1 = (random.choice(df['#']))
    player_1_name_html = df[df['#'] == player_1]['name'].values[0]
    base = "https://img.pokemondb.net/artwork/"

    player_1_img_url = base+df[df['#'] == player_1]['name'].values[0].lower()+'.jpg'
    players_2_options = (random.choices(df['name'],k=6))
    players_2_options

    player_2_url = []
    for i in players_2_options:
        player_2_img_url=base+i.lower()+'.jpg'
        player_2_url.append(player_2_img_url)
    player_2_url_name = list(zip(players_2_options,player_2_url))

    return render_template('pindex.html',player_1_name_html = player_1_name_html,player_1_img_url = player_1_img_url, player_2_url_name=player_2_url_name)

@app.route('/result', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        result = request.form

    #Dataframe contains names from the html page
    names = pd.DataFrame({
        'first_pokemon': player_1_name_html,
        'second_pokemon': [result['player_2']]
    })

    #This dataframe should have numbers ralated to the names from the page
    like_training = pd.DataFrame({
        'first_pokemon': [df[names['first_pokemon'][0] == df['name']]['#'].values[0]],
        'second_pokemon': [df[names['second_pokemon'][0] == df['name']]['#'].values[0]]
    })
    #Merg
    first = like_training.merge(df, how='left',left_on=['first_pokemon'], right_on = ['#'], suffixes=('_f', '_s'))
    second = first.merge(df, how='left',left_on=['second_pokemon'], right_on = ['#'],suffixes=('_f', '_s'))
    new=second.drop(['#_f', '#_s'], axis=1)

    prediction = model.predict(new)[0]
    prediction = int(prediction)
    winner = np.where(prediction == 1, new['name_s'].values[0], new['name_f'].values[0])
    url_winner = str(winner).lower()+'.jpg'
    url_winner=base+url_winner
    return render_template('result.html', winner = winner, url_winner = url_winner)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT =  4004
    app.run(HOST, PORT,debug = True)
