const list_movie = 'http://localhost:5000/print_all_recommandation_movie';
const add_movie = 'http://localhost:5000/add_note_in_matrix';


const rating = document.getElementById('rating');
const addButton = document.getElementById('addListe');
const passerButton = document.getElementById('passer');
let listMovie_recommande = []; // Variable globale pour stocker les données de l'API
let currentIndex = 0; // Indice actuel dans les données de l'API
let listMovie_user= []

const data = [
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    { imageUrl: 'https://png.pngtree.com/png-vector/20190420/ourlarge/pngtree-menu-vector-icon-png-image_963342.jpg', title: 'Titre 1' },
    // Ajoutez d'autres objets ici si nécessaire
];

// Fonction pour afficher la valeur suivante du dictionnaire
function afficherValeurSuivante() {
    // Vérifier si nous avons atteint la fin des données
    if (currentIndex <= listMovie_recommande.message.length - 1) {
        console.log(listMovie_recommande)
        console.log(listMovie_recommande.message.length)
        console.log(currentIndex)
        console.log(listMovie_recommande.message[currentIndex].titre);
        const titre = document.getElementById("titre");
        titre.textContent = `${listMovie_recommande.message[currentIndex].titre}`; // Afficher la valeur correspondante
        const overview = document.getElementById("overview");
        overview.textContent = `${listMovie_recommande.message[currentIndex].overview}`;
        const crew = document.getElementById("crew");
        crew.textContent = `${listMovie_recommande.message[currentIndex].realisateur}`;
        const actor = document.getElementById("listacteur");
        actor.textContent = `${listMovie_recommande.message[currentIndex].acteur}`;
        const genre = document.getElementById("listegenre");
        genre.textContent = `${listMovie_recommande.message[currentIndex].genres}`;
        const dates = document.getElementById("date");
        dates.textContent = `${listMovie_recommande.message[currentIndex].date}`;
        const image = document.getElementById('poster');
        console.log(listMovie_recommande.message[currentIndex].poster)
        image.src = `https://image.tmdb.org/t/p/original${listMovie_recommande.message[currentIndex].poster}`;
        
    } else {
        alert("Fin des films proposés, veuillez entrer de nouveau film");
    }
    
    
}

addButton.addEventListener('click', function() {
    listMovie_user.push({'image' : `https://image.tmdb.org/t/p/original${listMovie_recommande.message[currentIndex].poster}`,'title' : listMovie_recommande.message[currentIndex].titre });
    localStorage.setItem('data', JSON.stringify(listMovie_user));
    console.log(listMovie_user);
    currentIndex++;
    afficherValeurSuivante();
});

// Ajouter un écouteur d'événements au bouton "Passer"
passerButton.addEventListener('click', function() {
    console.log(listMovie_recommande);
    currentIndex++;
    afficherValeurSuivante();
});

rating.addEventListener('click', function(event) {
    const stars = rating.querySelectorAll('input');
    const starClicked = event.target;
    
    // Vérifier si l'élément déclencheur est une étoile
    if (starClicked.tagName === 'INPUT') {
        const starValue = parseFloat(starClicked.getAttribute('value')); // Get the value of the clicked star
        console.log(starValue/2)
        const title = listMovie_recommande.message[currentIndex].titre
        console.log(title);
        const data = { 
            title: title, 
            rating: starValue/2 
        };
        
        const options = {
            method: 'POST',
            mode: 'cors', // Utiliser 'cors' si le serveur prend en charge les requêtes CORS
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(data)
        };
        console.log(options)
        fetch(add_movie, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('La requête a échoué.');
                }
                return response.json();
                window.location.reload();
            })
            .then(data => {
                console.log('Réponse :', data);
                currentIndex++;
                afficherValeurSuivante();
                const listMovie_recommande = data.message;
                listMovie_recommande.forEach(film => {
                    const titre = film.titre;
                    const overview = film.overview;
                    console.log("Titre: ", titre);
                    console.log("Overview: ", overview);
                    
                  });
                //window.location.reload();
                // Actualiser la liste des notes si nécessaire
            })
            .catch(error => {
                console.error('Erreur :', error);
            });
        stars.forEach(star => {
            star.checked = false;
            
        });
    }
});


document.addEventListener("DOMContentLoaded", function() {
    console.log("Titre: ");
    const options = {
        method: 'GET',
        mode: 'cors', // Utiliser 'cors' si le serveur prend en charge les requêtes CORS
        headers: { 
            'Content-Type': 'application/json' 
        }
    };
    console.log(options)
    fetch(list_movie, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('La requête a échoué.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Réponse :', data);
            listMovie_recommande = data;
            console.log("coucouooo",listMovie_recommande.message[0].overview);
            console.log(listMovie_recommande)
            afficherValeurSuivante();
           
              });
            
            //window.location.reload();
            // Actualiser la liste des notes si nécessaire
        })
        

const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');

menuBtn.addEventListener('click', () => {
    menu.classList.toggle('active'); 
});

try {
    // Avant de stocker dans localStorage
    localStorage.setItem('data', JSON.stringify(listMovie_user));
    console.log("Données stockées avec succès dans le localStorage.");
} catch (error) {
    console.error("Erreur lors du stockage des données dans le localStorage :", error);
}
