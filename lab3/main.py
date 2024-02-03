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
        print(self.level * " ", "value: ", self.value)
        for i in self.children:
            i.print()
    def add_child(self, child):
        self.children.append(child)
    def get_value(self):
        return self.value

arr = []
for i in range(len(arr1)):
    arr.append(node(arr1[i]))

def get_values(arr):
    ret = []
    for i in arr:
        ret.append({i.get_value(): len(i.children)})
    return ret

def execute(arr, index : int = 0):
    if(arr[index].value == '('):
        arr[index] = node(-1, arr[index].level)
        while(arr[index + 1].value != ')'):
            arr[index + 1].level = arr[index].level + 1
            execute(arr, index + 1)
            arr[index].add_child(arr[index + 1])
            arr.pop(index + 1)
        arr.pop(index + 1)
    elif(arr[index].value == ')'):
        pass
    else:
        arr[index].children = []
        for i in range(arr[index].value):
            arr[index + 1].level = arr[index].level + 1
            execute(arr, index + 1)
            arr[index].add_child(arr[index + 1])
            arr.pop(index + 1)
    print(index, get_values(arr))
execute(arr, 0)
arr[0].print()