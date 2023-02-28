import json
import sqlite3
from collections import UserDict
from functools import cached_property
from datetime import datetime

from . import config, db
from .utils import normalize_date
from .exceptions import AppError


class Exercise(UserDict):
    name: str
    daytype: str
    weighttype: str
    entries: list[dict[str, any]]

    __properties__ = ('name', 'daytype', 'weighttype', 'entries')

    def __getattr__(self, item):
        if item in self.__properties__:
            return self.data.get(item)
        raise AttributeError(f'No such property: {item}')

    def __setattr__(self, key, value):
        if key in self.__properties__:
            self.data[key] = value
        else:
            super().__setattr__(key, value)

    @classmethod
    def new(cls, name, daytype, weighttype):
        try:
            assert daytype in config.DAY_TYPES, 'invalid day type'
            assert weighttype in config.WEIGHT_TYPES, 'invalid weight type'
        except AssertionError as e:
            raise AppError(f'bad exercise: {e}') from e

        return cls({
            'name': name,
            'daytype': daytype,
            'weighttype': weighttype,
            'entries': [],
        })

    @classmethod
    def from_row(cls, row):
        """Creates an Exercise object from a database row."""
        return cls(json.loads(row['object']))

    def to_json(self, **kwargs):
        return json.dumps(self.data, **kwargs)

    @cached_property
    def latest_entry(self):
        """Return the latest entry."""
        if not self.entries:
            return None
        return max(self.entries, key=lambda e: e['date'])

    def latest_date(self):
        """Return the normalized date string of the latest entry."""
        if entry := self.latest_entry:
            return normalize_date(entry['date'])
        return 'never'

    def latest_reps(self):
        """Return the reps of the latest entry."""
        if entry := self.latest_entry:
            return entry['reps']
        return ''

    def latest_sets(self):
        """Return the sets of the latest entry."""
        if entry := self.latest_entry:
            return entry['sets']
        return ''

    def latest_weight(self):
        """Return the weight of the latest entry."""
        if entry := self.latest_entry:
            return entry.get('weight', '')
        return ''

    def latest_rpe(self):
        """Return the one rep max of the latest entry."""
        if entry := self.latest_entry:
            return entry.get('rpe', '')
        return ''

    def add_entry(self, date, reps, sets, weight=None, rpe=None):
        try:
            reps = int(reps)
            sets = int(sets)
            date = normalize_date(date)
        except (ValueError, AppError) as e:
            raise AppError(f'bad exercise entry: {e}') from e

        self['entries'].append({
            'date': date,
            'weight': weight,
            'reps': reps,
            'sets': sets,
            'rpe': rpe,
        })

    def db_insert(self, cur: sqlite3.Cursor):
        """Inserts the exercise into the database."""
        sql = '''
            INSERT INTO Exercises (name, daytype, object)
            VALUES (?, ?, ?)
        '''
        values = (self.name, self.daytype, self.to_json())
        try:
            cur.execute(sql, values)
        except sqlite3.IntegrityError as e:
            raise AppError(f'insert {self.name!r}: {e}') from e

    def db_update(self, cur: sqlite3.Cursor):
        """Updates the exercise in the database."""
        sql = '''
            UPDATE Exercises
            SET object=?
            WHERE name=?
        '''
        values = (self.to_json(), self.name)
        try:
            cur.execute(sql, values)
        except sqlite3.IntegrityError as e:
            raise AppError(f'update {self.name!r}: {e}') from e


def new(name, weighttype, daytype):
    ex = Exercise.new(name, daytype, weighttype)
    with db.get_con() as con:
        ex.db_insert(con.cursor())


def get_all():
    sql = 'SELECT object FROM Exercises ORDER BY name'
    with db.get_con() as con:
        cur = con.cursor()
        return [
            Exercise.from_row(row)
            for row in cur.execute(sql)
        ]


def get_names():
    sql = 'SELECT name FROM Exercises ORDER BY name'
    with db.get_con() as con:
        return [row['name'] for row in con.execute(sql)]


def get_by_daytype(daytype):
    sql = f'''
        SELECT object
        FROM Exercises
        WHERE daytype = ?
        ORDER BY name
    '''
    with db.get_con() as con:
        return [
            Exercise.from_row(row)
            for row in con.execute(sql, (daytype,))
        ]


def get_session_exercises(daytype):
    """
    Returns a list of exercises for the given day type.
    Also handles cardio exercises.
    """
    if daytype != 'Cardio':
        lst = get_by_daytype('Cardio')
        today = normalize_date(datetime.today())
        if any(ex.latest_date() == today for ex in lst):
            lst.clear()
    else:
        lst = []

    lst.extend(get_by_daytype(daytype))
    return lst


def get(name):
    """
    Returns an Exercise object for the given name.
    Raises AppError if no such exercise exists.
    """
    sql = 'SELECT object FROM Exercises WHERE name = ?'
    with db.get_con() as con:
        row = con.execute(sql, (name,)).fetchone()
    if row is None:
        raise AppError(f'No exercise named {name}')
    return Exercise.from_row(row)


def add_entry(name, date, reps, sets, weight=None, rpe=None):
    """
    Adds an entry to the exercise with the given name.
    Raises AppError if no such exercise exists.
    """
    date = normalize_date(date)
    sql = 'SELECT object FROM Exercises WHERE name = ?'

    with db.get_con() as con:
        cur = con.cursor()
        if row := cur.execute(sql, (name,)).fetchone():
            ex = Exercise.from_row(row)
        else:
            raise AppError(f'No exercise named {name}')
        ex.add_entry(date, reps, sets, weight, rpe)
        ex.db_update(cur)
