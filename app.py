import os

import flask
from flask_session import Session

import db
from generate import generate

app = flask.Flask(__name__)
Session(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


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


def maybe_set_user_id(conn):
  user_id = flask.session.get('user_id')
  if user_id is None:
    user_id = db.insert_user(conn)
    flask.session['user_id'] = user_id


@app.route('/api/favorite', methods=['POST'])
def favorite():
  data = flask.request.get_json()
  if 'letter' not in data:
    flask.abort(400)

  conn = db.connect()
  maybe_set_user_id(conn)
  favorite_id = db.insert_favorite(conn, data['letter'],
                                   flask.session['user_id'])

  return flask.jsonify({'id': favorite_id})


@app.route('/api/unfavorite', methods=['POST'])
def unfavorite():
  data = flask.request.get_json()
  if 'id' not in data:
    flask.abort(400)

  if flask.session.get('user_id') is None:
    flask.abort(400)

  conn = db.connect()
  maybe_set_user_id(conn)
  db.delete_favorite(conn, data['id'], flask.session['user_id'])

  return ('', 204)


@app.route('/api/favorites')
def get_favorites():
  user_id = flask.session.get('user_id')
  if user_id is None:
    return flask.jsonify({'favorites': []})

  conn = db.connect()
  favorites = db.get_favorites(conn, user_id)
  return flask.jsonify({'favorites': favorites})
