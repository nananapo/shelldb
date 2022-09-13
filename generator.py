from parser import NodeType

TABLE = "test"

def gen(node, piped, pipedSql = ""):

	if node.type == NodeType.LS:
		if piped:
			print("error : ls doesn't use input")
			exit()
		return "SELECT * FROM " + TABLE

	if node.type == NodeType.WC:
		if piped:
			return "SELECT COUNT(*) FROM (" + pipedSql + ")"
		return "SELECT COUNT(*) FROM " + TABLE

	if node.type == NodeType.PIPE:
		if piped:
			sql = gen(node.lhs, True, pipedSql)
			return gen(node.rhs, True, sql)
		sql = gen(node.lhs, False)
		return gen(node.rhs, True, sql)

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

	print("gen: unknown node", node)
	exit()

def generate(node):
	return gen(node, False) + ";"
