import json
import sqlite3
from collections import UserDict

from . import config
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

    def add_entry(self, date, reps, sets, weight=None, onerepmax=None):
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
            'onerepmax': onerepmax,
        })

    def db_insert(self, cur):
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

    def db_update(self, cur):
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


def new(cur, name, weighttype, daytype):
    ex = Exercise.new(name, daytype, weighttype)
    ex.db_insert(cur)


def get_all(cur):
    sql = 'SELECT object FROM Exercises ORDER BY name'
    return [
        Exercise.from_row(row)
        for row in cur.execute(sql)
    ]


def get_by_daytype(cur, daytype):
    sql = f'''
        SELECT object
        FROM Exercises
        WHERE daytype = ?
        ORDER BY name
    '''
    return [
        Exercise.from_row(row)
        for row in cur.execute(sql, (daytype,))
    ]


def get(cur, name):
    sql = 'SELECT object FROM Exercises WHERE name = ?'
    row = cur.execute(sql, (name,)).fetchone()
    if row is None:
        raise AppError(f'No exercise named {name}')
    return Exercise.from_row(row)


def add_entry(cur, name, date, reps, sets, weight=None, onerepmax=None):
    date = normalize_date(date)
    ex = get(cur, name)
    ex.add_entry(date, reps, sets, weight, onerepmax)
    ex.db_update(cur)
