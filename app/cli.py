import click
from click import echo, secho

from . import (
    config,
    db,
    exercise,
    session,
)
from .exceptions import AppError
from .exercise import Exercise


def bail(msg):
    secho(f'[!!] {msg}', err=True, fg='red')
    exit(1)


def setup(app):
    @app.cli.command('version')
    def version():
        """Display application/schema version."""
        echo(f'App version: {config.APP_VERSION}')
        echo(f'Schema version: {db.get_meta("schema_version") or "?"}')

    ############################################################################
    # Exercises

    @app.cli.group('exercises')
    def exercises():
        """Manage exercises."""

    @exercises.command('list')
    @click.option('-d', '--daytype', type=click.Choice(config.DAY_TYPES))
    def list_exercises(daytype):
        """List all exercises."""
        try:
            if daytype:
                exs = exercise.get_by_daytype(daytype)
            else:
                exs = exercise.get_all()

            if not exs:
                echo('No exercises found.')
                return

            w = max(len(ex.name) for ex in exs)
            for ex in exs:
                n = len(ex.entries)
                echo(f'{ex.name:{w}}\t{ex.daytype}\t{ex.weighttype:8}\t{n} entries')

        except AppError as e:
            bail(e)

    @exercises.command('show')
    @click.argument('name')
    def show_exercise(name):
        """Show details of an exercise."""
        try:
            ex = exercise.get(name)

            echo(f'Name: {ex.name}')
            echo(f'Day type: {ex.daytype}')
            echo(f'Weight type: {ex.weighttype}')
            echo(f'Entries: {len(ex.entries)}')
            echo('')

            if not ex.entries:
                return
            echo('\n'.join(map(Exercise.entry_str, ex.entries)))

        except AppError as e:
            bail(e)

    @exercises.command('rm-entry')
    @click.argument('name')
    @click.argument('date')
    def rm_entry(name, date):
        """Remove an entry from an exercise."""
        try:
            exercise.remove_entry(name, date)
        except AppError as e:
            bail(e)

    ############################################################################
    # Sessions

    @app.cli.group('sessions')
    def sessions():
        """Manage sessions."""

    @sessions.command('list')
    def list_sessions():
        """List all sessions."""
        try:
            s = session.get_all()
        except AppError as e:
            bail(e)
        echo('\n'.join(map(str, s)))

    @sessions.command('new')
    @click.argument('date')
    @click.argument('length', type=int)
    @click.argument('daytype', type=click.Choice(config.DAY_TYPES))
    def new_session(date, length, daytype):
        """Create a new session."""
        try:
            session.new(date, length, daytype)
        except AppError as e:
            bail(e)

    @sessions.command('delete')
    @click.argument('id', type=int)
    def delete_session(id):
        """Delete a session."""
        try:
            session.delete(id)
        except AppError as e:
            bail(e)
