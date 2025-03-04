import json

def format_output_as_json(task_type: str, model_output: str) -> str:
    """
    生成モデルのテキスト model_output を受け取り、
    task_type( 'summary' or 'extraction' )に応じて
    決まったJSON構造を組み立てる。
    最終的にjson文字列を返す。
    """
    if task_type == "summary":
        # 要約の場合は {"summary": "..."} だけの構造にする
        result_dict = {
            "summary": model_output
        }
        return json.dumps(result_dict, ensure_ascii=False)

    elif task_type == "extraction":
        # データ抽出用のフィールドが固定されている想定
        # 例: "model_output"には複数行のテキストが来るので、正規表現やキーワード分割などで
        # 必要な情報を抽出するのが現実的。
        
        # ここではとりあえず全体を1つのフィールドに入れる例
        result_dict = {
            "company_name": "",
            "date": "",
            "other_info": ""
        }
        
        # 例として model_output に "company: FooInc, date:2025-01-01 ..." と出てきた場合に
        # それを正規表現で拾って埋め込むなどの処理を行う。
        # このサンプルでは簡易的に全体を丸ごと "other_info" に入れるだけにする。
        result_dict["other_info"] = model_output
        
        # 実際には、変換ロジックを定義して各フィールドに必要な情報を割り振る。
        # result_dict["company_name"] = extracted_company
        # result_dict["date"]         = extracted_date
        # ...

        return json.dumps(result_dict, ensure_ascii=False)

    else:
        # 想定外のtask_typeはエラーを返す
        raise ValueError(f"Unknown task_type: {task_type}")
