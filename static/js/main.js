let data = [];

async function fillLetter() {
  await loadData();
  id = Math.floor(Math.random() * data.length);
  const contents = data[id];

  container = document.getElementsByClassName('container')[0];

  letterEl = document.getElementsByClassName('letter')[0];
  letterEl.classList.add('loaded')
  letterEl.innerText = contents;
  heartEl = document.getElementsByClassName('heart')[0];
  heartEl.data = { letterId: id };

  curIds = getFavoriteIds() || [];
  if (curIds.indexOf(id) !== -1) {
    heartEl.classList.add('selected');
  }
  container.classList.add('visible')
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
  document.cookie = 'favorites=' + JSON.stringify(curIds) + ';path=/v1/';
}

function removeFavorite(id) {
  curIds = getFavoriteIds() || [];
  idx = curIds.indexOf(id);
  console.log(curIds, id, idx);
  if (idx !== -1) {
    curIds.splice(idx, 1);
    document.cookie = 'favorites=' + JSON.stringify(curIds) + ';path=/v1/';
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
  if (curIds.length == 0) {
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
