from flask import (
    Blueprint,
    request
)

from . import (
    db,
    exercise,
    session,
)
from .exceptions import AppError

bp = Blueprint('api', __name__, url_prefix='/api')


############################################################################
# Exercises

@bp.route('/exercises')
def all_exercises():
    """
    Get a JSON list of all exercises.
    """
    return [e.data for e in exercise.get_all()]


@bp.route('/exercises', methods=['POST'])
def add_exercise():
    """
    Add a new exercise to the database.
    The exercise must be a JSON exercise-object.
    """
    data = request.json
    try:
        exercise.new(data['name'], data['weighttype'], data['daytype'])
    except KeyError as e:
        return f'exercise object missing: {e}', 400
    except AppError as e:
        return str(e), 400
    return 'Created', 201


@bp.route('/exercises/<exercise_name>')
def get_exercise(exercise_name):
    """
    Get a JSON representation of an exercise.
    """
    return exercise.get(exercise_name).data


@bp.route('/exercises/<exercise_name>', methods=['POST'])
def add_exercise_entry(exercise_name):
    """
    Add a new entry to an exercise. The exercise must already exist.
    The entry must be a JSON entry-object.
    """
    data = request.json
    try:
        exercise.add_entry(
            exercise_name,
            data['date'],
            data['reps'],
            data['sets'],
            data.get('weight'),
            data.get('rpe')
        )
    except KeyError as e:
        return f'exercise entry missing: {e}', 400
    except AppError as e:
        return str(e), 400
    return 'Created', 201


############################################################################
# Sessions

@bp.route('/sessions')  # Date range?
def all_sessions():
    with db.cursor() as cur:
        ses = session.get_all(cur)
    return [s.data for s in ses]


@bp.route('/sessions', methods=['POST'])
def add_session():
    data = request.json
    try:
        session.new(data['date'], data['length'], data['daytype'])
    except KeyError as e:
        return f'Session missing: {e}', 400
    except AppError as e:
        return str(e), 400
    return 'Created', 201
