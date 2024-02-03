from typing import Any
from abc import ABC, abstractmethod

from Compiler.Semantic import LOGICAL_OPERATOR, MATH_OPERATOR, KEYWORD, is_String, is_Integer, is_Boolean

class node(ABC):
    def __init__(self, tokens, name = None):
        self.tokens = tokens
        self.children = []
        self.name = name
    @abstractmethod
    def build(self):
        pass

class expression(node):
    def build(self):
        pass

class literal(node):
    @abstractmethod
    def isInstance(self):
        pass

class string(literal):
    def isInstance(self):
        pass

class integer(literal):
    def isInstance(self):
        return super().isInstance()
    
class boolean(literal):
    def isInstance(self):
        return super().isInstance()
class identifier(node):
    def build(self):
        pass

class mathematic_operant(node):
    def build(self):
        pass

class logical_operant(node):
    def build(self):
        pass

class if_clause(node):
    def build(self):
        pass

class set(node):
    def build(self):
        pass

class print(node):
    def build(self):
        pass

class defun(node):
    def build(self):
        pass

class call(node):
    def build(self):
        pass

class for_clause(node):
    def build(self):
        pass

class loop(node):
    def build(self):
        pass

# literal have 1 child node
# identifier is node itself
# math operator have children in bracket itself , for example: + 1 2 3 4, / 1 2
# logical operator have 2 child node
# if have 2 or 3 node
# set have 2 node
# print have 1 node( without 't')
# defun have 3 node
# call have n node
# loop have 2 node : 1 for and 1 expression
# for have 3 node: i , from, to
# 1 node represent for 1 token or 1 chain of tokens(1 parentheses)

# thuat toan nhu the nao?
# dau tien, chia nho cac phan thanh node, co the la single node hoac expression
# xet node dau tien, lay a node tiep theo lam child cua node do, tiep tuc nhay den node thu a + 1,
# tiep tuc cho den khi ket thuc chuoi, hoac neu thua 1 cai gi do( dau dong ngoac/ mo ngoac thi bao loi)

# can trien khai nhu the nao?
    
class left(node):
    def build(self):
        pass

class right(node):
    def build(self):
        pass


def exp2exps(exp : expression):
    counter = 0
    stack = []
    tokens = exp.tokens
    values = list(tokens.values())
    for i in range(len(tokens)):
        if(values[i] == '('):
            counter = counter + 1
        elif(values[i] == ')'):
            counter = counter - 1
            if(counter  == 0):
                exp.children.append(expression(stack))
                stack.clear()
        else:
            if(counter == 0):
                