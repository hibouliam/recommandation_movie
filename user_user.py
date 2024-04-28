# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:23:02 2024

@author: huiss
"""
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

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
        print(batch_data)
        print(type(batch_data))
        # Créer la matrice de notation pour ce lot
        ratings_matrix_batch = batch_data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
        print(ratings_matrix_batch)
        # Ajouter la matrice de notation à la liste de résultats
        ratings_matrices.append(ratings_matrix_batch)
        print(ratings_matrices)
        print(type(ratings_matrices))
        z+=1
        print(z)

    # Concaténer les matrices de notation de tous les lots en une seule
    ratings_matrix = pd.concat(ratings_matrices)
    print(ratings_matrix)
    ratings_matrix = ratings_matrix.fillna(0)
    print(ratings_matrix)
    ratings_matrix.to_csv(r'matrix_test.csv', index=False)
    return ratings_matrix

def add_row_matrix(matrix,user) :
    new_row = pd.DataFrame({'1': [0.0]}, index=[user])
    df = pd.concat([matrix,new_row])
    df = df.fillna(0)
    return df

def modify_row_matrix(matrix, user, id_film, note) :
    matrix.loc[int(user), str(int(id_film))] = note 
    return matrix

def sort_users_near_userid(ratings_matrix,user_id) :
   
    user_ratings = ratings_matrix.loc[user_id]
    user_ratings_nonzero = user_ratings[user_ratings != 0]
    print("user_ratings_nonzero",user_ratings_nonzero)
    nbre_movie_rate=len(user_ratings_nonzero)
    ratings_matrix_nonzero = ratings_matrix[user_ratings_nonzero.index]
    print("ratings_matrix_nonzero",[ratings_matrix_nonzero])
    print("ratings_matrix_nonzero",user_ratings_nonzero)
    print(len(ratings_matrix_nonzero))
    list_user_score=[]
    for user in range(0,len(ratings_matrix_nonzero )):
        score=0
        index=0
        number_movie_similar=0
        if not user==user_id :
            #print("i",ratings_matrix_nonzero.iloc[user])
            for rating in ratings_matrix_nonzero.iloc[user] :
                #print(rating)
                if rating != 0.0 :
                    #print( user_ratings_nonzero.iloc[index],type( user_ratings_nonzero.iloc[index]))
                    score += np.abs(rating - float(user_ratings_nonzero.iloc[index]))
                    number_movie_similar+=1
                
                index+=1
            if not number_movie_similar==0 :
                list_user_score.append([user,score,number_movie_similar])
            list_user_score_sort = sorted(list_user_score, key=lambda x: x[2],reverse=True)
            list_user_score_sort = sorted(list_user_score_sort, key=lambda x: x[1])
            
    return list_user_score_sort,nbre_movie_rate

def take_rating(ratings_matrix,list_user_score,movie_id,k,nbr_movie_rate):
    predicted_rating =[]
    number_iteration=0
    print(number_iteration,len(predicted_rating))
    while number_iteration<k or len(predicted_rating)==0 :
    
        print('list',list_user_score[number_iteration][0])
        user_id=int(list_user_score[number_iteration][0])
        similar_users_ratings = ratings_matrix.iloc[user_id][movie_id]
        #print("similar_users_ratings",similar_users_ratings)
        #print("similar_users_ratings",similar_users_ratings)
        #print((similar_users_ratings))
        
        if similar_users_ratings != 0 and (list_user_score[number_iteration][2]>=(nbr_movie_rate)//2 or list_user_score[number_iteration][2]>=5):
            predicted_rating.append(similar_users_ratings)
        number_iteration+=1
    print(predicted_rating)
    print((nbr_movie_rate)//2)
    predicted_rating = sum(predicted_rating)/len(predicted_rating)    
    print(predicted_rating,number_iteration)
    return predicted_rating,number_iteration

def predict_without_cos(data,user_id,id_movie,near_user) :

    sort,nbr_movie_rate=sort_users_near_userid(data, user_id)
    print(sort,nbr_movie_rate)
    predicted_rating,near_user_end = take_rating(data,sort,id_movie,near_user,nbr_movie_rate)
    return predicted_rating,near_user_end

# Fonction pour prédire les notes
def predict(ratings_matrix, user_id, item_id, k):
    
    print("itemi",item_id,type(item_id))
    user_ratings = ratings_matrix.loc[user_id]
    user_ratings_nonzero = user_ratings[user_ratings != 0]
    print("user_ratings_nonzero",user_ratings_nonzero)
    ratings_matrix_nonzero = ratings_matrix[user_ratings_nonzero.index]
    print("ratings_matrix_nonzero",[ratings_matrix_nonzero])
    print("ratings_matrix_nonzero",user_ratings_nonzero)
    donnees = {'1': [100.0]}
    df = pd.DataFrame(donnees)
    df_normalized = normalize(df)
    print(df_normalized)
    print(type(ratings_matrix_nonzero),type([user_ratings_nonzero]),type(df))
    print(ratings_matrix_nonzero)
    
    user_similarities = cosine_similarity([user_ratings_nonzero], normalize(ratings_matrix_nonzero))[0]
    print(user_similarities)
    similar_users_indices = np.argsort(user_similarities)[::-1][1:k+1]
    #print("similar_users_indices",similar_users_indices)
    #print("ratings_matrix.iloc[similar_users_indices]['1']",ratings_matrix.iloc[similar_users_indices][item_id])

    similar_users_ratings = ratings_matrix.iloc[similar_users_indices][item_id]
    similar_users_ratings = similar_users_ratings[similar_users_ratings != 0]
    #print("similar_users_ratings",similar_users_ratings)
    print((similar_users_ratings))
    if len(similar_users_ratings) == 0:
        return False,k
    else :
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
#Création des matrices a enregitrer en csv
'''
#Création des matrices a enregitrer en csv
data = pd.read_csv('ratings_small.csv')
data=data.head(99)
print(data)
batch_size = len(data)*2
print(batch_size)

create_rating_matrix(data,0, len(data), batch_size)
'''

#Concaténation des matrices
#df1=pd.read_csv("matrix.csv")
#print(df1)
'''df2=pd.read_csv("matrix1.csv")
print(df2)
concatenated_df = pd.concat([df1, df2])
concatenated_df.to_csv('concatenated_file.csv', index=False)
print("wesh")'''
'''
data = pd.read_csv('matrix_test.csv')
data=add_row_matrix(data,672)
data=modify_row_matrix(data,672,'2',1000000.0)
predicted,y=predict_without_cos(data,672,'23',3)
print(predicted,y)
print(y)
#Prediction des films en fonction du numéro de l'utilisateur et numéro de film
'''
'''
data = pd.read_csv('matrix_test.csv')
data=add_row_matrix(data,672)
data=modify_row_matrix(data,672,'2',1000000.0)
predict=predict_without_cos(data,673,'23',near_user)
print(predict)










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
'''
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import numpy as np

def compute_difference(row1, row2):
    # Calculer la différence absolue entre chaque paire de valeurs correspondantes
    differences = np.abs(row1 - row2)
    # Somme des différences absolues
    total_difference = np.sum(differences)
    return total_difference

# Définir une matrice de vecteurs
X = np.array([[1, 2, 3], [4, 5, 6], [1, 5, 6]])  # Matrice X

# Indice de la ligne de référence
ligne_reference = 0

# Extraire la ligne de référence
reference = X[ligne_reference]

# Initialiser les variables pour stocker la meilleure correspondance et la différence minimale
meilleure_correspondance = None
difference_minimale = float('inf')  # Initialiser à l'infini pour garantir qu'elle sera remplacée lors de la première itération

# Parcourir toutes les autres lignes
for i, ligne in enumerate(X):
    print(ligne,i)
    if i != ligne_reference:  # Ignorer la ligne de référence elle-même
        # Calculer la différence entre la ligne de référence et la ligne actuelle
        difference = compute_difference(reference, ligne)
        # Mettre à jour la meilleure correspondance si la différence est minimale
        if difference < difference_minimale:
            difference_minimale = difference
            meilleure_correspondance = i

# Afficher l'indice de la ligne la plus similaire
print("L'indice de la ligne la plus similaire à la première ligne est :", meilleure_correspondance)
'''

''' 
        


data=add_row_matrix(data,673)
data=modify_row_matrix(data,673,'2',5.0)
data=modify_row_matrix(data,673,'3',5.0)
data=modify_row_matrix(data,673,'7',3.0)
data=modify_row_matrix(data,673,'1',2.0)
data=modify_row_matrix(data,673,'9',5.0)
data=modify_row_matrix(data,673,'8',0.5)
data=modify_row_matrix(data,673,'10',4.5)
print(data)
print(len(data))
near_user=3
predicted_rating=False
print(sort_users_near_userid(data, 673))
def predict_without_cos(data,user_id,id_movie,near_user) :

    sort,nbr_movie_rate=sort_users_near_userid(data, user_id)
    print(sort,nbr_movie_rate)
    predicted_rating = take_rating(data,sort,id_movie,near_user,nbr_movie_rate)
    return predicted_rating,near_user
print(predict_without_cos(data,673,'23',near_user))

'''