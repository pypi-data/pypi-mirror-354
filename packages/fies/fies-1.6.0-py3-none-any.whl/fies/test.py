
# ファイル入出力ツール [fies]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
fies = load_develop("fies", "../", develop_flag = True)

# json書き出し
fies["./test.json"] = {"hoge": 23, "dummy_data": "fuga"}

# json読み込み
sout(fies["./test.json"])

# プレーンテキスト書き出し
fies["./test.txt"] = "hogehoge"

# プレーンテキスト読み込み
print(fies["./test.txt"])

# pickleファイル書き出し
fies["./test.pickle"] = [("hoge", 23), 5.7]

# pickleファイル読み込み
print(fies["./test.pickle"])

# フォーマット指定書き出し
fies["./test.myext", "json"] = {"hoge": 23, "dummy_data": "fuga"}

# バイナリファイル書き出し
fies["./test.bin", "binary"] = b"hoge"

# csvファイル書き出し
fies["./test.csv", "csv"] = [
	["hoge", "fuga"],
	[23, True],
	['Hey, "Escape" man!\n']
]

# yamlファイル書き出し
fies["./test.yml", "yaml"] = {"hoge": {"fuga": 13, 77: [1,2]}}

# ディレクトリオブジェクトの扱い
d = fies["./input_dir/"]
for filename in d:
	print(filename, d[filename])

# ファイルの再帰的列挙
print(fies["./input_dir/"].all())

# fast-pickleファイル書き出し
fies["./test.fpkl"] = [("hoge", 23), 5.7]

# fast-pickleファイル読み込み
print(fies["./test.fpkl"])

# ファイルの存在確認
print("test.pickle" in fies)	# -> True
print("hoge.txt" in fies["input_dir"])	# -> True

# ファイルの削除
del fies["input_dir"]["hoge.txt"]
