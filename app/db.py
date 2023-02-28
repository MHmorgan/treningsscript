from pathlib import Path
import sqlite3
from contextlib import contextmanager
from importlib.resources import files

from flask import current_app, g

from . import config


def get_con() -> sqlite3.Connection:
    if 'db' not in g:
        sqlite3.threadsafety = 2
        g.db = sqlite3.connect(config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init():
    if not (p := Path(config.DATABASE)).exists():
        p.touch()
    execute_script('schema.sql')

    try:
        v = int(get_meta('schema_version'))
    except ValueError:
        v = -1

    if v < config.SCHEMA_VERSION:
        set_meta('schema_version', config.SCHEMA_VERSION)


def get_meta(key) -> str:
    con = get_con()
    cur = con.execute('SELECT value FROM Meta WHERE key = ?', (key,))
    if row := cur.fetchone():
        return row['value']
    return ''


def set_meta(key, value):
    con = get_con()
    con.execute("INSERT OR REPLACE INTO Meta (key, value) VALUES (?, ?)", (key, value))
    con.commit()


def table_exists(name) -> bool:
    con = get_con()
    cur = con.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", (name,))
    return bool(cur.fetchone())


def execute_script(fname):
    con = get_con()
    with current_app.open_resource('sql/' + fname) as f:
        con.executescript(f.read().decode('utf8'))
