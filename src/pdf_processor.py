import os
import shutil
import datetime
from typing import Optional

from pdfminer.high_level import extract_text
from pypdf import PdfReader, PdfWriter


def extract_pdf_text(pdf_path: str, page_option: int) -> str:
    """
    PDF からテキストを抽出する関数。

    - page_option = 0   -> テキスト抽出を行わない (空文字)
    - page_option = 1   -> 1ページ目のみ抽出 (デフォルト)
    - page_option = -1  -> 全ページ抽出
    - page_option = n>1 -> nページ目のみ抽出

    例:
      extract_pdf_text("sample.pdf", 0)   -> ""
      extract_pdf_text("sample.pdf", 1)   -> 1ページ目のみ
      extract_pdf_text("sample.pdf", -1)  -> 全ページ
      extract_pdf_text("sample.pdf", 3)   -> 3ページ目のみ
    """
    if not os.path.isfile(pdf_path):
        print(f"Warning: PDFファイルが見つかりません: {pdf_path}")
        return ""

    if page_option == 0:
        # 抽出しない
        return ""

    if page_option == -1:
        # 全ページ
        return extract_text(pdf_path)

    # 1ページ目、あるいは nページ目
    page_index = page_option - 1
    if page_index < 0:
        print(f"Warning: 無効な page_option({page_option}) のため抽出を行いません。")
        return ""

    return extract_text(pdf_path, page_numbers=[page_index])


def apply_pdf_metadata(input_pdf: str,
                       extracted_text: str,
                       output_pdf: Optional[str] = None,
                       config_data: Optional[dict] = None):
    """
    PDF にメタデータを設定して保存する関数。

    公式サンプルに準拠し、
      - /Author
      - /Producer
      - /Title
      - /Subject
      - /Keywords
      - /CreationDate
      - /ModDate
      - /Creator
      - /CustomField
    を登録。

    - extracted_text は /Keywords に格納
    - config_data があればそこから各項目(author, producer, など)を取得し、存在するものだけ登録
    - output_pdf が None なら input_pdf + ".temp.pdf" に書き出す
    """
    if not os.path.isfile(input_pdf):
        print(f"Error: PDFファイルが存在しません: {input_pdf}")
        return

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 全ページをコピー
    for page in reader.pages:
        writer.add_page(page)

    # 既存のメタデータがあれば取り込む
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    # 現在日時を PDF 用にフォーマット
    # 例: D:20250101120000-05'00' (公式サンプルのタイムゾーン例)
    now = datetime.datetime.now()
    utc_time = "-05'00'"
    time_str = now.strftime(f"D:%Y%m%d%H%M%S{utc_time}")

    # config_data から項目を読み取り、デフォルトが必要ならセット
    # なければ登録しない方針の場合は、チェック後にスキップします
    def get_cfg(key: str, default=None):
        """config_data の key を取得し、なければ default を返す"""
        if config_data and key in config_data:
            return config_data[key]
        return default

    author = get_cfg("author", "Martin")       # 例: 無ければ "Martin"
    producer = get_cfg("producer", "Libre Writer")
    title = get_cfg("title", "Title")
    subject = get_cfg("subject", "Subject")
    creator = get_cfg("creator", "Creator")
    custom_field = get_cfg("customfield", "CustomField")

    metadata = {
        "/Author": author,
        "/Producer": producer,
        "/Title": title,
        "/Subject": subject,
        "/Keywords": extracted_text,  # 抽出テキストをKeywordsに入れる
        #"/CreationDate": time_str,
        "/ModDate": time_str,
        "/Creator": creator,
        "/CustomField": custom_field,
    }

    # 値が空文字 or None のものは登録しない
    remove_keys = [k for k, v in metadata.items() if not v]
    for k in remove_keys:
        del metadata[k]

    writer.add_metadata(metadata)

    if output_pdf is None:
        output_pdf = input_pdf + ".temp.pdf"

    with open(output_pdf, "wb") as fp:
        writer.write(fp)


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


def process_single_pdf(pdf_path: str,
                       processed_pdf: str,
                       processed_text: str,
                       config_data: Optional[dict] = None):
    """
    単一PDFを処理するメイン関数。

    1) config_data["page_option"] に従ってテキストを抽出。
       - 無指定なら 1 (1ページ目)
       - 0 なら抽出しない
       - -1 なら全ページ
       - n>1 なら n ページ目のみ
    2) 抽出テキストを /Keywords に格納しつつ、
       Author や Title などを config_data から取得してメタデータ登録
    3) 上書き後に PDF を processed_dir へ移動
    """
    if not os.path.isfile(pdf_path):
        print(f"Error: PDFファイルが存在しません: {pdf_path}")
        return

    if not is_searchable_pdf(pdf_path):
        print(f"Error: 検索可能なPDFではありません。: {pdf_path}")
        return

    # config_data からページ設定を取得。無ければ 1(1ページ目)
    if config_data and "page_option" in config_data:
        try:
            page_option = int(config_data["page_option"])
        except ValueError:
            print(f"Warning: page_option が整数値ではありません: {config_data['page_option']}")
            page_option = -1
    else:
        page_option = -1

    # 1) PDFテキスト抽出
    extracted = extract_pdf_text(pdf_path, page_option)

    # 2) メタデータ設定
    #temp_pdf = pdf_path + ".temp.pdf"
    #apply_pdf_metadata(
    #    input_pdf=pdf_path,
    #    extracted_text=extracted,
    #    output_pdf=temp_pdf,
    #    config_data=config_data
    #)
    # 元ファイルを削除してリネーム
    #os.remove(pdf_path)
    #os.rename(temp_pdf, pdf_path)
    
    text_file_path = os.path.splitext(pdf_path)[0] + ".search.txt"
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(extracted)


    # 3) 処理後ディレクトリへ移動
    #if not os.path.exists(processed_dir):
    #    os.makedirs(processed_dir, exist_ok=True)

    pdf_dst_path = os.path.join(processed_pdf, os.path.basename(pdf_path))
    text_dst_path = os.path.join(processed_text, os.path.basename(text_file_path))
    shutil.move(pdf_path, pdf_dst_path)
    shutil.move(text_file_path, text_dst_path)
    print(f"[OK] Processed PDF2Text: {text_file_path}")
