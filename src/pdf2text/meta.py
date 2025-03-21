from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from util.convert import parse_pdf_date
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTImage
from typing import Dict, Any, Union


def safe_decode(value: Union[bytes, str]) -> str:
    """
    PDFメタデータの値を安全にデコードするための関数。
    UTF-16BE BOM を検出して適切にデコードし、それ以外は fallback あり。
    """
    if isinstance(value, bytes):
        try:
            # UTF-16BE with BOM
            if value.startswith(b'\xfe\xff') or value.startswith(b'\xff\xfe'):
                return value.decode('utf-16')
            # UTF-8 or ASCII
            return value.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return value.decode('latin-1')
            except Exception:
                return repr(value)  # バイナリそのままを文字列で表現
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def extract_pdf_metadata(file_path: str) -> Dict[str, str]:
    """
    PDFのメタデータを抽出し、文字列に変換して返す。
    """
    metadata = {}

    with open(file_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        if hasattr(doc, 'info') and isinstance(doc.info, list) and doc.info:
            info = doc.info[0]
            for key, value in info.items():
                key_str = safe_decode(key)
                val_str = safe_decode(value)
                if "Date" in key:
                    val_str = parse_pdf_date(val_str)
                metadata[key_str] = val_str

    return metadata


def analyze_pdf_pages_with_summary(file_path: str) -> Dict[str, Any]:
    """
    PDF各ページにテキストが含まれるか、画像のみかを判定し、集計も返す。

    :param file_path: PDFファイルのパス
    :return: ページごとの結果と集計を含む辞書
    """
    page_results = []
    summary = {
        "total_pages": 0,
        "text_pages": 0,
        "image_only_pages": 0,
        "blank_pages": 0,
    }

    for page_number, layout in enumerate(extract_pages(file_path), start=1):
        has_text = False
        has_image = False

        for element in layout:
            if isinstance(element, LTTextContainer):
                if element.get_text().strip():
                    has_text = True
            elif isinstance(element, LTImage):
                has_image = True

        is_image_only = not has_text and has_image
        is_blank = not has_text and not has_image

        result = {
            "page": page_number,
            "has_text": has_text,
            "has_image": has_image,
            "is_image_only": is_image_only,
            "is_blank": is_blank,
        }

        page_results.append(result)

        # 集計
        summary["total_pages"] += 1
        if has_text:
            summary["text_pages"] += 1
        elif is_image_only:
            summary["image_only_pages"] += 1
        elif is_blank:
            summary["blank_pages"] += 1

    return {
        "pages": page_results,
        "summary": summary
    }
