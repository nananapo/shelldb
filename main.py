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

	(success, tokens) = tokenize(userinput)
	if not success:
		continue
	#print("Token", tokens)

	asts = parse(tokens)
	#print("AST", asts)

	for i in range(len(asts)):
		(success, analyzed) = analyze(asts[i])
		if not success:
			continue

		sql = generate(analyzed)
		if len(asts) != 1:
			print("#",i)
		print("<",sql)
		print(execsql("test.db", sql))
