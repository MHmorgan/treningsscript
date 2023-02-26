import sqlite3
from os import environ

from click import secho
from flask import (
    Flask
)

from . import (
    api,
    db,
    website
)


def bail(msg):
    secho(f'[!!] {msg}', err=True, fg='red')
    exit(1)


def create_app():
    app = Flask(__name__)

    app.secret_key = environ.get(
        'SECRET_KEY',
        'a2e112dafab36433dab1a5ff173df9ae9f8dcfed854cb4663c0e6af81c3ae3cf'
    )
    app.teardown_appcontext(db.close_db)
    app.register_blueprint(website.bp)
    app.register_blueprint(api.bp)

    ############################################################################
    # CLI

    @app.cli.command('init')
    def init():
        """Initializes the database."""
        try:
            db.init_db()
        except sqlite3.Error as e:
            bail(e)

    return app
