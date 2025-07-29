# 猫っぽい語尾ツール [cat_tool]

import sys
import random

# 猫語尾一覧
TAIL_LS = [
	"にゃ",
	"にゃん",
	"にゃー",
	"に゛ゃー",
	"ごろごろ",
	"にゃー！",
	"にゃ！",
	"にゃん！",
]

# 語尾変換 [cat_tool]
def cat_tool(org_str):
	tail = random.choice(TAIL_LS)
	return org_str + tail

# モジュールと関数の同一視
sys.modules[__name__] = cat_tool
