import requests


url = "https://api.themoviedb.org/3/discover/movie"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwODM0MTNhY2ZjMWI0ODJjOWNjYzZlMTkxOTk5ZWU4OSIsInN1YiI6IjY2MTI4YTI4NmY0M2VjMDEzMWMwZWQ0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rH4uCEjUSgUJe9xfSUORkDeEMqLg-6dGq26aUgEfxOE"
}

params = {
    "include_video": "false",
    "release_date.gte": "2017-10-11",
    "release_date.lte": "2024-04-11",
    "vote_count.gte": "100",
    "sort_by": "popularity.desc",
    "page": 1  # Commencez par la première page
}

all_results = []

while True:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Ajouter les résultats de cette page à la liste
    all_results.extend(data['results'])
    
    # Vérifier s'il y a plus de pages à récupérer
    if data['page'] < data['total_pages']:
        # Passer à la page suivante
        params['page'] += 1
    else:
        # Si nous avons atteint la dernière page, sortir de la boucle
        break

import csv


csv_file_path = 'movies.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = all_results[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for movie in all_results:
        writer.writerow(movie)

print("Le fichier CSV a été créé avec succès :", csv_file_path)


# Imprimer tous les résultats

print(len(all_results))
