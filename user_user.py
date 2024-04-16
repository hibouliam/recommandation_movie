# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:23:02 2024

@author: huiss
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

'''# Charger les données
data = pd.read_csv('ratings.csv')
print(data.head())

# Définir la taille du lot
batch_size = 100000  # Vous pouvez ajuster cette taille en fonction de la taille de votre ensemble de données et de la capacité mémoire de votre système
print(len(data))
# Obtenir le nombre total de lignes dans votre ensemble de données
total_rows = len(data)//1000
print()
# Initialiser la liste pour stocker les résultats
ratings_matrices = []'''

# Diviser l'ensemble de données en lots et traiter chaque lot séparément
def create_rating_matrix (data,start,total_rows, batch_size):
    z=0
    ratings_matrices = []
    for i in range(start, total_rows, batch_size):
        # Sélectionner un lot de données
        batch_data = data.iloc[i:i+batch_size]
        # Créer la matrice de notation pour ce lot
        ratings_matrix_batch = batch_data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        
        # Ajouter la matrice de notation à la liste de résultats
        ratings_matrices.append(ratings_matrix_batch)
        z+=1
        print(z)
   
    # Concaténer les matrices de notation de tous les lots en une seule
    ratings_matrix = pd.concat(ratings_matrices)
    ratings_matrix = ratings_matrix.fillna(0)
    print(ratings_matrix)
    ratings_matrix.to_csv(r'matrix.csv', index=False)
    return ratings_matrix

# Fonction pour prédire les notes
def predict(ratings_matrix, user_id, item_id, k):
    user_ratings = ratings_matrix.loc[user_id]
    #print("user_ratings",user_ratings)
    user_ratings_nonzero = user_ratings[user_ratings != 0]
    #print("user_ratings_nonzero",user_ratings_nonzero)
    ratings_matrix_nonzero = ratings_matrix[user_ratings_nonzero.index]
    #print("ratings_matrix_nonzero",ratings_matrix_nonzero)
    user_similarities = cosine_similarity([user_ratings_nonzero], ratings_matrix_nonzero)[0]
    similar_users_indices = np.argsort(user_similarities)[::-1][1:k+1]
    #print("similar_users_indices",similar_users_indices)
    #print("ratings_matrix.iloc[similar_users_indices]['1']",ratings_matrix.iloc[similar_users_indices][item_id])

    similar_users_ratings = ratings_matrix.iloc[similar_users_indices][item_id]
    similar_users_ratings = similar_users_ratings[similar_users_ratings != 0]
    #print("similar_users_ratings",similar_users_ratings)
    if len(similar_users_ratings) == 0:
        k+=1
        predict (ratings_matrix,user_id,item_id,k) # Retourner 0 si aucun utilisateur similaire n'a noté ce film
    
    predicted_rating = similar_users_ratings.mean()
    
    return predicted_rating,k

'''
predicted_rating=0
for i in range (0,total_rows,1000000):
    if not i==(26000000):
        ratings_matrix=create_rating_matrix(i, (i+1000000), batch_size)
        inverted_matrix = ratings_matrix.T

# Vous pouvez également réinitialiser les index si nécessaire
        inverted_matrix.reset_index(drop=True, inplace=True)

        print(inverted_matrix)
        print(ratings_matrix)
    else :
        ratings_matrix=create_rating_matrix(i, total_rows, batch_size)
user_id = 27
item_id = [1394,1376,1375,1374,1373,1372,1371]
for i in item_id :
    predicted_rating= predict(ratings_matrix, user_id, i, k=50)
    
    print(f"La note prédite pour l'utilisateur {user_id} et le film {i} est: {predicted_rating}")
'''
#data = pd.read_csv('ratings.csv')
#batch_size = 100000
#create_rating_matrix(data,0, 500000, batch_size)
#df1=pd.read_csv("concatenated_file.csv")
#print(df1)
'''df2=pd.read_csv("matrix1.csv")
print(df2)
concatenated_df = pd.concat([df1, df2])
concatenated_df.to_csv('concatenated_file.csv', index=False)
print("wesh")'''


data = pd.read_csv('matrix.csv')
print(data)
predicted_rating,k= predict(data, 2, '1', k=3)
print(predicted_rating,k)























'''
# Tester la prédiction pour un utilisateur et un film spécifiques
user_id = 7
item_id = 1408
z=0
# Créer deux listes pour stocker les évaluations de userId 3 et 378
ratings_3 = []
ratings_378 = []

# Parcourir les données pour récupérer les évaluations correspondantes
for i in range(total_rows):
    if data['userId'][i] == 7:
        ratings_3.append((data['movieId'][i], data['rating'][i]))
    elif data['userId'][i] == 10004:
        ratings_378.append((data['movieId'][i], data['rating'][i]))

# Trouver la longueur maximale des listes pour aligner les valeurs
max_length = max(len(ratings_3), len(ratings_378))
max_length = max(len(ratings_3), len(ratings_378))

# Imprimer les évaluations alignées
print("userId 3".ljust(20), "userId 378")
for i in range(max_length):
    # Assurer que les index ne dépassent pas la longueur des listes
    rating_3 = ratings_3[i] if i < len(ratings_3) else ("", "")
    rating_378 = ratings_378[i] if i < len(ratings_378) else ("", "")
    print(f"{str(rating_3[0])}: {str(rating_3[1])}".ljust(20), f"{str(rating_378[0])}: {str(rating_378[1])}")
# Imprimer les évaluations alignées
print("userId 3".ljust(20), "userId 378")

for i in  ratings_3:
    
    for j in ratings_378:
        if i[0] ==j[0]:
            print(f"{str(i[0])}: {str(i[1])}".ljust(20), f"{str(j[0])}: {str(j[1])}")
predicted_rating= predict(ratings_matrix, user_id, item_id, k=1000)

print(f"La note prédite pour l'utilisateur {user_id} et le film {item_id} est: {predicted_rating}",z)
user_id = 270000
item_id = 1405
predicted_rating= predict(ratings_matrix, user_id, item_id, k=1000)

print(f"La note prédite pour l'utilisateur {user_id} et le film {item_id} est: {predicted_rating}",z)
'''