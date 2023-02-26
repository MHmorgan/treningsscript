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
    db = get_db()
    with current_app.open_resource('sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get():
    sqlite3.threadsafety = 2
    db = sqlite3.connect(config.DATABASE)
    db.row_factory = sqlite3.Row
    return db


@contextmanager
def connect():
    con = get()
    try:
        yield con
    finally:
        con.commit()
        con.close()


@contextmanager
def cursor():
    con = get()
    try:
        with con:
            yield con.cursor()
    finally:
        con.close()


def init():
    db = get()
    with files('sql').joinpath('schema.sql').open() as f:
        db.executescript(f.read())
