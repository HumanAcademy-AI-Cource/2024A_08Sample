#!/usr/bin/env python3

# ライブラリのインポート
import boto3

# 翻訳するコマンドリストのパス
source_filename = "ja_command_list.txt"

# 翻訳後のコマンドリストの保存先パス
output_filename = "en_command_list.txt"

# AWSを使った翻訳の準備
translate = boto3.client(service_name="translate")

# コマンドリストの中身を読み込む
with open(source_filename, "r") as f:
    filedata = f.read()

# 読み込んだコマンドリストの中身を一行ごとにわける
texts = {}
for index, text in enumerate(filedata.split("\n")):
    texts[index] = text

# 一行ごとにわけたコマンドリストの中身からコメント部分だけ抜き出す
comments = {}
for key, text in texts.items():
    if text == "" or text[0] != "#":
        continue
    comments[key] = text

# 抜き出したコメント部分を翻訳
transrate_comments = {}
for key, text in comments.items():
    transrate_comments[key] = translate.translate_text(
        Text=text,
        SourceLanguageCode="ja",
        TargetLanguageCode="en"
    )["TranslatedText"]
    print("○  翻訳前: {}".format(text))
    print("○  翻訳後: {}".format(transrate_comments[key]))
    print("=================================================")

# 翻訳結果を使って、新しいコマンドリストを作成
with open(output_filename, "w") as f:
    for key, text in texts.items():
        data = ""
        if key in transrate_comments:
            data = transrate_comments[key]
        else:
            data = text
        f.write("{}\n".format(data))
