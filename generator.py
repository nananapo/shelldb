from parser import NodeType
from util import isint

def gen(node, piped, pipedSql = ""):

	if node.type == NodeType.PIPE:
		if piped:
			sql = gen(node.lhs, True, pipedSql)
			return gen(node.rhs, True, sql)
		sql = gen(node.lhs, False)
		return gen(node.rhs, True, sql)

	if node.type == NodeType.LS:
		if piped:
			print("error : ls doesn't use input")
			exit()
		
		if len(node.args) != 1:
			print("Usage : ls [tablename]")
			exit()

		return "SELECT * FROM " + node.args[0].str

	if node.type == NodeType.COUNT:
		if piped:
			return "SELECT COUNT(*) FROM (" + pipedSql + ")"

		if len(node.args) != 1:
			print("Usage : count [tablename]")
			exit()

		return "SELECT COUNT(*) FROM " + node.args[0].str

	if node.type == NodeType.WHERE:
		if not piped:
			print("error : where requires input")
			exit()

		# とりあえず=で結ぶ
		if len(node.args) == 0 or len(node.args) % 2 == 1:
			print("error : where arg")
			exit()

		conds = []
		for i in range(0, len(node.args), 2):
			id = node.args[i].str
			val = node.args[i + 1].str
			conds.append(id + " = \"" + val + "\"")

		return "SELECT * FROM (" + pipedSql + ") WHERE " + " AND ".join(conds)

	if node.type == NodeType.LIMIT:
		if not piped:
			print("error : limit requires input")
			exit()

		if len(node.args) != 1:
			print("Usage : limit [count]")
			exit()

		s = node.args[0].str
		if not isint(s):
			print("error : failed to parse int :", s)
			exit()

		count = int(s)
		return "SELECT * FROM (" + pipedSql + ") LIMIT " + str(count)

	print("gen: unknown node", node)
	exit()

def generate(node):
	return gen(node, False) + ";"
