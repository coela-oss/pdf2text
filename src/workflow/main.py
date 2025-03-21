from invoke import task
from util.config import config
from util.config import _
from pdf2text.extract import extract_pdf_text

@task(help={"name": _("Extract Pdf")})
def extract_pdf(c, path="./"):
    text = extract_pdf_text(path, config.pdf.page_option)
    print(f'Extract PDF Text: {text}')
