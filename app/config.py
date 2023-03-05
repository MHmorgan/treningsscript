
from os import environ
from datetime import datetime

APP_VERSION = '1.3.1'
SCHEMA_VERSION = 0

DATABASE = environ.get('DATABASE', 'db.sqlite')

WEIGHT_TYPES = (
    'Total',
    'Each Arm',
    'Each Leg',
    'Bodyweight'
)

DAY_TYPES = (
    'Push',
    'Pull',
    'Legs',
    'Core',
    'Cardio'
)

TZ = datetime.now().astimezone().tzinfo
