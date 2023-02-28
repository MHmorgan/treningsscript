from os import environ

from click import echo, secho
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

    app.secret_key = environ.get(
        'SECRET_KEY',
        'a2e112dafab36433dab1a5ff173df9ae9f8dcfed854cb4663c0e6af81c3ae3cf'
    )
    app.teardown_appcontext(db.close)
    app.register_blueprint(website.bp)
    app.register_blueprint(api.bp)

    with app.app_context():
        db.init()

    @app.cli.command('version')
    def version():
        """Print version."""
        echo(f'App version: {config.APP_VERSION}')
        echo(f'Schema version: {db.get_meta("schema_version") or "?"}')

    return app
