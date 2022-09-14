import copy
from tokenizer import TokenType
from enum import Enum

class NodeType(Enum):
	PIPE			= 20
	REDIRECT_WRITE	= 21

	LS		= 100
	WHERE	= 101
	COUNT	= 102
	LIMIT	= 103

class Node:
	def __init__(self, ty):
		self.type = ty
		self.rhs = None
		self.lhs = None
		self.__args = []
		self.argc = 0

	def add_arg(self, tok):
		self.__args.append(tok)
		self.argc += 1

	@property
	def args(self):
		return copy.copy(self.__args)

	def __str__(self):
		if self.type == NodeType.PIPE:
			return "Node<"+str(self.type)+">("+str(self.lhs)+","+str(self.rhs)+")"
		return "Node<"+str(self.type)+">"

	def __repr__(self):
	    return self.__str__()

commands = {
	"ls": NodeType.LS,
	"where": NodeType.WHERE,
	"count": NodeType.COUNT,
	"limit": NodeType.LIMIT,
}

def read_command_args(tokens, index, node):
	while index < len(tokens):
		if tokens[index].type == TokenType.SYMBOL:
			node.add_arg(tokens[index])
		else:
			break
		index += 1
	return (index)

def consume_command(ty, tokens, index):
		node = Node(ty)
		index = read_command_args(tokens, index, node)
		return (node, index)

def parse_command(tokens, index):
	tok = tokens[index]

	if tok.type != TokenType.SYMBOL:
		print("parse error : not command", tok)
		exit()

	if tok.str in commands:
		return consume_command(commands[tok.str], tokens, index + 1)
	else:
		print("parse error: unknown command", tok.str)
		exit()

def parse_pipe(tokens, index):
	(ast, index) = parse_command(tokens, index)
	tok = tokens[index]
	if tok.type == TokenType.PIPE:
		index += 1
		node = Node(NodeType.PIPE)
		node.lhs = ast
		(node.rhs, index) = parse_syntax(tokens, index)
		return (node, index)
	return (ast, index)

def parse_syntax(tokens, index):
	(ast, index) = parse_pipe(tokens, index)
	tok = tokens[index]
	if tok.type == TokenType.REDIRECT_WRITE:
		index += 1
		node = Node(NodeType.REDIRECT_WRITE)
		node.lhs = ast
		index = read_command_args(tokens, index, node)
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
