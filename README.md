# PDF2TEXT

docker build -t pdf2text -f build/Dockerfile .
docker run pdf2text

# OCR

# PDF

## ファイルのメタデータに情報を埋め込む
## ファイルをテキストとして出力する

# 配置個所の決定

# GPT



## 完了後のファイルを移動する、上書きする


# 監視

## 新しく追加されたファイルがあるかを確認する


# DEVCONTAINER
```
{
	"name": "pdf2text",
	"image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
	"postCreateCommand": "pip install --upgrade pip && pip install --user -r requirements.txt",
	"mounts": [
		{
			"source": "path the dir to read",
			"target": "/workspaces/pdf2text/mnt/pdf",
			"type": "bind"
		},
		{
			"source": "path the dir to out",
			"target": "/workspaces/pdf2text/mnt/text",
			"type": "bind"
		},
		{
			"source": "path the dir to models",
			"target": "/workspaces/pdf2text/mnt/models",
			"type": "bind"
		}
	]
}
```