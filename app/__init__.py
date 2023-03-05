from os import environ

from flask import (
    Flask
)

from . import (
    api,
    cli,
    db,
    website
)


def create_app():
    app = Flask(__name__)

    app.secret_key = environ.get(
        'SECRET_KEY',
        'a2e112dafab36433dab1a5ff173df9ae9f8dcfed854cb4663c0e6af81c3ae3cf'
    )
    app.teardown_appcontext(db.close)
    app.register_blueprint(website.bp)
    app.register_blueprint(api.bp)

    cli.setup(app)

    with app.app_context():
        db.init()

    return app
