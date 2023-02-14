import os

from flask import Flask, request, send_from_directory
from werkzeug.exceptions import BadRequest

from . import (
    config,
    db,
    exercise,
    session,
)
from .exceptions import AppError


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/<any>')
    def catchall(*args, **kwargs):
        return send_from_directory('static', 'index.html')

    @app.route('/js/<path:path>')
    def static_proxy(path):
        return send_from_directory('static/js', path)

    ############################################################################
    # Exercises

    @app.route('/api/exercises')  # Filter by tags
    def all_exercises():
        with db.cursor() as cur:
            exs = exercise.get_all(cur)
        return [e.data for e in exs]

    @app.route('/api/exercises', methods=['POST'])
    def add_exercise():
        data = request.json
        with db.cursor() as cur:
            try:
                exercise.new(cur, data['name'], data['weighttype'], data['daytype'])
            except KeyError as e:
                raise BadRequest(f'exercise missing: {e}')
            except AppError as e:
                raise BadRequest(str(e))
        return 'Created', 201

    @app.route('/api/exercises/<exercise_name>')
    def get_exercise(exercise_name):
        with db.cursor() as cur:
            ex = exercise.get(cur, exercise_name)
        return ex.data

    @app.route('/api/exercises/<exercise_name>', methods=['POST'])
    def add_exercise_entry(exercise_name):
        data = request.json
        with db.cursor() as cur:
            try:
                ex = exercise.get(cur, exercise_name)
                ex.add_entry(data['date'], data['reps'], data['weight'], data['onerepmax'])
                ex.db_update(cur)
            except KeyError as e:
                raise BadRequest(f'exercise entry missing: {e}')
            except AppError as e:
                raise BadRequest(str(e))
        return 'Created', 201

    ############################################################################
    # Sessions

    @app.route('/api/sessions')  # Date range?
    def all_sessions():
        with db.cursor() as cur:
            ses = session.get_all(cur)
        return [s.data for s in ses]

    @app.route('/api/sessions', methods=['POST'])
    def add_session():
        data = request.json
        with db.cursor() as cur:
            try:
                session.new(cur, data['date'], data['length'], data['daytype'])
            except AppError as e:
                raise BadRequest(str(e))
            except KeyError as e:
                raise BadRequest(f'Session missing: {e}')
        return 'Created', 201

    if not os.path.exists(config.DATABASE):
        db.init()

    return app
