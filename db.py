import os
import sqlite3

from letters import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, 'endless_love_letters.db')


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL
    )''')
    return conn


def insert_user(conn):
    cursor = conn.execute('INSERT INTO users DEFAULT VALUES')
    conn.commit()
    return cursor.lastrowid


def insert_favorite(conn, contents, user_id):
    cursor = conn.execute(
        'INSERT INTO favorites (content, user_id) VALUES (?, ?)',
        (contents, user_id))
    conn.commit()
    return cursor.lastrowid


def delete_favorite(conn, favorite_id, user_id):
    conn.execute(
        'DELETE FROM favorites WHERE id = ? AND user_id = ?',
        (favorite_id, user_id))
    conn.commit()


def get_favorites(conn, user_id):
    cursor = conn.execute(
        'SELECT id, content FROM favorites WHERE user_id = ? '
        'ORDER BY id DESC', (user_id,))
    return [{'id': row[0], 'content': row[1]} for row in cursor.fetchall()]
