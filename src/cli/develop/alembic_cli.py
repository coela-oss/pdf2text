from pathlib import Path
import subprocess
import click
from util.config import _ 

@click.group(help="Alembic-related tasks")
def db():
    pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ALEMBIC_DIR = BASE_DIR / "alembic"

@click.command(help=_("Generate and apply Alembic migration"))
@click.option('--message', '-m', default="Auto migration", help=_("Revision message"))
@click.option('--autogenerate/--no-autogenerate', default=True, help=_("Use autogenerate"))
def migrate(message, autogenerate):
    """alembic revision + upgrade をまとめて実行"""
    click.echo(_("Creating Alembic revision: ") + message)
    
    cmd = ["alembic", "revision", "-m", message]
    if autogenerate:
        cmd.append("--autogenerate")
    
    subprocess.run(cmd, cwd=BASE_DIR, check=True)

    click.echo(_("Applying migration..."))
    subprocess.run(["alembic", "upgrade", "head"], cwd=BASE_DIR, check=True)

    click.echo(_("Migration complete."))

db.add_command(migrate)
