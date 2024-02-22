from Compiler.Lexer import Lexer
from Compiler.Parser import tokensToNodes, executor
from Compiler.Generator import translate
from Machine.Control_Unit import CU
import logging
# SRC = 'prob2.lisp'
# MCF = 'test.bin'
# INPUT_FILE = 'in.txt'
# OUTPUT_FILE = 'out.txt'
# file = open(SRC, 'r+')
# lexer = Lexer(file)
# lexer.get_hasher()
# lexer.get_tokens()
# nodeList = tokensToNodes(lexer.tokens)
# exec = executor(nodeList)
# root = exec.build()

# controlUnit = CU()
# controlUnit.setup(INPUT_FILE, OUTPUT_FILE, MCF)
# trans = translate(root, controlUnit.datapath.buffer)
# controlUnit.run()

dirs = ['tests/testcase-4/']
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
def run(src, machine_code, infile, outfile, stacktrace):
    
    file = open(src, 'r+')
    lexer = Lexer(file)
    lexer.get_hasher()
    lexer.get_tokens()
    nodeList = tokensToNodes(lexer.tokens)
    exec = executor(nodeList)
    root = exec.build()

    controlUnit = CU()
    controlUnit.setup(infile, outfile, machine_code)
    translate(root, controlUnit.datapath.buffer, machine_code, stacktrace)
    controlUnit.run()
for i in dirs:
    run(i + 'code.lisp', i + 'code.bin', i + 'in.txt', i + 'out.txt', i +  'debug.txt')