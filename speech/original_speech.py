#!/usr/bin/env python3

# ライブラリのインポート
from pydub import AudioSegment
import subprocess
import os
import csv


# 発話させたい文章
input_text = "こんにちは"

# 発話させたい文章を表示
print("------------------------------------")
print("○  発話させたい文章: {}".format(input_text))
print("------------------------------------")


# wavesフォルダの中身を読み込む
voices = {}
for filename in os.listdir("./waves"):
    name, ext = os.path.splitext(filename)
    voices[name] = AudioSegment.from_file("./waves/{}".format(filename), "wav")

# 母音の対応表を読み込む
vowel = {}
with open("./vowel.csv", "r") as f:
    for row in csv.reader(f):
        sp_row = row[0].split(" ")
        vowel[sp_row[0]] = sp_row[1]

# 文字をわける
words = []
print(input_text)
for word in list(input_text):
    if word == "ゃ" or word == "ゅ" or word == "ょ":
        words[-1] += word
    elif word == "ー" or word == "～":
        words.append(vowel[words[-1]])
    else:
        words.append(word)

# 先頭に無音の音声を追加
sound = AudioSegment.from_file("./waves/無音.wav", "wav")

# わけた文字を使って音声合成
for word in words:
    if word in voices:
        sound += voices[word]
    else:
        print("「{}」の音声データがありませんでした。".format(word))

# 末尾に無音の音声を追加
sound += AudioSegment.from_file("./waves/無音.wav", "wav")

# 合成した音声をWAVで保存
sound.export("speech.wav", format="wav")

# 保存したWAVデータを再生
subprocess.check_call('aplay -D plughw:Headphones {}'.format("speech.wav"), shell=True)
