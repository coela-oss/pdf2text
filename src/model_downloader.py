import os
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)

def download_model_locally(model_name: str, cache_dir: str = "./models/"):
    """
    指定された言語判定モデルをローカルにダウンロードし、
    TokenizerとModelインスタンスを返す。

    - model_name: Hugging Face で公開されているモデル名 (例: "nateraw/language-detection-distilbert")
    - cache_dir:  モデルをキャッシュするローカルパス
    """
    # from_pretrained でダウンロード＋キャッシュ
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=cache_dir)
    return tokenizer, model

def detect_dominant_language(text: str, tokenizer, model) -> str:
    """
    指定されたTokenizer・Modelを使い、入力テキストの主要言語(最もスコアが高い言語)を返す。
    """
    # パイプライン生成: "text-classification" タスク
    # return_all_scores=True で各ラベルのスコアを取得
    langid_pipeline = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        return_all_scores=True
    )
    
    # パイプラインの出力は二重リスト: [[{label:..., score:...}, ...]]
    results = langid_pipeline(text)[0]
    
    # 最もスコアの高いラベルを抜き出す
    top_label = max(results, key=lambda x: x["score"])["label"]
    return top_label


# --------------------------
# 実行テスト
# --------------------------
if __name__ == "__main__":
    # 例: DistilBERTベースの言語判定モデル
    MODEL_NAME = "NousResearch/DeepHermes-3-Llama-3-8B-Preview"

    # 1. ローカルダウンロード & モデル取得
    tokenizer, model = download_model_locally(MODEL_NAME, cache_dir="./models")

    # 2. 主要言語判定
    test_text = "This is a test message in English. これは英語と日本語が混ざった文章です。"
    main_lang = detect_dominant_language(test_text, tokenizer, model)

    print(f"入力テキストの主要言語: {main_lang}")
