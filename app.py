import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/<version>')
def view(version):
  if version not in ('v1', 'v2'):
    flask.abort(404)
  return flask.render_template('view.html', main_path=f'{version}_main.js', favorites_path=f'/{version}/favorites')

@app.route('/<version>/favorites')
def favorites(version):
  if version not in ('v1', 'v2'):
    flask.abort(404)
  return flask.render_template('favorites.html', main_path=f'{version}_main.js')

@app.route('/api/generate')
def generate_letter():
  return flask.jsonify(['Foo test letter'])
