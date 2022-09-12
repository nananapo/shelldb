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
	
	print("gen: unknown node" + node)

def generate(node):
	return gen(node, False) + ";"
