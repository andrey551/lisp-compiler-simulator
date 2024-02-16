from typing import Any
from abc import ABC, abstractmethod

from Compiler.Semantic import LOGICAL_OPERATOR, MATH_OPERATOR, KEYWORD, is_String, is_Integer, is_Boolean

class node(ABC):
    def __init__(self, tokens, name = None, value = None):
        self.tokens = tokens
        self.children = []
        self.name = name
        self.value = value
    def print(self, level = 0):
        print(level * "    ", self.name, " : ", self.value)
        for i in self.children:
            i.print(level + 1)
    def set_address(self, addr: int):
        self.address = addr
    @abstractmethod
    def build(self):
        pass

class expression(node):
    def build(self):
        pass

class literal(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 0
    @abstractmethod
    def isInstance(self):
        pass

    def build(self):
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
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 0
    def build(self):
        pass

class mathematic_operant(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass

class logical_operant(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass

class if_clause(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
    def build(self):
        pass

class set(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass

class let(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass

class printf(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass

class defun(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 3
    def build(self):
        pass

class call(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass

class input(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass

class for_clause(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 3
    def build(self):
        pass

class loop(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass
# expression can have multiple children
# literal have 0 child node
# identifier is node itself
# math operator have 1 child node , which is expression , for example: + (1 2 3 4), / (1 2)
# logical operator have 2 child node
# if have 2 or 3 node
# set have 2 node
# print have 2 node( t or whatever )
# defun have 3 node
# call have 2 node
# loop have 2 node : 1 for and 1 expression
# for have 3 node: i , from, to
# from have 1 node
# to have 1 node
# 1 node represent for 1 token or 1 chain of tokens(1 expression)
    
class left(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 0
    def build(self):
        pass

class right(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 0
    def build(self):
        pass

class fr(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass

class to(node):
    def __init__(self, 
               tokens, 
               name = None, 
               value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass
class while_(node):
    def __init__(self, 
                 tokens,
                 name = None,
                 value = None):
        node.__init__(self, tokens, name, value)
        self.params = 2
    def build(self):
        pass
class return_(node):
    def __init__(self, 
                 tokens,
                 name = None,
                 value = None):
        node.__init__(self, tokens, name, value)
        self.params = 1
    def build(self):
        pass

def tokensToNodes(tokens):
    ret = []
    keys = [key for dictionary in tokens for key in dictionary.keys()]
    values = [value for dictionary in tokens for value in dictionary.values()]
    for i in range(len(tokens)):
        if(keys[i] == 'LEFT_PARENTHESIS'):
            ret.append(left(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'RIGHT_PARENTHESIS'):
            ret.append(right(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'INTEGER'):
            ret.append(integer(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'BOOLEAN'):
            ret.append(boolean(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'STRING'):
            ret.append(string(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'IDENTIFIER'):
            ret.append(identifier(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'MATHEMATIC_OPERATION'):
            ret.append(mathematic_operant(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'LOGICAL_OPERATION'):
            ret.append(logical_operant(tokens[i], keys[i], values[i]))
        elif(keys[i] == 'KEYWORD'):
            if(values[i] == 'if'):
                ret.append(if_clause(tokens[i], keys[i], values[i]))
            elif(values[i] == 'let'):
                ret.append(let(tokens[i], keys[i], values[i]))
            elif(values[i] == 'set'):
                ret.append(set(tokens[i], keys[i], values[i]))
            elif(values[i] == 'format'):
                ret.append(printf(tokens[i], keys[i], values[i]))
            elif(values[i] == 'defun'):
                ret.append(defun(tokens[i], keys[i], values[i]))
            elif(values[i] == 'for'):
                ret.append(for_clause(tokens[i], keys[i], values[i]))
            elif(values[i] == 'loop'):
                ret.append(loop(tokens[i], keys[i], values[i]))
            elif(values[i] == 'from'):
                ret.append(fr(tokens[i], keys[i], values[i]))
            elif(values[i] == 'to'):
                ret.append(to(tokens[i], keys[i], values[i]))
            elif(values[i] == 'input'):
                ret.append(input(tokens[i], keys[i], values[i]))
            elif(values[i] == 'while'):
                ret.append(while_(tokens[i], keys[i], values[i]))
            elif(values[i] == 'return'):
                ret.append(return_(tokens[i], keys[i], values[i]))
            elif(values[i] == 'call'):
                ret.append(call(tokens[i], keys[i], values[i]))
            else:
                pass
        else:
            pass
    return ret

class executor():
    def __init__(self, 
                 node_chain = None):
        self.chain = node_chain
    def execute(self, iterator = 0):
        if(self.chain[iterator].value == '('):
            self.chain[iterator] = expression(self.chain[iterator], 'expression')
            while(self.chain[iterator + 1].value != ')'):
                self.execute(iterator + 1)
                self.chain[iterator].children.append(self.chain[iterator + 1])
                self.chain.pop(iterator + 1)
            self.chain.pop(iterator + 1)
        elif(self.chain[iterator].value == ')'):
            pass
        elif(self.chain[iterator].value == 'if'):
            counter = 0
            while(self.chain[iterator + 1].value != ')'):
                self.execute(iterator + 1)
                self.chain[iterator].children.append(self.chain[iterator + 1])
                self.chain.pop(iterator + 1)
                counter = counter + 1
                if(counter > 3):
                    raise BufferError('Number of parameter is not higher than 3 in if clause!')
        elif(self.chain[iterator].params >= 0):
            self.chain[iterator].children = []
            for i in range(self.chain[iterator].params):
                self.execute(iterator + 1)
                self.chain[iterator].children.append(self.chain[iterator + 1])
                self.chain.pop(iterator + 1)
        else:
            raise SyntaxError('Syntax is incorrect at ', iterator)
    def build(self):
        self.execute()
        return self.chain[0]

