import gcsfs
import pandas as pd


def get_links():
    gcs_url = "gs://movie_recommendation_1/links.csv"
    return pd.read_csv(gcs_url)

def get_data():
    gcs_url = "gs://movie_recommendation_1/filtered_movies_data.csv"
    return pd.read_csv(gcs_url)


def get_matrix():
    gcs_url = "gs://movie_recommendation_1/matrix_1000000_users.csv"
    return pd.read_csv(gcs_url)


def get_credits():
    gcs_url = "gs://movie_recommendation_1/credits.csv"
    return pd.read_csv(gcs_url)



