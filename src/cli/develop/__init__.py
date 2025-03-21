import click
from cli.develop.locale import locale
from cli.develop.alembic_cli import db

@click.group(help="Developer commands")
def develop():
    pass

develop.add_command(locale)
develop.add_command(db)
