# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:23:02 2024

@author: huiss
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


# Diviser l'ensemble de données en lots et traiter chaque lot séparément
def create_rating_matrix(rating: DataFrame, start: int, total_rows: int, batch_size: int) -> DataFrame:
    z = 0
    ratings_matrices = []
    for i in range(start, total_rows, batch_size):
        # Sélectionner un batch de données
        batch_data = rating.iloc[i:i + batch_size]
        # Créer la matrice de notation pour ce lot
        ratings_matrix_batch = batch_data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        # Ajouter la matrice de notation à la liste de résultats
        ratings_matrices.append(ratings_matrix_batch)
        z += 1

    # Concaténer les matrices de notation de tous les lots en une seule
    ratings_matrix = pd.concat(ratings_matrices)
    ratings_matrix = ratings_matrix.fillna(0)
    ratings_matrix.to_csv(r'matrix_test.csv', index=False)
    return ratings_matrix


def add_row_matrix(matrix: DataFrame, user: int) -> DataFrame:
    new_row = pd.DataFrame({'1': [0.0]}, index=[user])
    df = pd.concat([matrix, new_row])
    df = df.fillna(0)
    return df


def modify_row_matrix(matrix, user, id_film, note):
    matrix.loc[int(user), str(int(id_film))] = note
    return matrix



# Fonction pour prédire les notes
def predict(ratings_matrix, user_id, item_id, k):
    user_ratings = ratings_matrix.loc[user_id]
    user_ratings_nonzero = user_ratings[user_ratings != 0]
    ratings_matrix_nonzero = ratings_matrix[user_ratings_nonzero.index]
    donnees = {'1': [100.0]}
    df = pd.DataFrame(donnees)

    user_similarities = cosine_similarity([user_ratings_nonzero], normalize(ratings_matrix_nonzero))[0]
    similar_users_indices = np.argsort(user_similarities)[::-1][1:k + 1]

    similar_users_ratings = ratings_matrix.iloc[similar_users_indices][item_id]
    similar_users_ratings = similar_users_ratings[similar_users_ratings != 0]
    if len(similar_users_ratings) == 0:
        return False, k
    else:
        predicted_rating = similar_users_ratings.mean()

    return predicted_rating, k


def create_matrixes_to_save():
    data = pd.read_csv('ratings_small.csv')
    data = data.head(99)
    print(data)
    batch_size = len(data) * 2
    print(batch_size)
    create_rating_matrix(data, 0, len(data), batch_size)
