import os

import pymysql

CREDS = {}
for key in ('user', 'password', 'host', 'port', 'db'):
  CREDS[key] = os.environ.get(f'MYSQL_{key.upper()}')
CREDS = dict((key, value) for key, value in CREDS.items() if value is not None)


def connect():
  return pymysql.connect(**CREDS)


def insert_user(conn):
  with conn.cursor() as cursor:
    cursor.execute('INSERT INTO users VALUES ()')
    conn.commit()
    return cursor.lastrowid


def insert_favorite(conn, contents, user_id):
  with conn.cursor() as cursor:
    cursor.execute('INSERT INTO favorites (content, user_id) VALUES (%s, %s)',
                   (contents, user_id))
    conn.commit()
    return cursor.lastrowid


def delete_favorite(conn, favorite_id, user_id):
  with conn.cursor() as cursor:
    cursor.execute('DELETE FROM favorites WHERE id = %s AND user_id = %s',
                   (favorite_id, user_id))
    conn.commit()
    return cursor.lastrowid
