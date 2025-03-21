from pathlib import Path
from pydantic import BaseModel
import yaml
import yaml
import gettext
import os

class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    dbname: str

class PdfConfig(BaseModel):
    page_option: int

class DefaultConfig(BaseModel):
    lang: str

class AppConfig(BaseModel):
    database: DatabaseConfig
    pdf: PdfConfig
    default: DefaultConfig


def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return AppConfig(**raw)

def setup_i18n(lang="en"):
    root_dir = Path(__file__).resolve().parent.parent.parent
    localedir = os.path.join(root_dir, 'locales')
    gettext.bindtextdomain('messages', localedir)
    gettext.textdomain('messages')
    return gettext.translation('messages', localedir, languages=[lang], fallback=True).gettext

config = load_config()
_ = setup_i18n(config.default.lang)
