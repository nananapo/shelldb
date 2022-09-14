from parser import NodeType
from util import isint

# TODO 型チェック
# TODO パイプで正当な値の受け渡しをしているかのチェック
# TODO ↑これに関して、先にスキーマを取得しておきたい
# TODO 使っていないコマンドライン引数があるときどうする？
#      例えばパイプ時のls table

def ana(node, piped):

	if node.type == NodeType.ERROR:
		return (False, node)

	if node.type == NodeType.PIPE:
		(success1, node.lhs) = ana(node.lhs, piped)
		(success2, node.rhs) = ana(node.rhs, True)
		return (success1 and success2, node)

	if node.type == NodeType.REDIRECT_WRITE:
		if node.argc != 1:
			print("Usage : >> [tablename]")
			return (False, node)
		return (True, node)

	if node.type == NodeType.LS:
		if piped:
			print("error : ls doesn't use input")
			return (False, node)
		if node.argc != 1:	
			print("Usage : ls [tablename]")
			return (False, node)
		return (True, node)

	if node.type == NodeType.COUNT:
		if piped:
			return (True, node)
		if node.argc != 1:	
			print("Usage : count [tablename]")
			return (False, node)
		return (True, node)

	if node.type == NodeType.WHERE:
		if not piped:
			print("error : where requires input")
			return (False, node)

		# 引数がないか、奇数個である
		if node.argc == 0 or node.argc % 2 == 1:
			print("error : where arg")
			return (False, node)
		return (True, node)

	if node.type == NodeType.LIMIT:
		if not piped:
			print("error : limit requires input")
			return (False, node)

		if node.argc != 1:
			print("Usage : limit [count]")
			return (False, node)

		# 引数が数字ではない
		s = node.args[0].str
		if not isint(s):
			print("error : failed to parse int :", s)
			return (False, node)

		# TODO nodeを置き換えてしまいたい
		# count = int(s)
		return (True, node)

	if node.type == NodeType.SCHEMA:
		# TODO pipeするのもされるのも許さない
		if piped:
			return 
		if node.argc != 1:
			print("Usage : schema [tablename]")
			return (False, node)
		return (True, node)

	print("gen: unknown node", node)
	return (False, node)

def analyze(node):
	return ana(node, False)
