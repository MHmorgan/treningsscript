import os
import secrets
import sqlite3

from click import secho
from flask import (
    Flask
)

from . import (
    api,
    config,
    db,
    website
)


def bail(msg):
    secho(f'[!!] {msg}', err=True, fg='red')
    exit(1)


def create_app():
    app = Flask(__name__)

    app.secret_key = secrets.token_urlsafe()
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

    if not os.path.exists(config.DATABASE):
        db.init()

    return app
