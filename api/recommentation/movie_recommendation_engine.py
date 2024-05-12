# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:02:47 2024

@author: huiss
"""
import numpy as np
import pandas as pd
from pandas import DataFrame

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def compare_liste_mots_jaccard(mot_reference, liste_mots):
    mots_reference_set = set(mot_reference)
    similarities = {}
    for i in range(len(liste_mots)):
        mot_set = set(liste_mots[i].lower())
        similarity = jaccard_similarity(mots_reference_set, mot_set)
        similarities[liste_mots[i]] = similarity
    return similarities


def found_movie_from_name(df, movie):
    for idx, row in df.iterrows():

        if row['original_title'] == movie:
            print(df.iloc[idx])
            row_data = df.iloc[idx:idx + 1]
            return row_data
    print("Ecrire avec la bonne orthographe voir ci dessous")
    similarites_jaccard = compare_liste_mots_jaccard(movie.lower(), df['title'].fillna('').astype(str))
    title_tries = sorted(similarites_jaccard.items(), key=lambda x: x[1], reverse=True)[0:5]

    for mot, similarite in title_tries:
        print(mot)
    return pd.DataFrame


def add_rows(df, row_data):
    df = pd.concat([row_data, df])
    return df


def get_director(data_str):
    data_json = eval(data_str)
    for job in data_json:
        if [job['job'] == 'Director']:
            return job['name']

    return True


def get_name(data_str):
    data_json = eval(data_str)
    noms_acteurs = [acteur['name'] for acteur in data_json]
    return noms_acteurs


def get_movie_features(df: DataFrame) -> DataFrame:
    selected_columns = ['belongs_to_collection', 'original_title', 'genres', 'id', 'imdb_id', 'original_language',
                        'popularity',
                        'revenue', 'runtime', 'spoken_languages', 'vote_average',
                        'vote_count', 'overview', 'cast', 'crew', 'production_companies', 'release_date']

    # Sélectionner uniquement les colonnes spécifiées
    df = df[selected_columns]

    # Appliquer les transformations sur les colonnes 'cast' et 'crew'
    df['cast'] = df['cast'].apply(get_name)
    df['cast'] = df['cast'].apply(lambda x: ' '.join(x))
    df['crew'] = df['crew'].apply(get_director)
    df['crew'] = df['crew'].fillna('').astype(str)
    df['belongs_to_collection'] = df['belongs_to_collection'].fillna('').astype(str)
    df['production_companies'] = df['production_companies'].fillna('').astype(str)
    df['release_date'] = df['release_date'].fillna('').astype(str)

    # Remplacer les valeurs NaN dans les colonnes numériques par une chaîne vide ('')
    df['revenue'] = df['revenue'].fillna('').astype(str)
    df['runtime'] = df['runtime'].fillna('').astype(str)
    df['popularity'] = df['popularity'].fillna('').astype(str)
    df['genres'] = df['genres'].fillna('').astype(str)
    df['overview'] = df['overview'].fillna('').astype(str)
    df['original_title'] = df['original_title'].fillna('').astype(str)
    df['original_language'] = df['original_language'].fillna('').astype(str)

    # Convertir les colonnes numériques en chaînes de caractères pour éviter les erreurs de concaténation
    df['vote_count'] = df['vote_count'].astype(str)
    df['vote_average'] = df['vote_average'].astype(str)
    df['popularity'] = df['popularity'].fillna('').astype(str)

    # Convertir les valeurs booléennes en chaînes de caractères
    df['spoken_languages'] = df['spoken_languages'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

    # Prendre seulement les 500 premières lignes

    # Concaténation des données textuelles pour former un seul champ texte
    df['combined_features'] = df['original_title'] + ' ' + \
                              df['genres'] + ' ' + \
                              df['original_language'] + ' ' + \
                              df['overview'] + ' ' + \
                              df['cast'] + ' ' + \
                              df['crew'] + ' ' + \
                              df['vote_count'] + ' ' + \
                              df['vote_average'] + ' ' + \
                              df['popularity'] + ' ' + \
                              df['spoken_languages'] + ' ' + \
                              df['belongs_to_collection'] + ' ' + \
                              df['production_companies'] + ' ' + \
                              df['release_date']

    df['combined_features'].fillna('', inplace=True)
    return df['combined_features']


def find_index_movie(df, movie):
    index = df['original_title'] == movie.index[0]
    return index


def find_near_movies(df_combined: DataFrame, nombre_film: int):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df_combined)

    # Calcul de la similarité cosinus entre les films
    cosine_sim = cosine_similarity(count_matrix)
    similar_movies = []
    for i in range(0, nombre_film):
        similar_movies += sorted(list(enumerate(cosine_sim[i])), key=lambda x: x[1], reverse=True)[1:11]

    return similar_movies


def sort_users_near_userid(ratings_matrix, user_id):
    user_ratings = ratings_matrix.loc[user_id]
    user_ratings_nonzero = user_ratings[user_ratings != 0]
    nbre_movie_rate = len(user_ratings_nonzero)
    ratings_matrix_nonzero = ratings_matrix[user_ratings_nonzero.index]
    list_user_score = []
    for user in range(0, len(ratings_matrix_nonzero)):
        score = 0
        index = 0
        number_movie_similar = 0
        if not user == user_id:
            for rating in ratings_matrix_nonzero.iloc[user]:
                if rating != 0.0:
                    print(user_ratings_nonzero.iloc[index], type(user_ratings_nonzero.iloc[index]))
                    score += np.abs(rating - float(user_ratings_nonzero.iloc[index]))
                    number_movie_similar += 1

                index += 1
            if not number_movie_similar == 0:
                list_user_score.append([user, score, number_movie_similar])
            list_user_score_sort = sorted(list_user_score, key=lambda x: x[2], reverse=True)
            list_user_score_sort = sorted(list_user_score_sort, key=lambda x: x[1])

    return list_user_score_sort, nbre_movie_rate


def take_rating(ratings_matrix, list_user_score, movie_id, k, nbr_movie_rate):
    if not str(movie_id) in ratings_matrix.columns:
        return 0, 0
    else:
        predicted_rating = []
        number_iteration = 0
        print(number_iteration, len(predicted_rating))
        print(list_user_score)
        while (number_iteration < k or len(predicted_rating) == 0) and number_iteration < len(list_user_score) - 1:

            user_id = int(list_user_score[number_iteration][0])
            similar_users_ratings = ratings_matrix.loc[user_id, str(movie_id)]

            if similar_users_ratings != 0 and (
                    list_user_score[number_iteration][2] >= (nbr_movie_rate) // 2 or list_user_score[number_iteration][
                2] >= 5):
                predicted_rating.append(similar_users_ratings)
            number_iteration += 1

        if (len(predicted_rating) != 0):
            predicted_rating = sum(predicted_rating) / len(predicted_rating)
        else:
            predicted_rating = 0
        return predicted_rating, number_iteration


def predict_without_cos(data, user_id, id_movie, near_user):
    sort, nbr_movie_rate = sort_users_near_userid(data, user_id)
    print(sort, nbr_movie_rate)
    predicted_rating, near_user_end = take_rating(data, sort, id_movie, near_user, nbr_movie_rate)
    return predicted_rating, near_user_end
