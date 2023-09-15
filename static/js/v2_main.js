// From https://stackoverflow.com/a/52171480/41060
const cyrb53 = (str, seed = 0) => {
  let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
  for(let i = 0, ch; i < str.length; i++) {
      ch = str.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761);
      h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1  = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
  h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2  = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
  h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);

  return 4294967296 * (2097151 & h2) + (h1 >>> 0);
};

async function loadData() {
  if (data.length === 0) {
    const response = await fetch('/api/generate');
    data = await response.json();
  }
}

let data = [];

async function fillLetter() {
  await loadData();
  id = Math.floor(Math.random() * data.length);
  const contents = data[id];

  container = document.getElementsByClassName('container')[0];

  letterEl = document.getElementsByClassName('letter')[0];
  letterEl.innerText = contents;
  heartEl = document.getElementsByClassName('heart')[0];

  container.classList.add('visible')
}

function getFavorites() {
  const favoritesJson = localStorage.getItem("favorites");
  if (!favoritesJson) {
    return [];
  }
  return JSON.parse(favoritesJson);
}

function addFavorite(text) {
  const favorites = getFavorites();
  const id = cyrb53(text);
  favorites.shift({id, text});
  localStorage.setItem('favorites', JSON.stringify(favorites));
}

function removeFavorite(id) {
  let favorites = getFavorites();
  favorites = favorites.filter((item) => item.id !== id);
  localStorage.setItem('favorites', JSON.stringify(curIds));
}

function printFavorites() {
  const containerEl = document.getElementsByClassName('container')[0];
  const favorites = getFavorites() || [];
  for (let i = 0; i < favorites.length; i++) {
    const favorite = favorites[i];
    const frame = document.createElement('div');
    frame.classList.add('frame');
    const heart = document.createElement('span');
    heart.classList.add('heart', 'selected');
    heart.data = favorite;
    const letter = document.createElement('div');
    letter.classList.add('letter');
    letter.innerText = favorite.text;
    frame.appendChild(heart);
    frame.appendChild(letter);
    containerEl.append(frame);
  }
  if (favorites.length == 0) {
    const frame = document.createElement('div');
    frame.classList.add('frame');
    const letter = document.createElement('div');
    letter.classList.add('letter');
    letter.innerHTML = '<h2 style="text-align:center">No favorites</h2>';
    frame.appendChild(letter);
    containerEl.append(frame);
  }
  containerEl.classList.add('visible')
}

async function addHeartListeners() {
  if (FAVORITES) {
    printFavorites();
  }
  const hearts = document.getElementsByClassName('heart');
  for (let i = 0; i < hearts.length; i++) {
    const heart = hearts[i];
    heart.addEventListener('click', function () {
      this.classList.toggle('selected');
      if (this.classList.contains('selected')) {
        addFavorite(this.data.text);
      } else {
        removeFavorite(this.data.id);
      }
    });
  }
}

addHeartListeners();