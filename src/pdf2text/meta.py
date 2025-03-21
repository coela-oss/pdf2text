from pdfminer.high_level import extract_text


def is_searchable_pdf(pdf_path):
    """
    PDFが検索可能（テキストデータを含む）かどうかを判定する関数。

    Args:
        pdf_path (str): PDFファイルのパス
    
    Returns:
        bool: Trueなら検索可能、Falseなら画像のみのPDF
    """
    try:
        extracted_text = extract_text(pdf_path).strip()
        return bool(extracted_text)  # テキストが存在すれば検索可能
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False
