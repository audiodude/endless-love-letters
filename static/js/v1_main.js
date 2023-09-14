let data = [];

async function loadData() {
  if (data.length === 0) {
    const response = await fetch('/static/data/letters.json');
    data = await response.json();
  }
}

async function fillLetter() {
  await loadData();
  id = Math.floor(Math.random() * data.length);
  const contents = data[id];

  letterEl = document.getElementsByClassName('letter')[0];
  letterEl.innerText = contents;
  heartEl = document.getElementsByClassName('heart')[0];
  heartEl.data = { letterId: id };

  curIds = getFavoriteIds() || [];
  if (curIds.indexOf(id) !== -1) {
    heartEl.classList.add('selected');
  }
}

function getFavoriteIds() {
  allCookies = document.cookie;
  match = allCookies.match(/favorites=(\[[^;]+\]);?/);
  if (match) {
    return JSON.parse(match[1]);
  }
}

function addFavorite(id) {
  curIds = getFavoriteIds() || [];
  curIds.push(id);
  console.log(curIds);
  document.cookie = 'favorites=' + JSON.stringify(curIds);
}

function removeFavorite(id) {
  curIds = getFavoriteIds() || [];
  idx = curIds.indexOf(id);
  console.log(curIds, id, idx);
  if (idx !== -1) {
    curIds.splice(idx, 1);
    document.cookie = 'favorites=' + JSON.stringify(curIds);
  }
}

async function printFavorites() {
  await loadData();
  containerEl = document.getElementsByClassName('container')[0];
  curIds = getFavoriteIds() || [];
  for (let i = 0; i < curIds.length; i++) {
    const frame = document.createElement('div');
    frame.classList.add('frame');
    const heart = document.createElement('span');
    heart.classList.add('heart', 'selected');
    heart.data = { letterId: curIds[i] };
    const letter = document.createElement('div');
    letter.classList.add('letter');
    letter.innerText = data[curIds[i]];
    frame.appendChild(heart);
    frame.appendChild(letter);
    containerEl.append(frame);
  }
}

async function addHeartListeners() {
  if (FAVORITES) {
    console.log('Printing favorites...');
    await printFavorites();
  }
  hearts = document.getElementsByClassName('heart');
  for (let i = 0; i < hearts.length; i++) {
    heart = hearts[i];
    heart.addEventListener('click', function () {
      this.classList.toggle('selected');
      if (this.classList.contains('selected')) {
        addFavorite(this.data.letterId);
      } else {
        removeFavorite(this.data.letterId);
      }
    });
  }
}

addHeartListeners();
