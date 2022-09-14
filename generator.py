from parser import NodeType
from util import isint

def gen(node, piped, pipedSql = ""):

	if node.type == NodeType.PIPE:
		sql = gen(node.lhs, piped, pipedSql)
		return gen(node.rhs, True, sql)

	if node.type == NodeType.REDIRECT_WRITE:
		sub = gen(node.lhs, False)
		return "INSERT INTO " + node.args[0].str + " " + sub

	if node.type == NodeType.LS:
		return "SELECT * FROM " + node.args[0].str

	if node.type == NodeType.COUNT:
		if piped:
			return "SELECT COUNT(*) FROM (" + pipedSql + ")"
		print(node, node.args)
		return "SELECT COUNT(*) FROM " + node.args[0].str

	if node.type == NodeType.WHERE:
		# とりあえず=で結ぶ
		conds = []
		for i in range(0, node.argc, 2):
			id = node.args[i].str
			val = node.args[i + 1].str
			conds.append(id + " = \"" + val + "\"")
		return "SELECT * FROM (" + pipedSql + ") WHERE " + " AND ".join(conds)

	if node.type == NodeType.LIMIT:
		count = int(node.args[0].str)
		return "SELECT * FROM (" + pipedSql + ") LIMIT " + str(count)

	if node.type == NodeType.SCHEMA:
		return ".schema " + node.args[0].str + "\n"

	print("gen: unknown node", node)
	exit()

def generate(node):
	return gen(node, False) + ";"
