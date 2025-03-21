from invoke import task
from util.config import config
from util.config import _
from pdf2text.extract import extract_pdf_text
from pdf2text.meta import analyze_pdf_pages_with_summary, extract_pdf_metadata

@task(help={"name": _("Extract Pdf")})
def extract_pdf(c, path="./"): # TODO Path or Stored PDF UUID
    text = extract_pdf_text(path, config.pdf.page_option)
    print(f'Extract PDF Text: {text}')

@task(help={"name": _("Get Meta Info Pdf")})
def meta_pdf(c, path="./"):
    text = extract_pdf_metadata(path)
    text2 = analyze_pdf_pages_with_summary(path)

    print(f'Extract PDF Meta Info: {text}')
    print(f'Extract PDF Meta Pages Info: {text2}')
