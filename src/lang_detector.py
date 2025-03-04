from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 利用する言語判定モデル (DistilBERT ベース)
MODEL_NAME = "nateraw/language-detection-distilbert"

# モデル・トークナイザ・パイプラインの読み込み
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
langid_pipeline = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    return_all_scores=True  # 複数の言語ラベルに対するスコアを取得
)

def detect_dominant_language(text: str) -> str:
    """
    入力テキストに対して最もスコアが高い言語(ラベル)を返す。
    例: "English", "Japanese", "French" など
    """
    # パイプラインの出力は通常 [ [ {label:..., score:...}, ... ] ] のような二重リスト構造
    # 最初の要素(リスト)のみを取り出して、各言語候補のスコアを調べる
    results = langid_pipeline(text)[0]
    
    # スコアが最大の言語を抽出
    top_label = max(results, key=lambda x: x["score"])["label"]
    return top_label


# 例: 実行テスト
test_text = "This is a test message in English. これは英語と日本語が混ざった文章です。"
main_language = detect_dominant_language(test_text)
print("主要言語:", main_language)
