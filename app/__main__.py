import json
import sys

import click
from click import echo, secho, style

# Must import everything "from app" to
# get the app context.
import app
from app import (
    config,
    db,
    exercise,
    session,
)
from app.exceptions import AppError
from app.utils import to_json


@click.group()
def cli():
    pass


@cli.command()
@click.argument('host', default='0.0.0.0')
@click.argument('port', default=8000)
def web(host, port):
    """Run the web server."""
    app.create_app().run(host=host, port=port)


@cli.command()
def initdb():
    """Initialize the database."""
    db.init()


# Exercises

@cli.group()
def exercises():
    """Manage exercises."""
    pass


@exercises.command('new')
@click.argument('name')
@click.argument('weighttype', type=click.Choice(config.WEIGHT_TYPES))
@click.argument('daytype', type=click.Choice(config.DAY_TYPES))
def new_exercise(name, weighttype, daytype):
    """Create a new exercise."""
    with db.cursor() as cur:
        exercise.new(cur, name, weighttype, daytype)


@exercises.command('list')
@click.option('--daytype', '-d', type=click.Choice(config.DAY_TYPES))
def list_exercises(daytype):
    """List exercises."""
    with db.cursor() as cur:
        if daytype:
            exs = exercise.get_by_daytype(cur, daytype)
        else:
            exs = exercise.get_all(cur)

    if not exs:
        echo('No exercises found.')
        return

    name_width = max(len(e['name']) for e in exs)
    for e in exs:
        pprint_exercise(e, name_width=name_width)


@exercises.command('dump')
@click.option('--daytype', '-d', type=click.Choice(config.DAY_TYPES))
def dump_exercises(daytype):
    """Dump exercises as JSON."""
    with db.cursor() as cur:
        if daytype:
            exs = exercise.get_by_daytype(cur, daytype)
        else:
            exs = exercise.get_all(cur)
    echo(to_json(exs, indent=2))


@exercises.command()
@click.argument('name')
@click.option('--json', 'json_out', is_flag=True)
def show(name, json_out):
    """Show an exercise."""
    with db.cursor() as cur:
        ex = exercise.get(cur, name)

    if json_out:
        json.dump(ex, sys.stdout, indent=2)
        return

    pprint_exercise(ex, with_entries=True)


@exercises.command()
@click.argument('name')
@click.argument('date', type=click.DateTime())
@click.argument('reps', type=int)
@click.argument('sets', type=int)
@click.option('-w', '--weight', type=float)
@click.option('-r', '--onerepmax', type=int)
def entry(name, date, weight, onerepmax, reps, sets):
    """Add an entry to an exercise."""
    with db.cursor() as cur:
        exercise.add_entry(cur, name, date, reps, sets, weight, onerepmax)


@exercises.command()
@click.argument('name')
@click.argument('num', type=int)
def delete_entry(name, num):
    """Delete an entry from an exercise."""
    with db.cursor() as cur:
        ex = exercise.get(cur, name)
        if num > len(ex['entries']) or num < 1:
            secho('Invalid entry number.', fg='red')
            return
        del ex['entries'][num - 1]
        ex.db_update(cur)


# Session

@cli.group()
def sessions():
    """Manage sessions."""
    pass


@sessions.command('dump')
def dump_sessions():
    """Dump sessions as JSON."""
    with db.cursor() as cur:
        ses = session.get_all(cur)
    echo(to_json(ses, indent=2))


# Utils

def pprint_exercise(e, with_entries=False, name_width=0):
    name = style(f'{e["name"]:<{name_width}}', bold=True)
    num = len(e['entries'])
    echo(f'{name}  {e["weighttype"]:<10}  {num} entries  {e["daytype"]:<5}')

    if not (e['entries'] and with_entries):
        return

    echo('Entries:')
    for i, entry in enumerate(e['entries']):
        date = entry['date']
        weight = entry['weight'] or '?'
        reps = entry['reps']
        sets = entry['sets']
        onerepmax = entry['onerepmax'] or '?'
        echo(f'{i+1}. {date}  {reps} reps {sets} sets  {weight}kg  {onerepmax} 1RM')


if __name__ == '__main__':
    try:
        cli()
    except AppError as e:
        secho(e, fg='red')
        sys.exit(1)
