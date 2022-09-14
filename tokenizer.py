from enum import Enum

class TokenType(Enum):
	EOF				= 0

	SYMBOL			= 10
	#STR			= 11

	PIPE			= 20
	REDIRECT_WRITE	= 21
	#REDIRECT_APPEND= 22

class Token:
	def __init__(self, ty, strindex):
		self.type = ty
		self.strindex = strindex
		self.str = ""

	def __str__(self):
		if self.type == TokenType.SYMBOL:
			return "Token<"+str(self.str)+">"
		return "Token<"+str(self.type)+", "+str(self.strindex)+">"

	def __repr__(self):
	    return self.__str__()

ops = {
	"|": TokenType.PIPE,
	">": TokenType.REDIRECT_WRITE,
}

def matchword(S, index, word):
	if len(S) - index < len(word):
		return False
	for i in range(len(word)):
		if S[index + i] != word[i]:
			return False
	return True

def tokenize(S):
	tokens = []
	i = 0
	while i < len(S):
		s = S[i]
		
		#skip space
		if s == " " or s == "\n":
			i += 1
			continue

		# op
		is_word = False
		for (word, ty) in ops.items():
			if matchword(S, i, word):
				tokens.append(Token(ty, i))
				i += len(word)
				is_word = True
				break
		if is_word:
			continue

		# string
		if s == "\"":
			print("not impl")
			exit()

		# symbol
		if "A" <= s <= "z" or s == "_" or "0" <= s <= "9":
			tok = Token(TokenType.SYMBOL, i)
			while i < len(S):
				s = S[i]
				if not ("A" <= s <= "z" or s == "_" or "0" <= s <= "9"):
					break
				tok.str += s
				i += 1
			tokens.append(tok)
			continue

		print("tokenize error : " , s)
		print("number : ", i)
		exit()

	# eof
	tokens.append(Token(TokenType.EOF, i))

	return tokens
