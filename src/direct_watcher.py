# direct_watcher.py

import os
import sys
import time

from pdf_processor import process_single_pdf

def direct_watch(directory: str,
                 processed_dir: str,
                 interval: int,
                 config_data=None):
    """
    フォアグラウンドでディレクトリを一定間隔スキャンしてPDFを検知・処理する。
    config_data に page_option があれば、それに従ってテキスト抽出範囲を決定。
    """
    if not os.path.exists(directory):
        print(f"Error: 監視ディレクトリが存在しません: {directory}")
        sys.exit(1)

    processed_files = set()
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".pdf"):
                processed_files.add(os.path.join(root, f))

    print(f"[direct] Start watching: {directory} (interval={interval}s)")
    try:
        while True:
            for root, dirs, files in os.walk(directory):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        full_path = os.path.join(root, f)
                        if full_path not in processed_files:
                            processed_files.add(full_path)
                            print(f"[Detected new PDF] {full_path}")
                            try:
                                # config_data に page_option 等が含まれていれば
                                # process_single_pdf 内で参照
                                process_single_pdf(
                                    pdf_path=full_path,
                                    processed_dir=processed_dir,
                                    config_data=config_data
                                )
                            except Exception as ex:
                                print(f"Error processing {full_path}: {ex}")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[Interrupted] ユーザ操作で監視を終了します。")
