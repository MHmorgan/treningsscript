from datetime import datetime, timezone

import math
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session as flask_session,
    send_file,
)

from . import config, exercise, session
from .utils import normalize_date

bp = Blueprint('website', __name__)


@bp.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


@bp.route('/')
def index():
    if 'abort-session' in request.args:
        abort_session()
        return redirect('/')
    if 'finish-session' in request.args:
        finish_session()
        return redirect('/')

    context = {
        'title': 'TrApp',
        'version': config.APP_VERSION,
        'day_types': config.DAY_TYPES,
        'session': flask_session.get('session'),
    }
    return render_template('index.html', **context)


@bp.route('/session')
def session_page():
    if 'session' in flask_session:
        s = flask_session['session']
    elif 'daytype' in request.args:
        start_session(request.args['daytype'])
        s = flask_session['session']
    else:
        return redirect('/')

    cardio_exercises = exercise.get_by_daytype('Cardio')
    core_exercises = exercise.get_by_daytype('Core')
    if s['daytype'] not in ('Cardio', 'Core'):
        exercises = exercise.get_by_daytype(s['daytype'])
    else:
        exercises = []

    context = {
        'title': s['daytype'],
        'session': s,
        'exercises': exercises,
        'cardio_exercises': cardio_exercises,
        'core_exercises': core_exercises,
    }
    return render_template('session.html', **context)


@bp.route('/exercise')
def exercise_page():
    """
    The page for an exercise entry.
    """
    context = {
        'title': 'Create Exercise',
        'session': flask_session.get('session'),
        'day_types': config.DAY_TYPES,
        'weight_types': config.WEIGHT_TYPES,
        'exercise_names': exercise.get_names(),
    }
    return render_template('exercise.html', **context)


@bp.route('/exercise/<name>')
def entry_page(name):
    """
    The page for an exercise entry.
    """
    if 'session' not in flask_session:
        return redirect('/')

    context = {
        'title': name,
        'name': name,
        'exercise': exercise.get(name),
        'session': flask_session['session'],
    }
    return render_template('entry.html', **context)


################################################################################
# Helpers


def start_session(daytype):
    start = datetime.now(config.TZ)
    s = {
        'daytype': daytype,
        'date': normalize_date(start),
        'timestamp': start.timestamp(),
        'iso_date': start.isoformat(),
    }
    flask_session['session'] = s


def finish_session():
    if s := flask_session.get('session'):
        duration = math.floor(datetime.now().timestamp() - s['timestamp'])
        session.new(
            s['date'],
            duration,
            s['daytype'],
        )
        del flask_session['session']


def abort_session():
    if 'session' in flask_session:
        del flask_session['session']
