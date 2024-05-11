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
                    print( user_ratings_nonzero.iloc[index],type( user_ratings_nonzero.iloc[index]))
                    score += np.abs(rating - float(user_ratings_nonzero.iloc[index]))
                    number_movie_similar+=1
                
                index+=1
            if not number_movie_similar==0 :
                list_user_score.append([user,score,number_movie_similar])
            list_user_score_sort = sorted(list_user_score, key=lambda x: x[2],reverse=True)
            list_user_score_sort = sorted(list_user_score_sort, key=lambda x: x[1])
            
    return list_user_score_sort,nbre_movie_rate

def take_rating(ratings_matrix,list_user_score,movie_id,k,nbr_movie_rate):
    if not str(movie_id) in ratings_matrix.columns:
        return 0,0
    else :
        predicted_rating =[]
        number_iteration=0
        print(number_iteration,len(predicted_rating))
        print(list_user_score)
        while (number_iteration<k or len(predicted_rating)==0) and number_iteration<len(list_user_score)-1:
        
            print('list',list_user_score[number_iteration][0],number_iteration)
            user_id=int(list_user_score[number_iteration][0])
            similar_users_ratings = ratings_matrix.loc[user_id, str(movie_id)]
            print("similar_users_ratings",similar_users_ratings)
            #print("similar_users_ratings",similar_users_ratings)
            #print((similar_users_ratings))
            
            if similar_users_ratings != 0 and (list_user_score[number_iteration][2]>=(nbr_movie_rate)//2 or list_user_score[number_iteration][2]>=5):
                predicted_rating.append(similar_users_ratings)
            number_iteration+=1
        print(predicted_rating)
        print((nbr_movie_rate)//2)
        if (len(predicted_rating)!=0) :
            predicted_rating = sum(predicted_rating)/len(predicted_rating)    
        else :
            predicted_rating=0
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
'''
