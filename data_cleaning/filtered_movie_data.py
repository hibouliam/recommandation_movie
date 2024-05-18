import numpy as np
import pandas as pd
from pandas import DataFrame
import gcsfs



def get_links():
    gcs_url = "gs://movie_recommendation_1/links.csv"
    return pd.read_csv(gcs_url)

def get_data():
    gcs_url = "gs://movie_recommendation_1/movies_metadata_updated.csv"
    return pd.read_csv(gcs_url)


def get_matrix():
    gcs_url = "gs://movie_recommendation_1/matrix_test.csv"
    return pd.read_csv(gcs_url)


def get_credits():
    gcs_url = "gs://movie_recommendation_1/credits.csv"
    return pd.read_csv(gcs_url)



links = get_links()
data = get_data()

credits = get_credits()




# fusione les deux colonnes en fonction de l'Id
def clean_imdb_id(imdb_id):
    if isinstance(imdb_id, str) and len(imdb_id) >= 2:
        return int(imdb_id[2:])
    else:
        return np.nan if imdb_id == '' else imdb_id


data['imdb_id'] = data['imdb_id'].apply(clean_imdb_id)
data = pd.merge(data, links, how='left', left_on='imdb_id', right_on='imdbId')
data = data.dropna(subset=['imdbId'])
data['imdbId'] = data['imdbId'].astype(int)
data['movieId'] = data['movieId'].astype(int)
data['id'] = pd.to_numeric(data['id'], errors='coerce')
data = pd.merge(data, credits, left_on='id', right_on='id', how='inner')



matrix_df=get_matrix()

print(matrix_df.head())
movie_ids_in_matrix = matrix_df.columns.astype(int)
filtered_movies_df = data[data['movieId'].isin(movie_ids_in_matrix)]

print(filtered_movies_df.info())
print(filtered_movies_df.head())
print(filtered_movies_df.describe())

filtered_movies_df.to_csv('filtered_movies.csv', index=False)
