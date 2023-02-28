import json
import sqlite3
from dataclasses import dataclass

from . import config, db
from .utils import normalize_date
from .exceptions import AppError


@dataclass
class Session:
    date: str
    length: float
    daytype: str

    id: int = None

    @classmethod
    def new(cls, date, length, daytype):
        date = normalize_date(date)

        try:
            assert length is None or isinstance(length, (float, int)),\
                'length must be a number'
            assert daytype in config.DAY_TYPES, 'invalid day type'
        except AssertionError as e:
            raise AppError(f'bad session: {e}') from e

        return cls(date, length, daytype)

    @property
    def data(self):
        return {
            'id': self.id,
            'date': self.date,
            'length': self.length,
            'daytype': self.daytype,
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            date=row['date'],
            length=row['length'],
            daytype=row['daytype'],
        )

    def to_json(self, **kwargs):
        return json.dumps(self.data, **kwargs)

    def db_insert(self, cur):
        sql = '''
            INSERT INTO Sessions (date, length, daytype)
            VALUES (?, ?, ?)
        '''
        values = (self.date, self.length, self.daytype)
        try:
            cur.execute(sql, values)
        except sqlite3.IntegrityError as e:
            raise AppError(f'insert session: {e}') from e


def new(date, length, daytype):
    se = Session.new(date, length, daytype)
    with db.get_con() as con:
        se.db_insert(con.cursor())


def get_all():
    sql = '''
        SELECT ROWID as id, *
        FROM Sessions
        ORDER BY date DESC
    '''
    with db.get_con() as con:
        cur = con.execute(sql)
        return [
            Session.from_row(row)
            for row in cur.fetchall()
        ]
