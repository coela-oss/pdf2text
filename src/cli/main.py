import click
from invoke import Context
from cli.develop import develop
from workflow.main import meta_pdf
from workflow.main import extract_pdf
from util.config import _

@click.group(help=_("PDF2TEXT Task Runners"))
def entry():
    pass


@entry.command(help=_("Extract text Data from PDF"))
@click.option("--path", required=True, help=_("Path to the PDF"))
def extract(path):
    ctx = Context()
    extract_pdf(ctx, path=path)

@entry.command(help=_("Extract Meta Info from PDF"))
@click.option("--path", required=True, help=_("Path to the PDF"))
def meta(path):
    ctx = Context()
    meta_pdf(ctx, path=path)


entry.add_command(develop)

if __name__ == "__main__":
    entry()
