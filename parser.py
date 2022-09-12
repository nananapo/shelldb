from tokenizer import TokenType
from enum import Enum

class NodeType(Enum):
	PIPE = 20

	LS = 100
	WHERE = 101
	WC = 102

class Node:
	def __init__(self, ty):
		self.type = ty
		self.rhs = None
		self.lhs = None
		self.args = []

	def add_arg(self, tok):
		self.args.append(tok)

	def __str__(self):
		if self.type == NodeType.PIPE:
			return "Node<"+str(self.type)+">("+str(self.lhs)+","+str(self.rhs)+")"
		return "Node<"+str(self.type)+">"

	def __repr__(self):
	    return self.__str__()

def read_command_args(tokens, index, node):
	while index < len(tokens):
		if tokens[index].type == TokenType.SYMBOL:
			node.add_arg(tokens[index])
		else:
			break
		index += 1
	return (index)

def parse_command(tokens, index):
	tok = tokens[index]

	if tok.type != TokenType.SYMBOL:
		print("parse error : not command", tok)
		exit()

	if tok.str == "ls":
		node = Node(NodeType.LS)
		index = read_command_args(tokens, index + 1, node)
		return (node, index)
	elif tok.str == "wc":
		node = Node(NodeType.WC)
		index = read_command_args(tokens, index + 1, node)
		return (node, index)
	elif tok.str == "where":
		node = Node(NodeType.WHERE)
		index = read_command_args(tokens, index + 1, node)
		return (node, index)
	else:
		print("parse error: unknown command", tok.str)
		exit()

def parse_syntax(tokens, index):
	(ast, index) = parse_command(tokens, index)
	tok = tokens[index]
	if tok.type == TokenType.PIPE:
		index += 1
		node = Node(NodeType.PIPE)
		node.lhs = ast
		(node.rhs, index) = parse_syntax(tokens, index)
		return (node, index)
	return (ast, index)

def parse(tokens):
	index = 0
	asts = []
	while index < len(tokens):
		if tokens[index].type == TokenType.EOF:
			break
		(ast, index) = parse_syntax(tokens, index)
		asts.append(ast)
	return asts
