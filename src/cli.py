import click
import configparser

from direct_watcher import direct_watch
from pdf_processor import process_single_pdf

@click.group()
@click.option("--config", help="INI形式の設定ファイルパス")
@click.pass_context
def cli(ctx, config):
    """
    PDF監視スクリプト (Click版)
    - page_option を設定ファイルで指定すると、テキスト抽出範囲を制御できます
      0  => 抽出しない
      1  => 1ページ目のみ(デフォルト)
      -1 => 全ページ
      n>1 => nページ目のみ
    """
    ctx.ensure_object(dict)
    if config:
        parser = configparser.ConfigParser()
        parser.read(config)
        if "default" in parser:
            ctx.obj["config_data"] = dict(parser["default"])
        else:
            ctx.obj["config_data"] = {}
    else:
        ctx.obj["config_data"] = {}

@cli.command(help="フォアグラウンドで監視")
@click.pass_context
def direct(ctx):
    cfg = ctx.obj["config_data"]
    directory = cfg.get("directory", "./")
    processed_dir = cfg.get("processed_dir", "./processed")
    interval = int(cfg.get("interval", 10))

    direct_watch(directory, processed_dir, interval, config_data=cfg)


@cli.group(help="疑似サービス操作")
@click.pass_context
def service(ctx):
    pass

@cli.command(help="単一PDFを処理")
@click.option("--file", required=True, help="対象PDFファイル")
@click.pass_context
def process(ctx, file):
    cfg = ctx.obj["config_data"]
    processed_dir = cfg.get("processed_dir", "./processed")

    # ここで page_option は config_data に書いてあるものを使う
    process_single_pdf(pdf_path=file, processed_dir=processed_dir, config_data=cfg)


if __name__ == "__main__":
    cli()
