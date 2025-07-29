# 自作ツールの読み込みサポート [private_tools]

import sys
import fies
from relpath import rel2abs

# 設定ファイルのパス
PATH_LIST_FILENAME = rel2abs("path_list.yml")

# sys.pathへの追加
def add_sys_path(new_path):
	if new_path in sys.path: return None
	sys.path.append(new_path)

# 旧データの削除
def del_sys_path(del_path):
	if del_path not in sys.path: return None
	sys.path = [e for e in sys.path if e != del_path]

# パス一覧オブジェクト (list-like-object)
class Path_List:
	# 初期化処理
	def __init__(self):
		# 設定ファイルが存在しない場合に作成する
		if PATH_LIST_FILENAME not in fies:
			fies[PATH_LIST_FILENAME, "yaml"] = []
		# 設定ファイルの読み込み
		self.data = fies[PATH_LIST_FILENAME, "yaml"]
		# 最初の内容を全てsys.pathに追加する
		for e in self.data: add_sys_path(e)	# sys.pathへの追加
	# listに対する操作をすべて受け付け (受け付け)
	def __getattr__(self, funcname): return self.list_redirect(funcname)
	# listに対する操作をすべて受け付け (実処理)
	def list_redirect(self, funcname):
		def ret_func(*args, **kwargs):
			args = [(e.data if type(e) == type(self) else e) for e in args]	# 引数に渡されるPath_List型のオブジェクトをlist型にする
			copied_ls = list(self.data)	# 汚染防止
			org_func = getattr(copied_ls, funcname)	# 元の操作
			res = org_func(*args, **kwargs)	# 元の操作を実行
			# 変更後のリストを反映
			self.replace_all(copied_ls)	# 中身を全て置き換え
			return res
		return ret_func
	# 特殊関数の実装
	def __getitem__(self, *args, **kwargs): return self.list_redirect("__getitem__")(*args, **kwargs)
	def __setitem__(self, *args, **kwargs): return self.list_redirect("__setitem__")(*args, **kwargs)
	def __delitem__(self, *args, **kwargs): return self.list_redirect("__delitem__")(*args, **kwargs)
	def __len__(self, *args, **kwargs): return self.list_redirect("__len__")(*args, **kwargs)
	def __iter__(self, *args, **kwargs): return self.list_redirect("__iter__")(*args, **kwargs)
	def __contains__(self, *args, **kwargs): return self.list_redirect("__contains__")(*args, **kwargs)
	def __add__(self, *args, **kwargs): return self.list_redirect("__add__")(*args, **kwargs)
	def __mul__(self, *args, **kwargs): return self.list_redirect("__mul__")(*args, **kwargs)
	def __eq__(self, *args, **kwargs): return self.list_redirect("__eq__")(*args, **kwargs)
	def __lt__(self, *args, **kwargs): return self.list_redirect("__lt__")(*args, **kwargs)
	def __gt__(self, *args, **kwargs): return self.list_redirect("__gt__")(*args, **kwargs)
	def __le__(self, *args, **kwargs): return self.list_redirect("__le__")(*args, **kwargs)
	def __ge__(self, *args, **kwargs): return self.list_redirect("__ge__")(*args, **kwargs)
	# 1つパスを追加 (appendの別表現)
	def push(self, new_path): self.append(new_path)
	# 文字列化
	def __str__(self): return f"<private-tools-path-list {self.data}>"
	def __repr__(self): return str(self)
	# 中身を全て置き換え
	def replace_all(self, new_list):
		# new_list がPath_List型のとき
		if type(new_list) == type(self):
			new_list = new_list.data
		# 型の確認
		err = Exception('[private-tools error] `path` only accepts values of type "list of strings."')
		if type(new_list) != type([]): raise err
		for e in new_list:
			if type(e) != type(""): raise err
		# 重複の削除
		new_list = list({k: True for k in new_list})
		# sys.pathへの反映
		for e in self.data: del_sys_path(e)	# 旧データの削除
		for e in new_list: add_sys_path(e)	# sys.pathへの追加
		# 反映
		self.data = new_list
		fies[PATH_LIST_FILENAME, "yaml"] = self.data

# パス一覧オブジェクトを実体化
path_list = Path_List()

# ptオブジェクト (private_toolsモジュールそのものを表すオブジェクト)
class PT:
	# 初期化処理
	def __init__(self):
		self._path = path_list
	# pt.path を定義
	def __getattr__(self, key):
		return (self._path if key == "path" else super().__getattr__(key))
	# 「pt.path = ...」を特別に定義
	def __setattr__(self, key, new_list):
		if key == "path":
			self._path.replace_all(new_list)	# 中身を全て置き換え
		else:
			super().__setattr__(key, new_list)	# デフォルトの代入動作を行う

# ptオブジェクトを実体化
pt = PT()

# モジュールと「ptオブジェクト」を同一視
sys.modules[__name__] = pt
