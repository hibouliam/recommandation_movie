import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
from user_user import predict_without_cos,modify_row_matrix,add_row_matrix,sort_users_near_userid,take_rating
from sklearn.feature_extraction.text import CountVectorizer
from element_element import found_movie_from_name, add_rows,find_near_movies,sort_movie
from sklearn.metrics.pairwise import cosine_similarity

links=pd.read_csv('links.csv')
data=pd.read_csv('movies_metadata.csv')
matrix=pd.read_csv('matrix_test.csv')
dt = pd.read_csv('credits.csv')
#fusionne les deux colonnes en fonction de l'Id
data['id'] = pd.to_numeric(data['id'], errors='coerce')
data = pd.merge(data, dt, left_on='id', right_on='id', how='inner')
warnings.filterwarnings('ignore')
#Initialisation demande

list_movie_note_user=[]


#Première étape on demande les films qu'il aime en y mettant une note
while len(list_movie_note_user)<=1:
    movie=input("Veuillez entrer un film : ")
    row_data=found_movie_from_name(data,movie)
    if not row_data.empty:
        note=input("Veuillez entrer une note : ")
        list_movie_note_user.append([movie,row_data,note,row_data['imdb_id'].iloc[0][2:]])
        #print([movie,row_data["imdb_id"],note])
        #print(row_data['imdb_id'].iloc[0][2:])
#print(list_movie_note_user)

 

#Deuxième étape on utilise les similarités élément_élément qui retourne dix id imdb 

total_rows=len(data)
batch_size=1000
similar_movies=[]
similar_movies_imdb=[]

for i in range(0,total_rows,batch_size):
    result=[]
    d1 = data.iloc[i:i+batch_size]
    for movie_note_user in list_movie_note_user :
        #print(movie_note_user[1]) #vérification
        d1=add_rows(d1,movie_note_user[1])
    
    similar_movies1=find_near_movies(d1,sort_movie(d1),len(list_movie_note_user))
    
    for t in similar_movies1:  
        #print(t[0],t[1], type(t[0]))
        modified_tuple = (int(t[0])+i-1, t[1])

        result.append(modified_tuple)
    
    similar_movies+=result

similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[0:25]
#print("aba",similar_movies)
unique_movies = set()
final_similar_movies = []

for movie in similar_movies:
    if movie[0] not in unique_movies:
        final_similar_movies.append(movie)
        unique_movies.add(movie[0])

similar_movies = sorted(final_similar_movies, key=lambda x: x[1], reverse=True)
#print(similar_movies)
for movie_index, similarity in similar_movies:
    similar_movies_imdb.append([data.iloc[movie_index]['title'],int(data.iloc[movie_index]['imdb_id'][2:])]) 
#print("imdb",similar_movies_imdb)

#On trouve l'id dans pour le fichier rating 
def link_between_moviesid(links,movie_imdb):
    for item in range(len(links)):
        value = links.iloc[item][1]
        if not pd.isnull(value) and int(value) == movie_imdb:
            #print (links.iloc[item][0])
            return links.iloc[item][0] 
    return None


#On crée une nouvelle ligne à la matrice ratings en ajoutant les nouveaux id movie
id_user=len(matrix)
matrix=add_row_matrix(matrix,id_user)
for movie in list_movie_note_user :
    #print(movie)
    note_user=movie[2]
    #print(note_user)
    id_imdb=movie[3]
    #print(id_imdb)
    id_imdb=int(id_imdb)
    
    moviesid=link_between_moviesid(links, id_imdb)
    matrix=modify_row_matrix(matrix,id_user,moviesid,note_user) 

#Et on utilise l'algo user user pour trouver la note qu'il mettrait au film similaire

near_user=8
id_user=len(matrix)-1 #utilisateur 7 pour film 1 ligne 10 qd 8
predict_rating_list =[]
#print(matrix)
#print(similar_movies_imdb)
similar_movies_imdb=similar_movies_imdb[0:3]
sort,nbr_movie_rate=sort_users_near_userid(matrix, id_user)
for movie_imdb in similar_movies_imdb :
    predicted_rating =False
    #print(movie_imdb)
    id_imdb=movie_imdb[1]
    #print(id_imdb)
    id_movie=str(int(link_between_moviesid(links, id_imdb))) 
    #print('TRans',id_movie)
    #print(id_user)
    #print(near_user)
    
    predicted_rating,user= take_rating(matrix,sort,id_movie,near_user,nbr_movie_rate)
    #print(predicted_rating)
    predict_rating_list.append([movie_imdb,predicted_rating,user])
    print(predict_rating_list)  
#Et on affiche les films qui ont une note supérieur à une note prédéfénite
for movie in predict_rating_list :
    if (movie[1]>=4.0 and movie[2]<10) :
        print(movie[0]) #c'est le numéro imdb et titre du film qui est recommandé 
