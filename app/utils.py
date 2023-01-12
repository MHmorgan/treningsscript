import json
from datetime import datetime

from .exceptions import AppError


def normalize_date(date):
    if not isinstance(date, datetime):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            raise AppError(f'invalid date format {date!r}')
    return date.strftime('%Y-%m-%d')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return normalize_date(o)
        try:
            return o.data
        except AttributeError:
            pass
        return super().default(o)


def to_json(obj, **kwargs):
    return json.dumps(obj, cls=JSONEncoder, **kwargs)
