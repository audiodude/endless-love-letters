import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/v1')
def v1_index():
  return flask.render_template('v1/index.html')

@app.route('/v1/favorites')
def v1_favorites():
  return flask.render_template('v1/favorites.html')