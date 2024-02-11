# from Compiler.Lexer import Lexer
# from Compiler.Parser import tokensToNodes, executor, node
# file = open(r'hello.lisp', 'r+')
# lexer = Lexer(file)
# lexer.get_hasher()
# lexer.get_tokens()
# # lexer.print_Tokens()
# nodeList = tokensToNodes(lexer.tokens)
# exec = executor(nodeList)
# root = exec.build()
# root.print()
# import struct 
# with open('test.bin', mode  = 'wb') as f:
#     # f.write(struct.pack('i', 7))
#     f.write(struct.pack('i', ((31 << 24) | (4 << 24) )))
# f.close()
# with open('test.bin', mode  = 'wb') as f:
#     f.write(struct.pack('i', 7))
# f.close()

# with open('test.bin', mode  = 'rb') as f:
#     bin = f.read()
#     t = struct.unpack('i'*2,bin)[1]
# f.close()
# print(hex(t))
print(hex(1 << 2 | 3))