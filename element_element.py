# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:02:47 2024

@author: huiss
"""

import warnings
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
df=pd.read_csv('movies_metadata.csv')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import time

start = time.time()

#df.columns=['id', 'title', 'cast', 'crew']
#dt=dt.merge(df, on='id')
dt = pd.read_csv('credits.csv')
#fusionne les deux colonnes en fonction de l'Id
df['id'] = pd.to_numeric(df['id'], errors='coerce')
df = pd.merge(df, dt, left_on='id', right_on='id', how='inner')

warnings.filterwarnings('ignore')

cast=dt['cast'].head(1).values
print(cast)

#print(dt.info())
#print(df.columns)

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


def found_movie_from_name(df,movie) :
    for idx, row in df.iterrows():
        
        if row['original_title'] == movie:
            print(df.iloc[idx])
            row_data=df.iloc[idx:idx+1]
            return row_data
    print("Ecrire avec la bonne orthographe voir ci dessous")
    similarites_jaccard = compare_liste_mots_jaccard(movie.lower(), df['title'].fillna('').astype(str))
    title_tries = sorted(similarites_jaccard.items(), key=lambda x: x[1], reverse=True)[0:5]

    for mot, similarite in title_tries:
        print(mot)
    exit()
    

def add_rows(df,row_data):
    
    df = pd.concat([row_data, df])
    return df


def get_director(data_str):
    
    data_json = eval(data_str) 
    for job in data_json :
        if [job['job']=='Director'] :
            return job['name']
    
    return True

def get_name(data_str):
    
    data_json = eval(data_str) 
    noms_acteurs = [acteur['name'] for acteur in data_json]
    return noms_acteurs


def sort_movie(df):
    
    selected_columns = ['belongs_to_collection','original_title','genres', 'id', 'imdb_id', 'original_language', 'popularity', 
                        'revenue', 'runtime', 'spoken_languages', 'vote_average', 
                        'vote_count', 'overview','cast','crew', 'production_companies', 'release_date']
    
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
                              df['overview']  + ' ' + \
                              df['cast']+ ' ' + \
                              df['crew']+ ' ' + \
                              df['vote_count'] + ' ' + \
                              df['vote_average'] + ' ' + \
                              df['popularity'] + ' ' + \
                              df['spoken_languages']+ ' ' + \
                              df['belongs_to_collection']+ ' ' + \
                              df['production_companies']+ ' ' + \
                              df['release_date']
                              
    df['combined_features'].fillna('', inplace=True)
    return df['combined_features']
    
def find_index_movie(df,movie):
    index = df['original_title'] == movie.index[0]
    return index

def find_near_movies (df,df_combined) :
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df_combined)
    
    # Calcul de la similarité cosinus entre les films
    cosine_sim = cosine_similarity(count_matrix)

    # Obtenez les films similaires
    similar_movies = sorted(list(enumerate(cosine_sim[0])), key=lambda x: x[1], reverse=True)[1:11]
    
    


    return similar_movies



total_rows=len(df)
batch_size=1000
similar_movies=[]
movie_name="Toy Story"
row_data=found_movie_from_name(df, movie_name)


for i in range(0,total_rows,batch_size):
    result=[]
    d1 = df.iloc[i:i+batch_size]
    
    d1=add_rows(d1,row_data)
    
    similar_movies1=find_near_movies(d1,sort_movie(d1))
    print(time.time() - start)
    for t in similar_movies1:  
        modified_tuple = (t[0]+i-1, t[1])

        result.append(modified_tuple)
    
    similar_movies+=result


similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:11]
print(time.time() - start)
print(similar_movies)
for movie_index, similarity in similar_movies:
    print("  -", int(df.iloc[movie_index]['imdb_id'][2:]), ":", similarity) 

print(time.time() - start)