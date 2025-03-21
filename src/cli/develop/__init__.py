import click
from cli.develop.locale import locale

@click.group(help="Developer commands")
def develop():
    pass

develop.add_command(locale)
