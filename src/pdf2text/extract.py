import os
from pdfminer.high_level import extract_text


def extract_pdf_text(pdf_path: str, page_option: int) -> str:
    """
    PDF からテキストを抽出する関数
    - page_option = 0   -> 全ページ抽出(default)
    - page_option = n>1 -> nページ目のみ抽出
    """
    if not os.path.isfile(pdf_path):
        print(f"Warning: PDFファイルが見つかりません: {pdf_path}")
        return ""

    if page_option == 0:
        return extract_text(pdf_path)

    if page_option < 0:
        print(f"Warning: 無効な page_option({page_option}) のため抽出を行いません。")
        return ""

    return extract_text(pdf_path, page_numbers=[page_option])
