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
