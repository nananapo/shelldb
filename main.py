from tokenizer import tokenize
from parser import parse
from analyzer import analyze
from generator import generate
from dbutil import execsql

while True:
	userinput = input("$ ")

	if userinput == "exit" or userinput == "bye":
		print("Bye")
		exit()

	tokens = tokenize(userinput)
	print("Token", tokens)

	asts = parse(tokens)
	print("AST", asts)

	for i in range(len(asts)):
		analyzed = analyze(asts[i])
		sql = generate(analyzed)
		print("#0")
		print(" ", sql)
		print("result------")
		execsql("test.db", sql)
