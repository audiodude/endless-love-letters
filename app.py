from functools import wraps
import json
import os

import anthropic
import flask
from flask_session import Session

import db
from generate import generate
from generate_vibed import generate_vibed
from get_secrets import secret
from letters import DATABASE

app = flask.Flask(__name__)
Session(app)
app.config['SECRET_KEY'] = secret('FLASK_SECRET_KEY')
app.config['WEB_PASSWORD'] = secret('WEB_PASSWORD')


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
  if version not in ('v1', 'v2', 'vibed'):
    flask.abort(404)
  adj = flask.request.args.get('adj')
  extra = flask.request.args.get('extra')
  if version == 'vibed':
    from generate_vibed import MODIFIERS
    retro = flask.request.args.get('retro') == '1'
    try:
      letter = generate_vibed(adj=adj, extra=extra, retro=retro)
    except anthropic.APIStatusError:
      return flask.render_template('vibed/error.html',
                                   adjectives=list(MODIFIERS['adjectives'].keys()),
                                   extras=list(MODIFIERS['extras'].keys())), 503
    return flask.render_template('vibed/view.html', letter=letter,
                                 adjectives=list(MODIFIERS['adjectives'].keys()),
                                 extras=list(MODIFIERS['extras'].keys()))
  if version == 'v2':
    letter = generate(adj=adj, extra=extra)
    return flask.render_template('v2/view.html', letter=letter)

  return flask.render_template('v1/view.html')


@app.route('/favorites')
def favorites():
  return flask.render_template('v2/favorites.html')


@app.route('/<version>/favorites')
def favorites_legacy(version):
  return flask.redirect('/favorites')


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
  return flask.render_template('search.html')


@app.route('/api/search')
@require_auth
def api_search():
  q = flask.request.args.get('q', '').lower()
  if not q:
    return flask.jsonify([])
  results = [{'ref': doc_id, 'letter': letter}
             for doc_id, letter in DATABASE.items()
             if q in letter.lower()]
  return flask.jsonify(results)


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


