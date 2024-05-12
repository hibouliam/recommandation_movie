import pandas as pd
from pandas import DataFrame

from recommentation.movie_recommendation_engine import add_rows, find_near_movies, get_movie_features, \
    sort_similar_user, calculate_predicted_rating

   
def generate_user_recommendations(data: DataFrame,matrix : DataFrame,id_user: int)-> list:
    list_movie_note_user=[]
    user_ratings = matrix.loc[id_user]

    user_ratings_nonzero = user_ratings[user_ratings != 0]
    for id_link,rate in user_ratings_nonzero.items()    :
        print(id_link, type(id_link))
        print(data.loc[data['movieId'] == int(id_link)])
        list_movie_note_user.append(data.loc[data['movieId'] == int(id_link)])
    print(list_movie_note_user)
    total_rows=len(data)
    batch_size=1000
    similar_movies=[]
    similar_movies_imdb=[]
#Cherche les films les plus similaires en fonction du contenu de chacun en utilisant en séparant pour une question de rapidité
    for i in range(0,total_rows,batch_size): 
        result=[]
        d1 = data.iloc[i:i+batch_size]
        for movie_note_user in list_movie_note_user :
            #print(movie_note_user[1]) #vérification
            d1=add_rows(d1,movie_note_user)
        #Cherche les films les plus proches
        similar_movies1=find_near_movies(get_movie_features(d1), len(list_movie_note_user))
        #Ajout a une liste tuple
        for t in similar_movies1:  
            #print(t[0],t[1], type(t[0]))
            modified_tuple = (int(t[0])+i-1, t[1])

            result.append(modified_tuple)
        
        similar_movies+=result
    #Gardons que les 25 films les plus proches
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[0:25]
    #print("aba",similar_movies)
    unique_movies = set()
    final_similar_movies = []
    #Verifie qu'ils sont unique
    for movie in similar_movies:
        if movie[0] not in unique_movies:
            final_similar_movies.append(movie)
            unique_movies.add(movie[0])
    #Retrie la liste avec que des unique en fonction de la similarité
    similar_movies = sorted(final_similar_movies, key=lambda x: x[1], reverse=True)
    #Et on crée une liste avec le nom et l'imdb 
    for movie_index, similarity in similar_movies:
        similar_movies_imdb.append([data.iloc[movie_index]['title'],data.iloc[movie_index]['imdb_id']]) 
    print(similar_movies_imdb)
    #User-user   
    near_user=8
    #utilisateur 7 pour film 1 qd 8
    predict_rating_list =[]
    
    #Prendre les trois films les plus similaires
    similar_movies_imdb=similar_movies_imdb[0:20] 

    #on cherche les utilisateurs les plus proches
    sort,nbr_movie_rate=sort_similar_user(matrix, id_user)

    #Pour chaque film similaire on cherche a prédire la note
    for movie_imdb in similar_movies_imdb :
        predicted_rating =False
        id_imdb=movie_imdb[1]
        id_movie=str(int(data.loc[data['imdbId'] == int(id_imdb), 'movieId'].values[0]))
        predicted_rating,user= calculate_predicted_rating(matrix,sort,id_movie,near_user,nbr_movie_rate)
        predict_rating_list.append([movie_imdb,predicted_rating,user,data.loc[data['imdbId'] == int(movie_imdb[1])]])
        print(predict_rating_list)  


    #Et on affiche les films qui ont une note supérieur à une note prédéfénite
    for movie in predict_rating_list :
        if (movie[1]>=4.0 and movie[2]<50) :
            print(movie[0]) #c'est le numéro imdb et titre du film qui est recommandé 
    return predict_rating_list

