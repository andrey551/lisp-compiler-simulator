from Compiler.Lexer import Lexer
from Compiler.Parser import tokensToNodes, executor
from Compiler.Generator import translate
from Machine.Control_Unit import CU
SRC = 'prob2.lisp'
MCF = 'test.bin'
INPUT_FILE = 'in.txt'
OUTPUT_FILE = 'out.txt'
file = open(SRC, 'r+')
lexer = Lexer(file)
lexer.get_hasher()
lexer.get_tokens()
nodeList = tokensToNodes(lexer.tokens)
exec = executor(nodeList)
root = exec.build()

controlUnit = CU()
controlUnit.setup(INPUT_FILE, OUTPUT_FILE, MCF)
trans = translate(root, controlUnit.datapath.buffer)
controlUnit.run()

