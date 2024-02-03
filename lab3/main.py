# from Compiler.Lexer import Lexer
# from Compiler.Parser import node
# file = open(r'hello.lisp', 'r+')
# lexer = Lexer(file)
# lexer.get_hasher()
# lexer.get_tokens()
# i = node(lexer.tokens)
# i.build()
# print('list: ')
# i.print()
# lexer.print_Tokens()

arr1 = [1, 2, '(' ,1, 0, 2, 1, 0, 1, 1, 0, ')', 1, 0]
class node():
    def __init__(self, 
                 value, 
                 level = 0,
                 children = [],):
        self.value = value
        self.children = children
        self.level = level
    def print(self):
        print("level: ", self.level, ", value: ", self.value)

arr = []
for i in range(len(arr1)):
    arr.append(node(arr1[i]))

def execute(arr, index : int = 0):
    if(arr[index].value == '('):
        arr[index] = node(-1, arr[index].level + 1)
        while(arr[index + 1].value != ')'):
            execute(arr, index + 1)
            arr[index].children.append(arr[index + 1])
            arr.pop(index + 1)
    elif(arr[index].value == ')'):
        arr.pop(index)
    else:
        for i in range(arr[index].value):
            execute(arr, index + 1)
            arr[index].children.append(arr[index + 1])
            arr.pop(index + 1)
execute(arr, 0)
arr[0].print()