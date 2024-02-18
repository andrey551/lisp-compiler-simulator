from Compiler.Parser import (
    call, defun, 
    if_clause, integer, 
    logical_operant, 
    mathematic_operant, 
    printf, return_, 
    string, boolean, 
    node, literal, input,
    identifier, let,
    set,
    expression, while_)
from Compiler.Semantic import (
    code_generate,
    Opcode,
    Mode
)

import struct

class identifier_raw():
    def __init__(self, name, type : str, value): 
        # type address : direct address, 
        # register : data saved on registers ( for function ) 
        self.name = name
        self.type = type
        self.value = value
class visitor():
    def __init__(self) :
        self.identifier = []
        self.parameters = []
        self.main = []
        self.stack_counter = 65535 
        self.generator = code_generate()
        self.heap_address = 0

    def get_lastest_identifier(self, name :str):
        for i in reversed(self.identifier):
            if(i.name == name):
                return i
        return None
    
    def setLiteralAddress(self, root: node):
        
        if(isinstance(root, literal)):
            root.address = len(self.main)
        if(isinstance(root, integer)):
            self.main.append(self.generator.generate_int(root.value))
        elif(isinstance(root, boolean)):
            self.main.append(self.generator.generate_bool(root.value))
        elif(isinstance(root, string)):
            ret = self.generator.generate_string(root.value)
            for i in ret:
                self.main.append(i)
        for i in root.children:
                self.setLiteralAddress(i)

    def setFunctionNode(self, root : node):
        for i in root.children:
                self.visitDefunNode(i)

    def visitLetNode(self, nd : node):
        if(len(nd.children) != 2):
            raise ValueError('Expected number of parameters : 2')
        elif(isinstance(nd.children[0], identifier) == False):
            raise TypeError('Expected Identifier!')
        else :
            if(isinstance(nd.children[1], literal)):
                self.identifier.append(identifier_raw(nd.children[0].value,
                                                      "address",
                                                      nd.children[1].address))
            elif(isinstance(nd.children[1], expression)):
                self.identifier.append(identifier_raw(nd.children[0].value, 
                                                      "address",
                                                      self.stack_counter))
                pointer = self.stack_counter
                self.main.append(self.generator.
                                 generate_one_address_instruction(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.stack_counter = self.stack_counter - 1
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.STORE,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0x0,
                                                                    pointer))
        
    def visitSetNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('Expected 2 params on set command!')
        elif(isinstance(nd.children[0], identifier) == False):
            raise TypeError('first parameter on set - variable')
        else:
            # self.main.append(self.generator
            #                  .generate_one_address_instruction(Opcode.PUSH, 
            #                                                      Mode.DIRECT_REG, 0x0))
            iden = self.get_lastest_identifier(nd.children[0].value)
            if(iden == None):
                raise KeyError(nd.children[0].value, " is not declared yet!")
            else :
                if(isinstance( nd.children[1], literal)):
                    if(iden.type == 'address'):
                        iden.value = nd.children[1].address
                    else:
                        self.main.append(self.generator
                                         .generate_two_address_instruction(Opcode.MOV,
                                                                            Mode.DIRECT_REG,
                                                                            Mode.ADDRESS,
                                                                            iden.value,
                                                                            nd.children[1]
                                                                            .address))
                elif(isinstance(nd.children[1], identifier)):
                    iden1 = self.get_lastest_identifier(nd.children[1].value)
                    if(iden1 != None):
                        self.main.append(self.generator.generate_one_address_instruction(Opcode.PUSH,
                                                                                         Mode.DIRECT_REG,
                                                                                         0x2))
                        self.main.append(self.generator.generate_two_address_instruction(Opcode.LOAD,
                                                                                         Mode.DIRECT_REG,
                                                                                         Mode.ADDRESS,
                                                                                         0x2,
                                                                                         iden1.value))
                        self.main.append(self.generator.generate_two_address_instruction(Opcode.STORE,
                                                                                         Mode.DIRECT_REG,
                                                                                         Mode.ADDRESS,
                                                                                         0x2,
                                                                                         iden.value))
                        self.main.append(self.generator.generate_one_address_instruction(Opcode.POP,
                                                                                         Mode.DIRECT_REG,
                                                                                         0x2))
                elif(isinstance( nd.children[1], expression)):
                    self.visitExpressionNode(nd.children[1])
                    if(iden.type == 'address'):
                        self.main.append(self.generator
                                        .generate_two_address_instruction(Opcode.STORE,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.VALUE,
                                                                        0x0,
                                                                        iden.value))
                    else:
                        self.main.append(self.generator
                                         .generate_two_address_instruction(Opcode.MOV,
                                                                            Mode.DIRECT_REG,
                                                                            Mode.DIRECT_REG,
                                                                            0x0,
                                                                            iden.value))
                else :
                    raise TypeError('Unexpected parameter type on set command')
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.POP, 
                                                                 Mode.DIRECT_REG, 0x0))
            
    def visitMathNode(self, nd: node):
        if(len(nd.children) != 1):
            raise AttributeError('Expected 1 params on set command!')
        else:
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.PUSH, 
                                                                 Mode.DIRECT_REG, 0x2))
            
            if(isinstance(nd.children[0].children[0], expression)):
                self.visitExpressionNode(nd.children[0].children[0])
            elif(isinstance(nd.children[0].children[0], identifier)):
                iden = self.get_lastest_identifier(nd.children[0].children[0].value)
                if(iden.type == 'address'):
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.LOAD, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.ADDRESS, 
                                                                        0x0, iden.value))
                else:
                    self.main.append(self.generator
                                     .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        iden.value,
                                                                        0x0))
            elif(isinstance(nd.children[0].children[0], literal)):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')
            
            if(isinstance(nd.children[0].children[1], expression)):
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.visitExpressionNode(nd.children[0].children[1])
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.MOV, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0, 0x2))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.POP, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
            elif(isinstance( nd.children[0].children[1], identifier)):
                iden = self.get_lastest_identifier(nd.children[0].children[1].value)
                if(iden.type == 'address'):
                    self.main.append(self.generator
                                     .generate_two_address_instruction(Opcode.LOAD, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.ADDRESS, 
                                                                        0x2, iden.value))
                else :
                    self.main.append(self.generator
                                     .generate_two_address_instruction(Opcode.MOV, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.DIRECT_REG, 
                                                                        iden.value,
                                                                        0x2))
            elif(isinstance( nd.children[0].children[1], literal)):
                self.main.append(self.generator
                .generate_two_address_instruction(Opcode.LOAD, 
                                                    Mode.DIRECT_REG, 
                                                    Mode.ADDRESS, 0x2, 
                                                    nd.children[0].children[1].address))
            else:
                raise ValueError('dont know ')
            ret = None
            if(nd.value == '+'):
                ret = self.generator.generate_althmetic_instruction(Opcode.ADD, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0,  0x2)
            elif(nd.value == '-'):
                ret = self.generator.generate_althmetic_instruction(Opcode.SUB,  
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x2)
            elif(nd.value == '*'):
                ret = self.generator.generate_althmetic_instruction(Opcode.MUL, 
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                        0x0, 0x2)
            elif(nd.value == '/'):
                ret = self.generator.generate_althmetic_instruction(Opcode.DIV,
                                                                        Mode.DIRECT_REG,  
                                                                        Mode.DIRECT_REG, 
                                                                        0x0, 0x2)
            elif(nd.value == 'mod'):
                ret = self.generator.generate_althmetic_instruction(Opcode.MOD,  
                                                                       Mode.DIRECT_REG, 
                                                                       Mode.DIRECT_REG, 
                                                                       0x0, 0x2)
            else:
                raise TypeError('Missing mathematic operation!')
            for i in ret :
                self.main.append(i)
            self.main.append(self.generator.generate_one_address_instruction(Opcode.POP, 
                                                                 Mode.DIRECT_REG, 0x2))
            
    def visitLogicalNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('Expected 2 params on set command!')
        else:
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.PUSH, 
                                                                 Mode.DIRECT_REG, 
                                                                 0x2))
            
            if(isinstance(nd.children[0], expression)):
                self.visitExpressionNode(nd.children[0])
            elif(isinstance( nd.children[0], identifier)):
                iden = self.get_lastest_identifier(nd.children[0].value)
                if(iden.type == 'address'):
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.LOAD, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.ADDRESS, 
                                                                        0x0, iden.value))
                else:
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.MOV, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.DIRECT_REG, 
                                                                        iden.value,
                                                                        0x0))
            elif(isinstance( nd.children[0], literal)):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 
                                                                     0x0, 
                                                                     nd.children[0].address))
            else:
                raise ValueError('dont know ')
            
            if(isinstance(nd.children[1], expression)):
                self.main.append(self.generator.
                                 generate_one_address_instruction(Opcode.PUSH, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
                self.visitExpressionNode(nd.children[1])
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.MOV, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0, 0x2))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.POP, 
                                                                     Mode.DIRECT_REG, 
                                                                     0x0))
            elif(isinstance( nd.children[1], identifier)):
                iden = self.get_lastest_identifier(nd.children[1].value)
                if(iden.type == 'address'):
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.LOAD, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.ADDRESS, 
                                                                        0x2, iden.value))
                else :
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.MOV, 
                                                                        Mode.DIRECT_REG, 
                                                                        Mode.DIRECT_REG, 
                                                                        iden.value, 
                                                                        0x2))
            elif(isinstance( nd.children[1], literal)):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.LOAD, 
                                                                     Mode.DIRECT_REG, 
                                                                     Mode.ADDRESS, 0x2, 
                                                                     nd.children[1].address))
            else:
                raise ValueError('dont know ')
            if(nd.value == '>'):
                self.main.append(self.generator
                             .generate_two_address_instruction(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                    
            elif(nd.value == '<'):
                self.main.append(self.generator
                             .generate_two_address_instruction(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x2,
                                                                    0x0))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
            elif(nd.value == '='):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                
            elif(nd.value == '>='):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0x2))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 3))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
                
            elif(nd.value == '<='):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.CMP,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x2,
                                                                    0x0))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BGT,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 3))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BEQ,
                                                                     Mode.VALUE,
                                                                     len(self.main) + 2))
            else:
                raise TypeError('Missing logical operation!')
            
            self.main.append(self.generator
                             .generate_two_address_instruction(Opcode.LOAD,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0x0,
                                                                    0x0))
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.JMP,
                                                                    Mode.VALUE,
                                                                    len(self.main) + 1))
            self.main.append(self.generator
                             .generate_two_address_instruction(Opcode.LOAD,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0x0,
                                                                    0x1))
            
    def visitIfNode(self, nd: node):
        if(len(nd.children) < 2 or len(nd.children) > 3) :
            raise AttributeError('if <clause> <exp-1> (<exp-2>)')
        else:
            first_inst_jmp = 0
            second_exp_addr = 0
            after_exp = 0
            self.visitExpressionNode(nd.children[0])
            self.main.append(self.generator.
                             generate_two_address_instruction(Opcode.CMP, 
                                                                 Mode.DIRECT_REG, 
                                                                 Mode.VALUE,
                                                                 0x0, 0x0))
            if(len(nd.children) == 2):
                first_inst_jmp = len(self.main)
                self.main.append(self.generator.
                                 generate_one_address_instruction(Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    after_exp))
                self.visitExpressionNode(nd.children[1])
                after_exp = len(self.main) + 1
                self.main[first_inst_jmp] = self.generator.generate_one_address_instruction(Opcode.BEQ,
                                                                                            Mode.VALUE,
                                                                                            after_exp)
