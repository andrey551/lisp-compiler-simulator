from enum import Enum
import re
class SPECIAL_CHARACTER(Enum):
    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    QUOTE = '\''         # Denotes literal data or prevents evaluation of an expression
    BACKQUOTE = '`'      # Used for quasi-quotation, a mechanism for constructing templates
    COMMA = ','          # Used in conjunction with backquote for unquoting within quasi-quoted expressions
    PERIOD = '.'         # Separates the elements of a cons cell in a dotted pair notation
    COLON = ':'          # Often used in keywords and package prefixes
    SHARP = '#'          # Introduces various reader macros
    AMPERSAND = '&'      # Used in special parameters in lambda lists for specifying various kinds of argument passing
    PERCENTAGE = '%'     # Used in some Lisps for special variables

    @classmethod
    def is_Special_Character(self, word):
        try:
            SPECIAL_CHARACTER(word)
            return True
        except ValueError:
            return False
    @classmethod
    def get_Name(self, word):
        return SPECIAL_CHARACTER(word).name
class MATH_OPERATOR(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTI = '*'
    DIVIDE = '/'
    EXPONENT = 'expt'
    SQUARE_ROOT = 'sqrt'
    ABSOLUTE = 'abs'
    MODULO = 'mod'

    @classmethod
    def is_Math_Operator(self, word):
        try:
            MATH_OPERATOR(word)
            return True
        except ValueError:
            return False
class LOGICAL_OPERATOR(Enum):
    GREATER = '>'
    EQUAL = '='
    LESS = '<'
    NOT_EQUAL = '/='
    LOE = '<='
    GOE = '>='
    OR = '|'
    AND = '&'
    NOT = '~'

    @classmethod
    def is_Logical_Operator(self, word):
        try:
            LOGICAL_OPERATOR(word)
            return True
        except ValueError:
            return False
class KEYWORD(Enum):
    LET = 'let'
    IF = 'if'
    SET = 'set'
    DEFINE_FUNC = 'defun'
    LOOP = 'loop'
    PRINT = 'format'
    INPUT = 'input'
    FOR = 'for'
    DO = 'do'
    FROM = 'from'
    TO = 'to'
    WHILE = 'while'
    RETURN = 'return'
    CALL = 'call'
    @classmethod
    def is_Keyword(self,word):
        try:
            KEYWORD(word)
            return True
        except ValueError:
            return False
def is_Integer(word):
    return bool(re.compile(r'^[+-]?\d+$').match(word))
def is_Float(word):
    return bool(re.compile(r'^[+-]?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?$').match(word))
def is_String(word):
    if(word[0] == '"' and word[-1] == '"'):
        return True
    return False
def is_Boolean(word):
    if(word == 'true' or word == 'false'):
        return True
    return False
def to_Token(word):
    if(SPECIAL_CHARACTER.is_Special_Character(word)):
        return {SPECIAL_CHARACTER.get_Name(word) : word}
    if(MATH_OPERATOR.is_Math_Operator(word)):
        return {'MATHEMATIC_OPERATION' : word }
    if(LOGICAL_OPERATOR.is_Logical_Operator(word)):
        return {'LOGICAL_OPERATION' : word}
    if(KEYWORD.is_Keyword(word)):
        return {'KEYWORD' : word}
    if(is_Integer(word)):
        return {'INTEGER' : word}
    if(is_Float(word)):
        return {'FLOAT' : word }
    if(is_Boolean(word)):
        return {'BOOLEAN' : word}
    if(is_String(word)):
        return {'STRING' : word}
    return {'IDENTIFIER' : word}

class Opcode(Enum):
    RET = 1
    NOP = 0
    HALT = 31
    DI = 25
    EI = 26
    JMP = 2
    CALL = 3
    BEQ = 4
    BGT = 5
    IN = 6
    OUT = 7
    PUSH = 8
    POP = 9
    LOAD = 10
    STORE = 11
    CMP = 22
    MOV = 23
    NOT = 24
    ADD = 12
    SUB = 13
    MUL = 14
    DIV = 15
    MOD = 16
    AND = 17
    OR = 18
    LSL = 19
    LSR = 20
    ASR = 21
    INC = 27
class Mode(Enum):
    DIRECT_REG = 0
    INDIRECT_REG = 1
    ADDRESS = 2
    VALUE = 3
class code_generate():
    def __init__(self):
        self.desc = []
    def generate_zero_address_instruction(self, op : Opcode):
        return op.value << 24
    def generate_one_address_instruction(self, op : Opcode, mode : Mode, src):
        if(mode == Mode.DIRECT_REG 
           or mode == Mode.INDIRECT_REG):
            return op.value << 24 | mode.value << 20 | src << 16
        elif(mode == Mode.ADDRESS 
             or mode == Mode.VALUE):
            return op.value << 24 | mode.value << 20 | src << 4
    def generate_two_address_instruction(self, 
                             op: Opcode, 
                             mode_1 : Mode, 
                             mode_2 : Mode, 
                             src1, 
                             src2):
        if(mode_1.value > 1):
            raise ValueError('opcode <reg> <reg/address>')
        else :
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                return op.value << 24 | (mode_1.value << 2 | mode_2.value) << 20 |  src1 << 16 | src2 << 12
            else :
                return op.value << 24 | (mode_1.value << 2 | mode_2.value) << 20 |  src1 << 16 | src2

    def generate_althmetic_instruction(self,
                               op: Opcode,
                               mode_1: Mode,
                               mode_2: Mode,
                               src1,
                               src2):
        if(mode_1.value > 1):
           raise ValueError('opcode <reg> <reg/address>')
        else:
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                return [op.value << 24 | (mode_1.value << 2 | mode_2.value) << 20 |  src1 << 16 | src2 << 12]
            else:
                return [op.value << 24 | (mode_1.value << 2 | mode_2.value) << 20 |  src1 << 16, src2]
        
    def generate_int(self, value):
        return int(value) & 0x7FFFFFFF
    def generate_bool(self, value):
        return int(value) & 0x7FFFFFFF
    def generate_string(self, value):
        ret = []
        ret.append(0x80000000 | len(value) - 2)
        for i in range(1, len(value) - 1):
            ret.append(ord(value[i]))
        return ret