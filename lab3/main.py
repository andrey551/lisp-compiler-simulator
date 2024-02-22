from lab3.Compiler.Lexer import Lexer
from lab3.Compiler.Parser import tokensToNodes, executor
from lab3.Compiler.Generator import translate
from lab3.Machine.Control_Unit import CU
import logging
logging.basicConfig(level=logging.DEBUG)

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
