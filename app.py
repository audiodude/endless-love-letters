import flask

from generate import generate

app = flask.Flask(__name__)


@app.route('/')
def index():
  return flask.render_template('index.html')


@app.route('/<version>')
def view(version):
  if version not in ('v1', 'v2'):
    flask.abort(404)
  return flask.render_template(f'{version}/view.html')


@app.route('/<version>/favorites')
def favorites(version):
  if version not in ('v1', 'v2'):
    flask.abort(404)
  return flask.render_template(f'{version}/favorites.html')


@app.route('/api/generate')
def generate_letter():
  letter = generate()
  return flask.jsonify({'letter': letter})


@app.route('/api/favorite', methods=['POST'])
def favorite():
  data = flask.request.get_json()
  if 'letter' not in data:
    flask.abort(400)
  return flask.jsonify({'id': 1})


@app.route('/api/unfavorite', methods=['POST'])
def unfavorite():
  data = flask.request.get_json()
  if 'id' not in data:
    flask.abort(400)
  print(data['id'])
  return ('', 204)
