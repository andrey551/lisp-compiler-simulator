from Compiler.Parser import (
    executor, integer, 
    string, boolean, 
    node, literal, 
    identifier,
    expression)
from Compiler.Semantic import (
    code_generate,
    Opcode,
    Mode
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
# sbp: 0x5 : begin of stack( end of memory) 
# rsi: 0x6
# rdi: 0x7
# r8 -> r15
class visitor():
    def __init__(self) :
        self.identifier = []
        self.main = []
        self.stack_counter = 65535 
        self.generator = code_generate()
    def get_lastest_identifier(self, name :str):
        for i in reversed(self.identifier):
            if(i.name == name):
                return i
        return None
    def setLiteralAddress(self, root: node):
        for i in root.children:
            self.setLiteralAddress(i)
            if(isinstance(literal, root)):
                root.address = len(self.main)
            if(isinstance(int, root)):
                self.main.append(self.generator.generate_int(root.value))
            elif(isinstance(boolean, root)):
                self.main.append(self.generator.generate_bool(root.value))
            elif(isinstance(string, root)):
                self.main.append(self.generator.generate_string(root.value))
            else:
                pass

            
    def visitLetNode(self, nd : node):
        self.state.isInLet = True
        if(len(nd.children) != 2):
            raise ValueError('Expected number of parameters : 2')
        elif(isinstance(identifier, nd.children[0]) == False):
            raise TypeError('Expected Identifier!')
        else :
            if(isinstance(literal, nd.children[1])):
                self.identifier.append(identifier_raw(nd.children[0].value,
                                                      nd.children[1].address))
            elif(isinstance(expression, nd.children[1])):
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator.generate_one_address(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.identifier.append(identifier_raw(nd.children[0].value, 
                                                      self.stack_counter))
                self.stack_counter = self.stack_counter - 1
            
    def visitSetNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('Expected 2 params on set command!')
        elif(isinstance(nd.children[0]) == False):
            raise TypeError('first parameter on set - variable')
        else:
            self.main.append(self.generator.generate_one_address(Opcode.PUSH, Mode.DIRECT_REG, 0x0))
            self.main.append(self.generator.generate_one_address(Opcode.PUSH, Mode.DIRECT_REG, 0x2))
            iden = self.get_lastest_identifier(nd.children[0].value)
            if(iden == None):
                raise KeyError(nd.children[0].value, " is not declared yet!")
            else :
                if(isinstance(literal, nd.children[1])):
                    iden.value = nd.children[1].address
                elif(isinstance(expression, nd.children[1])):
                    self.visitExpressionNode(nd.children[1])
                    self.main.append(self.generator.generate_one_address(Opcode.PUSH,
                                                                         Mode.DIRECT_REG, 
                                                                         0x2))
                    self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                         Mode.DIRECT_REG, 
                                                                         Mode.ADDRESS, 
                                                                         0x2, iden.value))
                    self.main.append(self.generator.generate_two_address(Opcode.MOV, 
                                                                         Mode.INDIRECT_REG, 
                                                                         Mode.DIRECT_REG, 
                                                                         0x2, 0x0))
                    self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                         Mode.DIRECT_REG, 0x2))
                else :
                    raise TypeError('Unexpected parameter type on set command')
            self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                 Mode.DIRECT_REG, 0x2))
            self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                 Mode.DIRECT_REG, 0x0))
    def visitMathNode(self, nd: node):
        if(len(nd.children) != 2):
            raise AttributeError('Expected 2 params on set command!')
        else:
            self.main.append(self.generator.generate_one_address(Opcode.PUSH, 
                                                                 Mode.DIRECT_REG, 0x2))
            
            if(isinstance(expression(nd.children[0]))):
                self.visitExpressionNode(nd.children[0])
            elif(isinstance(identifier, nd.children[0])):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, iden.value))
            elif(isinstance(literal, nd.children[0])):
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')
            
            if(isinstance(expression(nd.children[1]))):
                self.main.append(self.generator.generate_one_address(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator.generate_two_address(Opcode.MOV, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0, 0x2))
                self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
            elif(isinstance(identifier, nd.children[0])):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x2, iden.value))
            elif(isinstance(literal, nd.children[0])):
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 0x2, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')

            if(nd.value == '+'):
                self.main.append(self.generator.generate_three_address(Opcode.ADD, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x0, 0x2))
            elif(nd.value == '-'):
                self.main.append(self.generator.generate_three_address(Opcode.SUB, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x0, 0x2))
            elif(nd.value == '*'):
                self.main.append(self.generator.generate_three_address(Opcode.MUL, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x0, 0x2))
            elif(nd.value == '/'):
                self.main.append(self.generator.generate_three_address(Opcode.DIV,
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.DIRECT_REG, 
                                                                        0x0, 0x0, 0x2))
            elif(nd.value == 'mod'):
                self.main.append(self.generator.generate_three_address(Opcode.MOD, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x0, 0x2))
            else:
                raise TypeError('Missing mathematic operation!')
            self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                 Mode.DIRECT_REG, 0x2))
            
        
    def visitLogicalNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('Expected 2 params on set command!')
        else:
            self.main.append(self.generator.generate_one_address(Opcode.PUSH, 
                                                                 Mode.DIRECT_REG, 0x2))
            
            if(isinstance(expression(nd.children[0]))):
                self.visitExpressionNode(nd.children[0])
            elif(isinstance(identifier, nd.children[0])):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, iden.value))
            elif(isinstance(literal, nd.children[0])):
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')
            
            if(isinstance(expression(nd.children[1]))):
                self.main.append(self.generator.generate_one_address(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator.generate_two_address(Opcode.MOV, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0, 0x2))
                self.main.append(self.generator.generate_one_address(Opcode.POP, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
            elif(isinstance(identifier, nd.children[0])):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x2, iden.value))
            elif(isinstance(literal, nd.children[0])):
                self.main.append(self.generator.generate_two_address(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 0x2, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')

            self.main.append(self.generator.generate_three_address(Opcode.CMP, 
                                                                    Mode.DIRECT_REG, 
                                                                    Mode.DIRECT_REG, 
                                                                    Mode.DIRECT_REG, 
                                                                    0x0, 0x0, 0x2))
            self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
            if(nd.value == '>'):
                self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))

                self.main.append(self.generator.generate_one_address(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                    
            elif(nd.value == '<'):
                self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x2,
                                                                    0x0))
                
                self.main.append(self.generator.generate_one_address(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
            elif(nd.value == '='):
                self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
                self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                
            elif(nd.value == '>='):
                self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
                self.main.append(self.generator.generate_one_address(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 3))
                self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                
            elif(nd.value == '<='):
                self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x2,
                                                                    0x0))
                self.main.append(self.generator.generate_one_address(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 3))
                self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
            else:
                raise TypeError('Missing mathematic operation!')
            
            self.main.append(self.generator.generate_two_address(Opcode.LOAD,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0x0,
                                                                    0x0))
            self.main.append(self.generator.generate_one_address(Opcode.JMP,
                                                                    Mode.VALUE,
                                                                    len(self.main) + 1))
            self.main.append(self.generator.generate_two_address(Opcode.LOAD,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0x0,
                                                                    0x1))
            
    def visitIfNode(self, nd: node):
        if(len(nd.children) < 2 or len(nd.children) > 3) :
            raise AttributeError('if clause exp-1 (exp-2)')
        else:
            first_inst_jmp = 0
            second_inst_jmp = 0
            second_exp_addr = 0
            after_exp = 0
            self.visitExpressionNode(nd.children[0])
            self.main.append(self.generator.generate_two_address(Opcode.CMP, 
                                                                 Mode.DIRECT_REG, 
                                                                 Mode.VALUE,
                                                                 0x0, 0x0))
            if(len(nd.children) == 2):
                first_inst_jmp = len(self.main)
                self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    after_exp))
                self.visitExpressionNode(nd.children[1])
                after_exp = len(self.main)
                self.main[first_inst_jmp] = self.generator.generate_one_address(
                                                                    Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    after_exp)
