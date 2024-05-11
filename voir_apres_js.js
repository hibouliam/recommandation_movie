const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');
const container = document.getElementById('container');

const storedList = localStorage.getItem('data');
const data = JSON.parse(storedList);
console.log(data);
menuBtn.addEventListener('click', () => {
    menu.classList.toggle('active'); 
});



data.forEach(item => {
    const div = document.createElement('div');
    div.classList.add('item');
    const img = document.createElement('img');
    img.src = item.image;//balise img
    const title = document.createElement('h3');
    title.textContent = item.title;
    div.appendChild(img);
    div.appendChild(title);
    container.appendChild(div);
});
