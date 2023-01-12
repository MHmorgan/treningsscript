import json
import sqlite3
from collections import UserDict

from .utils import normalize_date
from .exceptions import AppError


class Warmup(UserDict):
    name: str
    entries: list[dict[str, any]]

    __properties__ = ('name', 'entries')

    def __getattr__(self, item):
        if item in self.__properties__:
            return self.data.get(item)
        raise AttributeError(f'no such property: {item}')

    def __setattr__(self, key, value):
        if key in self.__properties__:
            self.data[key] = value
        else:
            super().__setattr__(key, value)

    @classmethod
    def new(cls, name):
        return cls({'name': name, 'entries': []})

    @classmethod
    def from_row(cls, row):
        """Creates an Warmup object from a database row."""
        return cls(json.loads(row['object']))

    def to_json(self, **kwargs):
        return json.dumps(self.data, **kwargs)

    def add_entry(self, date, intervals):
        try:
            assert isinstance(intervals, list), 'intervals must be a list'
            assert all(isinstance(i, int) for i in intervals), 'intervals must integers'
        except AssertionError as e:
            raise AppError(f'bad warmup entry: {e}') from e

        self['entries'].append({
            'date': normalize_date(date),
            'intervals': intervals,
        })

    def db_insert(self, cur):
        """Inserts the exercise into the database."""
        sql = '''
            INSERT INTO Warmups (name, object)
            VALUES (?, ?)
        '''
        values = (self.name, self.to_json())
        try:
            cur.execute(sql, values)
        except sqlite3.IntegrityError as e:
            raise AppError(f'insert {self.name!r}: {e}') from e

    def db_update(self, cur):
        """Updates the exercise in the database."""
        sql = '''
            UPDATE Warmups
            SET object=?
            WHERE name=?
        '''
        values = (self.to_json(), self.name)
        try:
            cur.execute(sql, values)
        except sqlite3.IntegrityError as e:
            raise AppError(f'update {self.name!r}: {e}') from e


def new(cur, name):
    ex = Warmup.new(name)
    ex.db_insert(cur)


def get_all(cur):
    sql = 'SELECT object FROM Warmups ORDER BY name'
    return [
        Warmup.from_row(row)
        for row in cur.execute(sql)
    ]


def get(cur, name):
    sql = 'SELECT object FROM Warmups WHERE name = ?'
    row = cur.execute(sql, (name,)).fetchone()
    if row is None:
        raise AppError(f'no exercise named {name}')
    return Warmup.from_row(row)


def add_entry(cur, name, date, intervals):
    ex = get(cur, name)
    ex.add_entry(date, intervals)
    ex.db_update(cur)
