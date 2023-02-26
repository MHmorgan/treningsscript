from datetime import datetime

import math
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session as flask_session,
)

from . import config, exercise, session
from .utils import normalize_date

bp = Blueprint('website', __name__)


@bp.route('/')
def index():
    if 'abort-session' in request.args:
        if 'session' in flask_session:
            del flask_session['session']
        return redirect('/')
    if 'finish-session' in request.args:
        if s := flask_session.get('session'):
            duration = math.floor(datetime.now().timestamp() - s['timestamp'])
            session.new(
                s['date'],
                duration,
                s['daytype'],
            )
            del flask_session['session']
        return redirect('/')

    context = {
        'title': 'Trapp',
        'day_types': config.DAY_TYPES,
        'session': flask_session.get('session'),
    }
    return render_template('index.html', **context)


@bp.route('/session')
def session_page():
    if 'session' in flask_session:
        s = flask_session['session']
    elif 'daytype' in request.args:
        start = datetime.now()
        s = {
            'daytype': request.args['daytype'],
            'date': normalize_date(start),
            'timestamp': start.timestamp(),
        }
        flask_session['session'] = s
    else:
        return redirect('/')

    context = {
        'title': s['daytype'],
        'session': s,
        'exercises': exercise.get_session_exercises(s['daytype']),
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
