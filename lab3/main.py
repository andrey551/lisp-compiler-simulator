from Compiler.Lexer import Lexer
from Compiler.Parser import tokensToNodes, executor, node
from Compiler.Generator import translate
file = open(r'prob5.lisp', 'r+')
lexer = Lexer(file)
lexer.get_hasher()
lexer.get_tokens()
nodeList = tokensToNodes(lexer.tokens)
exec = executor(nodeList)
root = exec.build()
root.print()
trans = translate(root)

