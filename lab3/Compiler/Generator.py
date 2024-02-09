from Compiler.Parser import (
    executor, integer, 
    string, boolean, 
    node, literal, 
    identifier,
    expression)
from Compiler.Semantic import (
    code_generate
)
class generator():
    def __init__(self):
        self.instruction = []
        self.data = []
        self.instr_counter = 0
    def inc_counter(self):
        self. instr_counter + 1
    def scan_data(self, tree : executor):
        for node in tree.chain:
            if(isinstance(integer, node)):
                node.set_address(len(self.data))
                if(node.value > 2^32):
                    raise ValueError(node.value,' is out of range supported!')
                else:
                    self.data.append(node.value & 0xFFFF)
                    
            elif(isinstance(boolean, node.value)):
                node.set_address(len(self.data))
                if(node.value == 'True'):
                    self.data.append(0x0001)
                else:
                    self.data.append(0x0000)
            elif(isinstance(string, node.value)):
                node.set_address(len(self.data))
                for i in range(len(node.value)):
                    word = ord(self.value[i]) * 0x100
                    if(i != len(node.value)):
                        word = word + ord(self.value[i + 1])
                    self.data.append(word)
                    i = i + 1
            else:
                pass
        self.instr_counter = len(self.data)

    def scan_instruction(self, root: node):
        if(isinstance(literal, root) == False):
            self.inc_counter()

        for i in root.children:
            self.scan_instruction(i)
        if(isinstance(literal, root)):
            pass
        elif(isinstance(identifier, root)):
            pass
        else:
            pass
class identifier_raw():
    def __init__(self, name, value): # at 0: stack , 1: data
        self.name = name
        self.value = value

# rax : 0x0
# rbx : 0x3
# rcx: 0x1
# rdx: 0x2
# rsp: 0x4
# sbp: 0x5
# rsi: 0x6
# rdi: 0x7
# r8 -> r15
class visitor():
    def __init__(self) :
        self.state = {
            isInFunction: False,
            isInIf: False,
            isInExpression:False,
            isInLet: False,
            isInSet: False
        }
        self.data = []
        self.identifier = []
        self.main = []
        self.stack_counter = 4096 
        self.generator = code_generate()
    def get_lastest_identifier(self, name :str):
        for i in reversed(self.identifier):
            if(i.name == name):
                return i
        return 
    def visitLetNode(self, nd : node):
        self.state.isInLet = True
        if(len(nd.children) != 2):
            raise ValueError('Expected number of parameters : 2')
        elif(isinstance(identifier, nd.children[0]) == False):
            raise TypeError('Expected Identifier!')
        else :
            if(isinstance(integer, nd.children[1]) == True):
                if(self.state.isInFunction == True):
                    self.identifier.append(identifier_raw(nd.children[1].value, len(self.stack)))
                    self.stack.append(self.generator.generate_int(nd.children[1].value))
                else:
                    self.identifier.append(identifier_raw(nd.children[1].value, len(self.data)))
                    self.data.append(self.generator.generate_int(nd.children[1].value))
            elif(isinstance(boolean, nd.children[1]) == True ):
                if(self.state.isInFunction == True):
                    self.identifier.append(identifier_raw(nd.children[1].value, len(self.stack)))
                    self.stack.append(self.generator.generate_bool(nd.children[1].value))
                else:
                    self.identifier.append(identifier_raw(nd.children[1].value, 1, len(self.data)))
                    self.data.append(self.generator.generate_bool(nd.children[1].value))
            elif(isinstance(string, nd.children[1])):
                if(self.state.isInFunction == True):
                    self.identifier.append(identifier_raw(nd.children[1].value, 0, len(self.stack)))
                    ret = self.generator.generate_string(nd.children[1].value)
                    for i in ret: 
                        self.stack.append(i)
                else:
                    self.identifier.append(identifier_raw(nd.children[1].value, 1, len(self.data)))
                    ret = self.generator.generate_string(nd.children[1].value)
                    for i in ret: 
                        self.data.append(i)
            elif(isinstance(expression, nd.children[1])):
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator.generate_push(0, 0x0))
                self.stack_counter = self.stack_counter - 1
                self.identifier.append(identifier_raw(nd.children[0].value))


    def visitExpressionNode(self):
        pass
        
        





    
                
            