import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv('links.csv')
df=df.head(20)
print(df.head())

id='tt0210234'
print(int(id[2:]))

#Première étape on demande les films qu'il aime en y mettant une note

#Deuxième étape on utilise les similarités élément_élément qui
 
#Retourne dix id imdb 

#On trouve l'id dans pour le fichier rating 
def link_between_moviesid(movie_imdb):
    for item in range(len(df)):
        if int(df.iloc[item][1]) == movie_imdb :
            return df.iloc[item][0] 
    return False 


#On crée une nouvelle ligne à la matrice ratings en ajoutant les nouveaux id movie

#Et on utilise l'algo user user pour trouver la note qu'il mettrait au film similaire

#Et on affiche les films qui ont une note supérieur à une note prédéfénite
