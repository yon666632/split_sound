# -*- coding: utf-8 -*-
import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--min_silence_len", help="value for min_silence_len", type=int)
parser.add_argument("-t", "--silence_thresh", help="value for silence_thresh", type=int)
parser.add_argument("-k", "--keep_silence", help="value for keep_silence", type=int)
parser.add_argument("-s", "--start_num", help="start number of output file", type=int)
parser.add_argument("-e", "--target_ext", help="target file extention", type=str)

args = parser.parse_args()

# 初期化
min_silence_len = args.min_silence_len if args.min_silence_len else 2000
silence_thresh = args.silence_thresh if args.silence_thresh else -50
keep_silence = args.keep_silence if args.keep_silence else 500
start_num = args.start_num if args.start_num else 0
target_ext = args.target_ext if args.target_ext else "mp3"

# 同階層のinのフォルダにあるmp3ファイルをすべて検索
files = os.listdir("./in")
for file in files:
    f = os.path.splitext(file)
    if (f[1] != u".{0}".format(target_ext)):
        continue
    input_file_path = u"./in/{0}{1}".format(f[0], f[1])
    sound = AudioSegment.from_mp3(input_file_path)
    chunks = split_on_silence(
        sound,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    j = start_num
    out_dir = u"./out/{0}".format(f[0])

    # フォルダ存在チェック
    # TODO:フォルダの中に同一ファイル名があったときのハンドリング
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    for i, chunk in enumerate(chunks):
        out_file_path_name = u"{0}/{1:03d}.{2}".format(out_dir, j, target_ext)
        chunk.export(out_file_path_name, format="mp3")
        j += 1