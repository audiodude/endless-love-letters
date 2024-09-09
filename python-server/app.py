from functools import wraps
import json
import os

import flask
from flask_session import Session

import db
from generate import generate
from get_secrets import secret

app = flask.Flask(__name__)
Session(app)
app.config['SECRET_KEY'] = secret('FLASK_SECRET_KEY')
app.config['WEB_PASSWORD'] = secret('WEB_PASSWORD')

DATABASE = {}
with open('search_documents.jsonl') as f:
  search_documents = [json.loads(doc) for doc in f.read().splitlines()]
  for doc in search_documents:
    print(repr(doc['id']))
    DATABASE[doc['id']] = doc['letter']


def require_auth(fn):

  @wraps(fn)
  def wrapped(*args, **kwargs):
    if not flask.session.get('has_password'):
      return flask.redirect('/login')
    return fn(*args, **kwargs)

  return wrapped


@app.route('/')
def index():
  return flask.render_template('index.html')


@app.route('/<version>')
def view(version):
  if version not in ('v1', 'v2'):
    flask.abort(404)
  if version == 'v2':
    adj = flask.request.args.get('adj')
    extra = flask.request.args.get('extra')
    letter = generate(adj=adj, extra=extra)
    return flask.render_template(f'v2/view.html', letter=letter)

  return flask.render_template(f'v1/view.html')


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


@app.route('/search')
@require_auth
def search():
  for key in flask.session:
    print(f'{key}: {flask.session[key]}')
  return flask.render_template('search.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'POST':
    if flask.request.form.get(
        'password') == flask.current_app.config['WEB_PASSWORD']:
      flask.session['has_password'] = True
      return flask.redirect('/search')
    else:
      return flask.render_template('login.html', error=True)
  elif flask.session.get('has_password'):
    return flask.redirect('/search')
  else:
    return flask.render_template('login.html')


@app.route('/doc/<id_>')
@require_auth
def doc(id_):
  if id_ not in DATABASE:
    flask.abort(404)
  return flask.jsonify({'letter': DATABASE[id_]})
