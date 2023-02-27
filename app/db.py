from pathlib import Path
import sqlite3
from contextlib import contextmanager
from importlib.resources import files

from flask import current_app, g

from . import config


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        sqlite3.threadsafety = 2
        g.db = sqlite3.connect(config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    if not (p := Path(config.DATABASE)).exists():
        p.touch()
    db = get_db()
    with current_app.open_resource('sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
