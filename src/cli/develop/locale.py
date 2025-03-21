from pathlib import Path
from util.config import _
import click
from pathlib import Path
import subprocess

@click.group(help="Locale-related tasks")
def locale():
    pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
LOCALE_DIR = BASE_DIR / "locales"
#BABEL_CFG = BASE_DIR / "babel.cfg"
POT_FILE = LOCALE_DIR / "messages.pot"

@click.command(help=_("Extract, update, and compile translation files"))
@click.option('--lang', '-l', multiple=True, help=_("Target languages (e.g. ja, en)"))
def update(lang):
    """CLIから翻訳ファイルの一括更新を実行"""
    click.echo(_("Extracting messages..."))
    subprocess.run([
        "pybabel", "extract",
        #"-F", str(BABEL_CFG),
        "-o", str(POT_FILE),
        str(BASE_DIR)
    ], check=True)

    langs = lang or ["ja", "en"]
    for lng in langs:
        click.echo(_("Updating translation for: %s") % lng)
        subprocess.run([
            "pybabel", "update",
            "-i", str(POT_FILE),
            "-d", str(LOCALE_DIR),
            "-l", lng
        ], check=True)

    click.echo(_("Compiling .po to .mo..."))
    subprocess.run([
        "pybabel", "compile",
        "-d", str(LOCALE_DIR)
    ], check=True)

    click.echo(_("All translations updated successfully."))

locale.add_command(update)
