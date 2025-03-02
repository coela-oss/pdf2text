#!/bin/sh

CONFIG_FILE="/app/config.ini"

# `config.ini` が存在しない場合はエラー
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found at $CONFIG_FILE"
    exit 1
fi

# `config.ini` から値を読み込んで環境変数として設定
INPUT_DIR=$(grep "^directory=" "$CONFIG_FILE" | cut -d '=' -f2 | tr -d '[:space:]')
OUTPUT_DIR=$(grep "^processed_dir=" "$CONFIG_FILE" | cut -d '=' -f2 | tr -d '[:space:]')

# 設定値の確認（デバッグ用）
echo "Input Directory: $INPUT_DIR"
echo "Output Directory: $OUTPUT_DIR"

# 環境変数を設定
export INPUT_DIR OUTPUT_DIR

# Pythonスクリプトを実行（環境変数が渡される）
exec python /app/src/cli.py "$@"
