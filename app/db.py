import sqlite3
from contextlib import contextmanager
from importlib.resources import files

from . import config


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
