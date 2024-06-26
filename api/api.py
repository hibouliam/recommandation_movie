import warnings

import numpy as np
import pandas as pd
from flask import Flask, jsonify,request
from flask_cors import CORS

from data_reader import get_links, get_data, get_matrix, get_credits
from recommentation.link import generate_user_recommendations
from recommentation.movie_recommendation_engine import compare_liste_mots_jaccard,modify_row_matrix, add_row_matrix
from recommentation.movie_recommendation_engine import get_name, get_name_director

links = get_links()
data = get_data()
matrix = get_matrix()
credits = get_credits()


warnings.filterwarnings('ignore')

id_user = len(matrix)
matrix = add_row_matrix(matrix, id_user)

app = Flask(__name__)
CORS(app)


@app.route('/found_movie_title', methods=['POST'])
def found_movie_title():
    title_entry = request.get_json()
    mots = []
    print(title_entry)
    parametre = title_entry['parametre']
    similarites_jaccard = compare_liste_mots_jaccard(parametre.lower(), data['original_title'].fillna('').astype(str))
    title_tries = sorted(similarites_jaccard.items(), key=lambda x: x[1], reverse=True)[0:5]
    for mot, similarite in title_tries:
        mots.append(mot)
    return jsonify({"resultat": mots})


@app.route('/add_note_in_matrix', methods=['POST'])
def add_note_in_matrix():
    global matrix, links, data
    donnee = request.get_json()

    movie_row = data.loc[data['title'] == donnee['title']]
    note_user = float(donnee['rating'])
    moviesid = int(movie_row['movieId'])
    matrix = modify_row_matrix(matrix, id_user, moviesid, note_user)
    films = [{"titre": "coucou", "overview": "pierre"}, {"titre": "Hello", "overview": "mon gros"}]

    return jsonify({'message': films})


@app.route('/print_all_recommandation_movie', methods=['GET'])
def print_all_recommandation_movie():
    global matrix, links, data, id_user
    list_movie = generate_user_recommendations(data, matrix, id_user)
    films_recommande = []
    for movie in list_movie:
        id_imdb = movie[3]['movieId'].values[0]

        if (str(id_imdb) in matrix.columns and movie[1] >= 4.0 and movie[2] < 50 and matrix.loc[
            id_user, str(id_imdb)] == 0):
            title = movie[3]['title'].values[0]
            overview = movie[3]['overview'].values[0]
            cast = get_name(movie[3]['cast'].values[0])
            crew = get_name_director(movie[3]['crew'].values[0])
            genre = get_name(movie[3]['genres'].values[0])
            date = movie[3]['release_date'].values[0]
            poster = movie[3]['poster_path'].values[0]

            films_recommande.append(
                {"titre": title, "overview": overview, "acteur": cast, "realisateur": crew, "genres": genre,
                 "date": date, "poster": poster})

    return jsonify({'message': films_recommande})


if __name__ == '__main__':
    app.run(debug=True)
