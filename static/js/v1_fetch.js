async function loadData() {
  if (data.length === 0) {
    const response = await fetch('/static/data/letters.json');
    data = await response.json();
  }
}