# hard to explain, but if condition : if (condition) (expression) [after if]
# then if condition is false, jump to [after if], but since we didn't visit expression yet, 
# we don't know what is exactly address that we will jump to
# so strategy is jump to a blind address , and after visit expression , we go back to correct that instruction
# same with if (condidtion) (expression) [1] (expression)[2]
#  if condition false : jump to [1], else after first expression, jump to [2])
            if(len(nd.children) == 3):
                first_inst_jmp = len(self.main) # jump if condition is false
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    first_inst_jmp))
                self.visitExpressionNode(nd.children[1])
                second_exp_addr = len(self.main) #jump to ret
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.JMP,
                                                                     Mode.VALUE, 
                                                                     after_exp))
                self.visitExpressionNode(nd.children[2])
                after_exp = len(self.main)
                self.main[first_inst_jmp] = self.generator.generate_one_address_instruction(
                                                                    Opcode.BEQ,
                                                                    Mode.VALUE,
                                                                    second_exp_addr + 1)
                self.main[second_exp_addr] = self.generator.generate_one_address_instruction(
                                                                    Opcode.JMP,
                                                                    Mode.VALUE,
                                                                    after_exp)
                
    def visitWhileNode(self, nd : node):
        if(len(nd.children) != 2):
            raise AttributeError('while <condition> <expression>')
        else:
            while_begin = len(self.main)
            self.visitExpressionNode(nd.children[0])
            self.main.append(self.generator
                             .generate_two_address_instruction(Opcode.CMP,
                                                                 Mode.DIRECT_REG,
                                                                 Mode.VALUE,
                                                                 0x0,
                                                                 0x0))
            first_instr_jmp = len(self.main)
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.BEQ,
                                                                 Mode.VALUE,
                                                                 0x0))
            self.visitExpressionNode(nd.children[1])
            self.main.append(self.generator
                             .generate_one_address_instruction(Opcode.JMP,
                                                                 Mode.VALUE,
                                                                 while_begin))
            self.main[first_instr_jmp] = self.generator.generate_one_address_instruction(
                                                                 Opcode.BEQ,
                                                                 Mode.VALUE,
                                                                 len(self.main))
    
    def visitReturnNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError('return <expression>')
        else:
            if(isinstance( nd.children[0], literal)):
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.LOAD,
                                                                     Mode.DIRECT_REG,
                                                                     Mode.ADDRESS,
                                                                     0x0,
                                                                     nd.children[0].address))
            elif(isinstance(nd.children[0], identifier)):
                iden = self.get_lastest_identifier(nd.children[0].value)
                if(iden.type == 'address'):
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.LOAD,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.ADDRESS,
                                                                        0x0,
                                                                        iden.value))
                else:
                    self.main.append(self.generator
                                    .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        iden.value,
                                                                        0x0))
            elif(isinstance( nd.children[0], expression)):
                self.visitExpressionNode(nd.children[0])
            else:
                raise SyntaxError('Expression is not bounded!')
            
    
    def printString(self, addr):
        self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.PUSH,
                                                                    Mode.DIRECT_REG,
                                                                    0xA))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.PUSH,
                                                            Mode.DIRECT_REG,
                                                            0x0))
        self.main.append(self.generator
                            .generate_two_address_instruction(Opcode.MOV,
                                                            Mode.DIRECT_REG,
                                                            Mode.ADDRESS,
                                                            0x0,
                                                            addr))
        ops = self.generator.generate_althmetic_instruction(Opcode.AND,
                                                                Mode.DIRECT_REG,
                                                            Mode.VALUE,
                                                            0x0,
                                                            0xFFFF)
        for i in ops : 
            self.main.append(i)
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.PUSH,
                                                            Mode.DIRECT_REG,
                                                            0x03))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.PUSH,
                                                            Mode.DIRECT_REG,
                                                            0x01))
        self.main.append(self.generator
                            .generate_two_address_instruction(Opcode.MOV,
                                                            Mode.DIRECT_REG,
                                                            Mode.DIRECT_REG,
                                                            0x3,
                                                            0x0))
        addr1 = len(self.main)
        self.main.append(self.generator
                            .generate_two_address_instruction(Opcode.MOV,
                                                            Mode.DIRECT_REG,
                                                            Mode.VALUE,
                                                            0x1,
                                                            0x0))
        self.main.append(self.generator
                    .generate_two_address_instruction(Opcode.CMP,
                                                        Mode.DIRECT_REG,
                                                        Mode.DIRECT_REG,
                                                        0x3,
                                                        0x1))
        addr2 = len(self.main)
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.BGT,
                                                            Mode.VALUE,
                                                            0x00))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.OUT,
                                                            Mode.INDIRECT_REG,
                                                            0x1))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.JMP,
                                                            Mode.VALUE,
                                                            addr1))
        self.main[addr2] = self.generator.generate_one_address_instruction(Opcode.BGT,
                                                                            Mode.VALUE,
                                                                            len(self.main))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.POP,
                                                            Mode.DIRECT_REG,
                                                            0x01))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.POP,
                                                            Mode.DIRECT_REG,
                                                            0x03))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.POP,
                                                            Mode.DIRECT_REG,
                                                            0x00))
    def printNumber(self, addr):
        self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.LOAD,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.VALUE,
                                                                    0xA,
                                                                    addr))
        self.main.append(self.generator
                            .generate_one_address_instruction(Opcode.OUT,
                                                            Mode.DIRECT_REG,
                                                            0xA))
    def visitPrintNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError('print <identifier>/ literal / <expression>')
        else:
            self.main.append(self.generator
                             .generate_zero_address_instruction(Opcode.DI))
            if(isinstance( nd.children[0], integer)
               or isinstance( nd.children[0], boolean)):
                self.printNumber(nd.children[0].address)
            elif(isinstance( nd.children[0], string)):
                self.printString(nd.children[0].address)
            elif(isinstance( nd.children[0], expression)):
                self.visitExpressionNode(nd.children[0])
                self.main.append(self.generator
                                 .generate_two_address_instruction(Opcode.MOV,
                                                                    Mode.DIRECT_REG,
                                                                    Mode.DIRECT_REG,
                                                                    0x0,
                                                                    0xA))
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.OUT,
                                                                    Mode.DIRECT_REG,
                                                                    0xA))
            elif(isinstance(nd.children[0], identifier)):
                iden = self.get_lastest_identifier(nd.children[0].value)
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.PUSH,
                                                                    Mode.DIRECT_REG,
                                                                    0x0))
                self.main.append(self.generator.generate_two_address_instruction(Opcode.MOV,
                                                                                 Mode.DIRECT_REG,
                                                                                 Mode.ADDRESS,
                                                                                 0x0, 
                                                                                 iden.value))
                self.main.append(self.generator.generate_two_address_instruction(Opcode.LSR,
                                                                                 Mode.DIRECT_REG,
                                                                                 Mode.VALUE,
                                                                                 0x0,
                                                                                 31))
                self.main.append(self.generator.generate_two_address_instruction(Opcode.CMP,
                                                                               Mode.DIRECT_REG,
                                                                               Mode.VALUE,
                                                                               0x0,
                                                                               0x1))
                self.main.append(self.generator.generate_one_address_instruction(Opcode.BEQ,
                                                                                 Mode.VALUE,
                                                                                 len(self.main) + 4))
                self.printNumber(iden.value)
                self.main.append(self.generator.generate_one_address_instruction(Opcode.JMP,
                                                                                 Mode.VALUE,
                                                                                 len(self.main) + 17))
                self.printString(iden.value)     
                self.main.append(self.generator
                                 .generate_one_address_instruction(Opcode.POP,
                                                                    Mode.DIRECT_REG,
                                                                    0x0))   
            else :
                pass

            self.main.append(self.generator
                             .generate_zero_address_instruction(Opcode.EI))
            
    def visitInputNode(self, nd : node):
        if(len(nd.children) != 1):
            raise AttributeError("input <identifier>")
        if(isinstance(nd.children[0], identifier) == False):
            raise TypeError('Require input identifier')
        # save begin address of string
        self.main.append(self.generator
                         .generate_two_address_instruction(Opcode.MOV,
                                                            Mode.DIRECT_REG,
                                                            Mode.DIRECT_REG,
                                                            0x9, 
                                                            0x8))
        
        self.main.append(self.generator
                         .generate_zero_address_instruction(Opcode.DI))
        
        self.main.append(self.generator
                         .generate_one_address_instruction(Opcode.IN,
                                                            Mode.DIRECT_REG,
                                                            0xA))
        self.main.append(self.generator
                         .generate_two_address_instruction(Opcode.CMP,
                                                            Mode.DIRECT_REG,
                                                            Mode.VALUE,
                                                            0xA,
                                                            0xD))
        addr2 = len(self.main)
        # neu the, lenh DI phai tao ra 1 instruction dau tien luu do dai cua chuoi, va tang 0x9 len 1
        self.main.append(self.generator
                         .generate_one_address_instruction(Opcode.BEQ,
                                                            Mode.VALUE,
                                                            0x0))
        self.main.append(self.generator
                         .generate_two_address_instruction(Opcode.MOV,
                                                            Mode.INDIRECT_REG,
                                                            Mode.DIRECT_REG,
                                                            0x9,
                                                            0xA))
        self.main.append(self.generator
                         .generate_one_address_instruction(Opcode.INC,
                                                            Mode.DIRECT_REG,
                                                            0x9))
        self.main[addr2] = self.generator.generate_one_address_instruction(Opcode.BEQ,
                                                                         Mode.VALUE,
                                                                         len(self.main))
        self.main.append(self.generator
                         .generate_zero_address_instruction(Opcode.EI))
        # EI dieu chinh 0x9 = 0x8

        # 0x8 : begin heap 0x9 : current pointer to heap

    def visitCallNode(self, nd : node):
        if(len(nd.children) != 2):
            raise SyntaxError('call function (expression)')
        else:
             if(len(nd.children[1].children) >= 1):
                 self.main.append(self.generator
                                  .generate_one_address_instruction(Opcode.PUSH,
                                                                    Mode.DIRECT_REG,
                                                                    0x7))
                 if(isinstance(nd.children[1].children[0], literal)):
                     self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.ADDRESS,
                                                                        0x7,
                                                                        nd.children[1]
                                                                        .children[0]
                                                                        .address))
                 elif(isinstance(nd.children[1].children[0], identifier)):
                  iden = self.get_lastest_identifier(nd.children[1].children[0].value)
                  if(iden != None):
                      if(iden.type == 'address'):
                          self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.ADDRESS,
                                                                        0x7,
                                                                        iden.value))
                      else:
                          self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        0x7,
                                                                        iden.value))
                 elif(isinstance( nd.children[1].children[0], expression)):
                     self.main.append(self.generator
                                      .generate_one_address_instruction(Opcode.PUSH,
                                                                        Mode.DIRECT_REG,
                                                                        0x0))
                     self.visitExpressionNode(nd.children[1].children[0])
                     self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        0x7,
                                                                        0x0))
                     self.main.append(self.generator
                                      .generate_one_address_instruction(Opcode.POP,
                                                                        Mode.DIRECT_REG,
                                                                        0x0))
                 else:
                    pass
             if(len(nd.children[1].children) == 2):
                 self.main.append(self.generator
                                  .generate_one_address_instruction(Opcode.PUSH,
                                                                    Mode.DIRECT_REG,
                                                                    0x6))
                 if(isinstance( nd.children[1].children[1], literal)):
                     self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.ADDRESS,
                                                                        0x6,
                                                                        nd.children[1]
                                                                        .children[1]
                                                                        .address))
                 elif(isinstance(nd.children[1].children[1], identifier)):
                  iden = self.get_lastest_identifier(nd.children[1].children[1].value)
                  if(iden != None):
                      if(iden.type == 'address'):
                          self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.ADDRESS,
                                                                        0x6,
                                                                        iden.value))
                      else:
                          self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        0x6,
                                                                        iden.value))
                 elif(isinstance( nd.children[1].children[1], expression)):
                     self.visitExpressionNode(nd.children[1].children[1])
                     self.main.append(self.generator
                                      .generate_one_address_instruction(Opcode.PUSH,
                                                                        Mode.DIRECT_REG,
                                                                        0x0))
                     self.visitExpressionNode(nd.children[1].children[1])
                     self.main.append(self.generator
                                      .generate_two_address_instruction(Opcode.MOV,
                                                                        Mode.DIRECT_REG,
                                                                        Mode.DIRECT_REG,
                                                                        0x6,
                                                                        0x0))
                     self.main.append(self.generator
                                      .generate_one_address_instruction(Opcode.POP,
                                                                        Mode.DIRECT_REG,
                                                                        0x0))
             self.main.append(self.generator
                              .generate_two_address_instruction(Opcode.MOV,
                                                                Mode.DIRECT_REG,
                                                                Mode.VALUE,
                                                                0x3,
                                                                len(self.main) + 2))
             iden = self.get_lastest_identifier(nd.children[0].value)
             if(iden != None):
                self.main.append(self.generator
                                .generate_one_address_instruction(Opcode.JMP,
                                                                Mode.VALUE,
                                                                iden.value))
            #  if(len(nd.children[1].children) == 2):
            #     self.main.append(self.generator
            #                      .generate_one_address_instruction(Opcode.POP,
            #                                                         Mode.DIRECT_REG,
            #                                                         0x6))
            #  if(len(nd.children[1].children) >= 1):
            #     self.main.append(self.generator
            #                      .generate_one_address_instruction(Opcode.POP,
            #                                                         Mode.DIRECT_REG,
            #                                                         0x7))
                
    def visitDefunNode(self, nd : node):
        if(isinstance(nd, defun) == False):
            return
        self.identifier.append(
            identifier_raw(nd.children[0].value, 'address', len(self.main)))
        if(len(nd.children[1].children) == 2) :
            self.main.append(
                self.generator
                .generate_one_address_instruction(Opcode.POP,
                                                    Mode.DIRECT_REG,
                                                    0x7))
            self.main.append(
                self.generator
                .generate_one_address_instruction(Opcode.POP,
                                                Mode.DIRECT_REG,
                                                0x6))
            self.identifier.append(
                identifier_raw(nd.children[1].children[0].value, "register", 0x6))
            self.identifier.append(
                identifier_raw(nd.children[1].children[1].value, "register", 0x7))
        elif(len(nd.children[1].children) == 1) :
            self.main.append(
                self.generator
                .generate_one_address_instruction(Opcode.POP,
                                                    Mode.DIRECT_REG,
                                                    0x6))
            self.identifier.append(
                identifier_raw(nd.children[1].children[0].value, "register", 0x6))
        else:
            pass
        self.visitExpressionNode(nd.children[2])
        
        self.main.append(self.generator
                             .generate_zero_address_instruction(Opcode.RET))
        
    def visitExpressionNode(self, nd : node):
        for i in nd.children:
            if(isinstance(i, mathematic_operant)):
                self.visitMathNode(i)
            if(isinstance( i, logical_operant)):
                self.visitLogicalNode(i)
            if(isinstance( i, if_clause)):
                self.visitIfNode(i)
            if(isinstance(i, set)):
                self.visitSetNode(i)
            if(isinstance(i, let)):
                self.visitLetNode(i)
            if(isinstance( i, printf)):
                self.visitPrintNode(i)
            if(isinstance( i, defun)):
                self.visitDefunNode(i)
            if(isinstance(i, call)):
                self.visitCallNode(i)
            if(isinstance(i, input)):
                self.visitInputNode(i)
            if(isinstance(i, while_)):
                self.visitWhileNode(i)
            if(isinstance(i, return_)):
                self.visitReturnNode(i)
            if(isinstance(i, expression)):
                self.visitExpressionNode(i)

