from Compiler.Lexer import Lexer
from Compiler.Parser import tokensToNodes, executor, node
from Compiler.Generator import translate
file = open(r'inout.lisp', 'r+')
lexer = Lexer(file)
lexer.get_hasher()
lexer.get_tokens()
# lexer.print_Tokens()
nodeList = tokensToNodes(lexer.tokens)
exec = executor(nodeList)
root = exec.build()
root.print()
trans = translate(root)
