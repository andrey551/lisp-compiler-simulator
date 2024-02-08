from Compiler.Parser import (
    executor, integer, 
    string, boolean, 
    node, literal, 
    identifier)
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
            





    
                
            