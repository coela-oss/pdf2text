import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 小型のFLAN-T5モデルを例示
MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def summarize_text(text: str) -> str:
    """
    テキストを要約し、文字列として返す。
    """
    # T5系列は "summarize: ..." というタスク指示を入れると要約タスクを行う慣習がある
    input_ids = tokenizer(
        "summarize: " + text,
        return_tensors="pt",
        truncation=True
    ).input_ids

    # 推論
    outputs = model.generate(
        input_ids,
        max_length=100,  # 適宜調整
        num_beams=2      # ビームサーチ幅
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

def extract_data(text: str, instruction: str) -> str:
    """
    テキストから特定の情報を抽出する。
    instruction は「抜き出したい項目」の説明を任意で含めるなど。
    """
    # 例えば "extract: 会社名と日付 from text" のようなプロンプトを作る
    prompt_text = f"extract: {instruction} from {text}"
    input_ids = tokenizer(prompt_text, return_tensors="pt", truncation=True).input_ids

    outputs = model.generate(
        input_ids,
        max_length=128,
        num_beams=2
    )
    extraction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return extraction
