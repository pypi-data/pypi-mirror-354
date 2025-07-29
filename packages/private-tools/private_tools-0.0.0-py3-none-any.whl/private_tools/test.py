# 自作ツールの読み込みサポート [private_tools]
# 【動作確認 / 使用例】

import sys
import ezpip
private_tools = ezpip.load_develop("private_tools", "../", develop_flag = True)

# パスの追加
private_tools.path.append("./my_tools_test_dir")

# テスト用のダミーツール
import cat_tool

print(cat_tool("怒った"))
print(cat_tool("間違って会社のファイル全部消した"))


# パスの追加
private_tools.path.append("path/to/your/tools")
private_tools.path.push("2nd/path/to/your/tools")	# appendと動作は同様

# パス一覧の確認
print(private_tools.path)	# -> <private-tools-path-list ['path/to/your/tools', '2nd/path/to/your/tools']>

# パスの削除
private_tools.path.remove("path/to/your/tools")

private_tools.path += ["path1", "path2"]	# 一気に追加

private_tools.path = private_tools.path[:3] + private_tools.path[4:]	# リストの結合などもOK

# 下記の操作も受け付ける
del private_tools.path[1]
for e in private_tools.path: print(e)

# パスのオールクリア
private_tools.path = []
