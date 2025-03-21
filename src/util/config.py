from pathlib import Path
from pydantic import BaseModel
import yaml
from typing import Optional
import yaml
import gettext
import os

class DeployConfig(BaseModel):
    environment: str
    region: str
    bucket: str

class ProjectConfig(BaseModel):
    name: str
    version: str

class PdfConfig(BaseModel):
    author: Optional[str]
    producer: Optional[str]
    title: Optional[str]
    subject: Optional[str]
    creator: Optional[str]
    customfield: Optional[str]
    page_option: int

class DefaultConfig(BaseModel):
    lang: str
    directory: str
    processed_pdf: str
    processed_text: str
    llm_models: str
    interval: int

class AppConfig(BaseModel):
    project: ProjectConfig
    deploy: DeployConfig
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
