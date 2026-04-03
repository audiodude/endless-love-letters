async function loadData() {
  if (data.length === 0) {
    const response = await fetch('/static/data/letters.json');
    data = await response.json();
  }
}

let data = [];
let favoriteMap = {}; // letterId -> server favorite id

async function loadFavorites() {
  const response = await fetch('/api/favorites');
  const result = await response.json();
  return result.favorites;
}

async function fillLetter() {
  await loadData();
  const id = Math.floor(Math.random() * data.length);
  const contents = data[id];

  const container = document.getElementsByClassName('container')[0];
  const letterEl = document.getElementsByClassName('letter')[0];
  letterEl.innerText = contents;

  const heartEl = document.getElementsByClassName('heart')[0];
  heartEl.dataset.letterId = id;

  // Check if this letter is already favorited
  const favorites = await loadFavorites();
  favorites.forEach(fav => {
    if (fav.content === contents) {
      heartEl.classList.add('selected');
      favoriteMap[id] = fav.id;
    }
  });

  container.classList.add('visible');
}

async function addFavorite(letterId) {
  const contents = data[letterId];
  const response = await fetch('/api/favorite', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ letter: contents }),
  });
  const result = await response.json();
  favoriteMap[letterId] = result.id;
}

async function removeFavorite(letterId) {
  const favId = favoriteMap[letterId];
  if (favId) {
    await fetch('/api/unfavorite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: favId }),
    });
    delete favoriteMap[letterId];
  }
}

async function printFavorites() {
  const containerEl = document.getElementsByClassName('container')[0];
  const favorites = await loadFavorites();

  for (const fav of favorites) {
    const frame = document.createElement('div');
    frame.classList.add('frame', 'v1');
    const heart = document.createElement('span');
    heart.classList.add('heart', 'selected');
    heart.dataset.favId = fav.id;
    const letter = document.createElement('div');
    letter.classList.add('letter');
    letter.innerText = fav.content;
    frame.appendChild(heart);
    frame.appendChild(letter);
    containerEl.append(frame);
  }

  if (favorites.length === 0) {
    const frame = document.createElement('div');
    frame.classList.add('frame', 'v1');
    const letter = document.createElement('div');
    letter.classList.add('letter');
    letter.innerHTML = '<h2 style="text-align:center">No favorites</h2>';
    frame.appendChild(letter);
    containerEl.append(frame);
  }
  containerEl.classList.add('visible');
}

async function addHeartListeners() {
  if (FAVORITES) {
    await printFavorites();
  }
  const hearts = document.getElementsByClassName('heart');
  for (let i = 0; i < hearts.length; i++) {
    const heart = hearts[i];
    heart.addEventListener('click', async function () {
      this.classList.toggle('selected');
      if (this.classList.contains('selected')) {
        if (this.dataset.letterId !== undefined) {
          await addFavorite(parseInt(this.dataset.letterId));
        }
      } else {
        if (this.dataset.letterId !== undefined) {
          await removeFavorite(parseInt(this.dataset.letterId));
        } else if (this.dataset.favId) {
          await fetch('/api/unfavorite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: parseInt(this.dataset.favId) }),
          });
          this.closest('.frame').remove();
        }
      }
    });
  }
}

addHeartListeners();
