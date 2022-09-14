from parser import NodeType
from util import isint

def gen(node, piped, pipedSql = ""):

	if node.type == NodeType.PIPE:
		if piped:
			sql = gen(node.lhs, True, pipedSql)
			return gen(node.rhs, True, sql)
		sql = gen(node.lhs, False)
		return gen(node.rhs, True, sql)

	if node.type == NodeType.REDIRECT_WRITE:
		if node.argc != 1:
			print("Usage : >> [tablename]")
			exit()

		sub = gen(node.lhs, False)
		return "INSERT INTO " + node.args[0].str + " " + sub

	if node.type == NodeType.LS:
		if piped:
			print("error : ls doesn't use input")
			exit()

		if node.argc != 1:	
			print("Usage : ls [tablename]")
			exit()

		return "SELECT * FROM " + node.args[0].str

	if node.type == NodeType.COUNT:
		if piped:
			return "SELECT COUNT(*) FROM (" + pipedSql + ")"

		if node.argc != 1:	
			print("Usage : count [tablename]")
			exit()

		return "SELECT COUNT(*) FROM " + node.args[0].str

	if node.type == NodeType.WHERE:
		if not piped:
			print("error : where requires input")
			exit()

		# とりあえず=で結ぶ
		if node.argc == 0 or node.argc % 2 == 1:
			print("error : where arg")
			exit()

		conds = []
		for i in range(0, node.argc, 2):
			id = node.args[i].str
			val = node.args[i + 1].str
			conds.append(id + " = \"" + val + "\"")

		return "SELECT * FROM (" + pipedSql + ") WHERE " + " AND ".join(conds)

	if node.type == NodeType.LIMIT:
		if not piped:
			print("error : limit requires input")
			exit()

		if node.argc != 1:
			print("Usage : limit [count]")
			exit()

		s = node.args[0].str
		if not isint(s):
			print("error : failed to parse int :", s)
			exit()

		count = int(s)
		return "SELECT * FROM (" + pipedSql + ") LIMIT " + str(count)

	if node.type == NodeType.SCHEMA:
		# TODO pipeするのもされるのも許さない
		if node.argc != 1:
			print("Usage : schema [tablename]")
			exit()

		return ".schema " + node.args[0].str + "\n"

	print("gen: unknown node", node)
	exit()

def generate(node):
	return gen(node, False) + ";"
