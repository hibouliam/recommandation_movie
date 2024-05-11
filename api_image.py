import pandas as pd
import requests
import csv

df = pd.read_csv('movies_metadata.csv')

base_url = "https://api.themoviedb.org/3/movie/{}?language=en-US"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwODM0MTNhY2ZjMWI0ODJjOWNjYzZlMTkxOTk5ZWU4OSIsInN1YiI6IjY2MTI4YTI4NmY0M2VjMDEzMWMwZWQ0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rH4uCEjUSgUJe9xfSUORkDeEMqLg-6dGq26aUgEfxOE"
}

def get_poster_path(movie_id):
    url = base_url.format(movie_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        poster_path = response.json().get('poster_path')
        return poster_path
    else:
        return None

with open('movies_metadata_updated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(df.columns)  # Write the header row

    for index, row in df.iterrows():
        poster_path = get_poster_path(row['id'])
        row['poster_path'] = poster_path
        writer.writerow(row)

print("Le fichier CSV a été mis à jour avec succès.")