# hard to explain, but if condition is if (condition) (expression) [after if]
# then if condition is false, jump to [after if], but since we didn't visit expression yet, 
# we don't know what is exactly address that we will jump to
# so strategy is jump to a blind address , and after visit expression , we go back to correct that instruction
# same with if (condidtion) (expression) [1] (expression)[2]
#  if condition false : jump to [1], else after first expression, jump to [2])
            if(len(nd.children) == 3):
                first_inst_jmp = len(self.main)
                self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    second_exp_addr))
                self.visitExpressionNode(nd.children[1])
                second_exp_addr = len(self.main)
                self.main.append(self.generator.generate_one_address(Opcode.JMP,
                                                                     Mode.VALUE, 
                                                                     after_exp))
                self.visitExpressionNode(nd.children[2])
                after_exp = len(self.main)
                self.main[first_inst_jmp] = self.generator.generate_one_address(
                                                                    Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    second_exp_addr)
                self.main[second_inst_jmp] = self.generator.generate_one_address(
                                                                    Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    after_exp)
    def visitWhileNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('while <condition> <expression>')
        else:
            while_begin = len(self.data)
            self.visitExpressionNode(nd.children[0])
            self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                                 Mode.DIRECT_REG,
                                                                 Mode.VALUE,
                                                                 0x0,
                                                                 0x0))
            first_instr_jmp = len(self.data)
            self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                                 Mode.VALUE,
                                                                 0x0))
            self.visitExpressionNode(nd.children[1])
            self.main.append(self.generator.generate_one_address(Opcode.JMP,
                                                                 Mode.VALUE,
                                                                 while_begin))
            self.data[first_instr_jmp] = self.generator.generate_one_address(Opcode.BEQ,
                                                                 Mode.VALUE,
                                                                 len(self.data))
    
    def visitReturnNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError('return <expression>')
        else:
            if(isinstance(literal, nd.children[0])):
                self.main.append(self.generator.generate_two_address(Opcode.LOAD,
                                                                     Mode.DIRECT_REG,
                                                                     Mode.ADDRESS,
                                                                     0x0,
                                                                     nd.children[0].address))
            elif(isinstance(identifier, nd.children[0])):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator.generate_two_address(Opcode.LOAD,
                                                                     Mode.DIRECT_REG,
                                                                     Mode.ADDRESS,
                                                                     0x0,
                                                                     iden.value))
            elif(isinstance(expression, nd.children[0])):
                self.visitExpressionNode(nd.children[0])
            else:
                raise SyntaxError('Expression is not bounded!')
    def visitPrintNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError('print <identifier>/ literal / <expression>')
        else:
            if(isinstance(literal, nd.children[0])):
                pass
    def visitInputNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError("input <identifier>")
        if(isinstance(identifier, nd.children[0]) == False):
            raise TypeError('Require input identifier')
        self.identifier.append(identifier_raw(nd.children[0], self.stack_counter))

        ptt = len(self.data)
        self.main.append(self.generator.generate_one_address(Opcode.PUSH,
                                                             Mode.VALUE,
                                                             0x8080))
        self.main.append(self.generator.generate_two_address(Opcode.LOAD,
                                                             Mode.DIRECT_REG,
                                                             Mode.VALUE,
                                                             0x2,
                                                             0x0))
        self.main.append(self.generator.generate_one_address(Opcode.PUSH,
                                                                    Mode.VALUE,
                                                                    0x0))
        self.main.append(self.generator.generate_zero_address(Opcode.DI))
        self.main.append(self.generator.generate_one_address(Opcode.IN,
                                                             Mode.INDIRECT_REG,
                                                             0x4))
        
        self.main.append(self.generator.generate_two_address(Opcode.CMP,
                                                             Mode.INDIRECT_REG,
                                                             Mode.VALUE,
                                                             0x4,
                                                             0xD))
        addr = len(self.data)
        self.main.append(self.generator.generate_one_address(Opcode.BEQ,
                                                             Mode.VALUE,
                                                             0x0))
        self.main.append(self.generator.generate_one_address(Opcode.PUSH,
                                                             Mode.DIRECT_REG,
                                                             0x4))
        self.main.append(self.generator.generate_three_address(Opcode.ADD,
                                                               Mode.DIRECT_REG,
                                                               Mode.DIRECT_REG,
                                                               Mode.value,
                                                               0x2,
                                                               0x2, 
                                                               0x1))
        self.main[addr] = self.generator.generate_one_address(Opcode.BEQ,
                                                             Mode.VALUE,
                                                             len(self.data))
        self.main.append(self.generator.generate_zero_address(Opcode.EI))
        
    def visitCallNode(self, nd : node):
        pass
    def visitDefunNode(self, nd : node):
        pass
    def visitExpressionNode(self):
        pass
        
        





    
                
            