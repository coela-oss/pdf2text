# DebianベースのPython公式イメージ
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存パッケージを先にコピーしてキャッシュを有効にする
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY src /app/src

# 設定ファイルをビルド時にコンテナ内に配置
COPY config.ini /app/config.ini

# エントリポイントスクリプトを追加
#COPY build/entrypoint.sh /app/entrypoint.sh
#RUN chmod +x /app/entrypoint.sh

# エントリポイントを設定
ENTRYPOINT ["/app/src/cli.py"]

CMD [ "--help" ]
