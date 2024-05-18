const found_movie_title = 'http://localhost:5000/found_movie_title';
const add_movie = 'http://localhost:5000/add_note_in_matrix';

// Récupération des éléments du DOM
const searchInput = document.getElementById('search-input');
const suggestionsList = document.getElementById('suggestions');
const noteForm = document.getElementById('add');

// Fonction pour proposer des films
searchInput.addEventListener('input', function() {
    const searchQuery = this.value.trim(); // Récupérer la valeur entrée

    if (searchQuery.length === 0) {
        suggestionsList.innerHTML = ''; // Effacer les suggestions si vide
        return;
    }

    const data = { // Transmettre donnée de recherche
        parametre: searchQuery,
        test: 'ehl'
    };

    const options = {
        method: 'POST',
        headers: { // Type de contenu de la requête
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Convertir en JSON pour la requête
    };
    console.log(options);
    fetch(found_movie_title, options)
        .then(response => response.json())
        .then(data => {
            console.log('Résultat de la fonction Python :', data.resultat);
            suggestionsList.innerHTML = ''; // Effacer les anciennes suggestions

            for (let key in data.resultat) {
                const suggestion = document.createElement('li'); // Utilisation de <li> au lieu de <div>
                suggestion.textContent = data.resultat[key];
                suggestionsList.appendChild(suggestion);
            }
            suggestionsList.style.display = 'block'; // Afficher les suggestions
        })
        .catch(error => console.error('Erreur :', error));
});

// Écouteur d'événements de clic sur suggestionsList
suggestionsList.addEventListener('click', (event) => {
    if (event.target.tagName === 'LI') { // Vérifier si l'élément cible est un <li>
        searchInput.value = event.target.textContent;
        suggestionsList.style.display = 'none'; // Puis cacher les suggestions
    }
});

// Enregistrer le film dans la matrice
document.addEventListener("DOMContentLoaded", function() { // S'assurer que tout est chargé
    const addButton = document.getElementById('add');

    addButton.addEventListener('click', async function(event) {
        event.preventDefault(); // Empêcher le rechargement de la page
        
        // Récupérer les valeurs saisies dans le formulaire
        const title = document.getElementById('search-input').value;
        const rating = document.getElementById('note').value;
        const data = { 
            title: title, 
            rating: rating 
        };
        
        const options = {
            method: 'POST',
            mode: 'cors', // Utiliser 'cors' si le serveur prend en charge les requêtes CORS
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };
        console.log(options);
        fetch(add_movie, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('La requête a échoué.');
                }
                return response.json();
            })
            .then(data => {
                console.log('Réponse :', data);
                const listMovie = data.message;
                alert("Film bien ajouté");
                listMovie.forEach(film => {
                    const titre = film.titre;
                    const overview = film.overview;
                    console.log("Titre: ", titre);
                    console.log("Overview: ", overview);
                });
                window.location.reload();
            })
            .catch(error => {
                console.error('Erreur :', error);
                alert("Sélectionnez un film dans la base.");
            });
    });
});

const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');

menuBtn.addEventListener('click', () => {
    menu.classList.toggle('active');
});