def generatemodeValue(mode, value):
    if(mode == 0x0):
        return " #" + hex(value)
    if mode == 0x1:
        return " [ #" + hex(value) + " ]"
    if mode == 0x2:
         return" " + "[ " + hex(value) + " ]"
    if mode == 0x3:
        return " " + hex(value)

def decodeAlthmeticInstruction(instr1, instr2):
    opcode = instr1 >> 24 & 0xFF
    mode1 = instr1 >> 22 & 0x3
    value1 = instr1 >> 16 & 0xF
    return Opcode.getname(opcode) + generatemodeValue(mode1, value1) + " " + str(hex(instr2))

def decodeInstruction(instruction):
    opcode = instruction >> 24 & 0xFF
    if(opcode == 0x80):
        return "- string length"
    if opcode in [0, 1, 25, 26, 31]:
        return Opcode.getname(opcode) 
    
    if opcode in [2, 3, 4, 5, 6, 7, 8, 9, 27]:
        mode = instruction >> 20 & 0xf
        value = instruction & 0xFFFF
        return Opcode.getname(opcode) + generatemodeValue(mode, value)
    
    if opcode in [10, 11, 19, 20, 21, 22, 23, 24]:
        mode1 = instruction >> 22 & 0x3
        mode2 = instruction >> 20 & 0x3
        value1 = instruction >> 16 & 0xF
        value2 = instruction & 0xFFFF

        return Opcode.getname(opcode) + generatemodeValue(mode1, value1) + generatemodeValue(mode2, value2)
    mode1 = instruction >> 22 & 0x3
    mode2 = instruction >> 20 & 0x3

    if(mode2 == 0x3):
        return 'althmetic'
    value1 = instruction >> 16 & 0xF
    value2 = instruction & 0xFFFF
    return str(Opcode.getname(opcode)) + generatemodeValue(mode1, value1) + generatemodeValue(mode2, value2) 
    

def createStackTrace(data):
    filepath = 'debug.txt'
    textToWrite = None
    with open(filepath, 'w') as f:
        for i in range(len(data)):
            decode = decodeInstruction(data[i])
            if(decode == 'althmetic'):
                textToWrite = hex(i) + ' ' + hex(data[i]) + ' ' + decodeAlthmeticInstruction(data[i], data[i + 1])
                i = i + 1
            else:
                textToWrite = hex(i) + ' ' + hex(data[i]) + ' ' + decode
            f.write(textToWrite)
            f.write('\n')
    f.close()

def translate(root :node):
    visit = visitor()
    visit.main.append(0x0)
    visit.setLiteralAddress(root)
    visit.setFunctionNode(root)
    
    visit.main[0] = len(visit.main)
    visit.visitExpressionNode(root)
    visit.main.append(visit.generator
                      .generate_zero_address_instruction(Opcode.HALT))
    filepath = 'test.bin'
    with open(filepath, 'wb') as file:
        for i in visit.main:
            bin_data = struct.pack('q', i)
            file.write(bin_data)
    file.close()

    createStackTrace(visit.main)
















    
                
            