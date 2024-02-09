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
class Mode(Enum):
    DIRECT_REG = 0
    INDIRECT_REG = 1
    ADDRESS = 2
    VALUE = 3
class code_generate():

    def generate_zero_address(self, op : Opcode):
        return op.value
    def generate_one_address(self, op : Opcode, mode : Mode, src):
        if(mode == Mode.DIRECT_REG 
           or mode == Mode.INDIRECT_REG):
            return op.value << 6 | mode.value << 4 | src
        elif(mode == Mode.ADDRESS 
             or mode == Mode.VALUE):
            return op.value << 18 | mode.value << 16 | src
    def generate_two_address(self, 
                             op: Opcode, 
                             mode_1 : Mode, 
                             mode_2 : Mode, 
                             src1, 
                             src2):
        if(mode_1 == Mode.DIRECT_REG 
           or mode_1 == Mode.INDIRECT_REG):
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                return op.value << 12 | mode_1.value << 10 | mode_2.value << 8 | src1 << 4 | src2
            else :
                return op.value << 24 | mode_1.value << 22 | mode_2.value << 20 | src1 << 16 | src2
        else :
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                return op.value << 24 | mode_1.value << 22 | mode_2.value << 20 | src1 << 4 | src2
            else :
                return op.value << 36 | mode_1.value << 34 | mode_2.value << 32 | src1 << 16 | src2

    def generate_three_address(self,
                               op: Opcode,
                               mode_1: Mode,
                               mode_2: Mode,
                               mode_3: Mode,
                               src1,
                               src2,
                               src3):
        if(mode_1 == Mode.DIRECT_REG 
           or mode_1 == Mode.INDIRECT_REG):
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                if(mode_3 == Mode.DIRECT_REG
                    or mode_3 == Mode.INDIRECT_REG):
                    return op.value << 18 | mode_1.value << 16 | mode_2.value << 14 | mode_3 << 12| src1 << 8 | src2 << 4 | src3
                else:
                    return op.value << 30 | mode_1.value << 28 | mode_2.value << 26 | mode_3 << 24| src1 << 20 | src2 << 16 | src3
            else :
                if(mode_3 == Mode.DIRECT_REG
                    or mode_3 == Mode.INDIRECT_REG):
                    return op.value << 30 | mode_1.value << 28 | mode_2.value << 26 | mode_3 << 24| src1 << 20 | src2 << 4 | src3
                else:
                    return op.value << 42 | mode_1.value << 40 | mode_2.value << 38 | mode_3 << 36| src1 << 32 | src2 << 16 | src3
        else :
            if(mode_2 == Mode.DIRECT_REG
               or mode_2 == Mode.INDIRECT_REG):
                if(mode_3 == Mode.DIRECT_REG
                    or mode_3 == Mode.INDIRECT_REG):
                    return op.value << 30 | mode_1.value << 28 | mode_2.value << 26 | mode_3 << 24| src1 << 8 | src2 << 4 | src3
                else:
                    return op.value << 42 | mode_1.value << 40 | mode_2.value << 38 | mode_3 << 36| src1 << 20 | src2 << 16 | src3
            else :
                if(mode_3 == Mode.DIRECT_REG
                    or mode_3 == Mode.INDIRECT_REG):
                    return op.value << 42 | mode_1.value << 40 | mode_2.value << 38 | mode_3 << 36| src1 << 20 | src2 << 4 | src3
                else:
                    return op.value << 54 | mode_1.value << 52 | mode_2.value << 50 | mode_3 << 48| src1 << 32 | src2 << 16 | src3
    def generate_int(self, value):
        return value & 0x7FFFFFFF
    def generate_bool(self, value):
        return value & 0x7FFFFFFF
    def generate_string(self, value):
        ret = []
        ret.append(0x80000000 | len(value))
        i = 0
        while(i + 3 < len(value)):
            ret.append(ord(value[i]) << 24 
                       | ord(value[i + 1]) << 16 
                       | ord(value[i + 2]) << 8 
                       | ord(value[i + 3]))
            i = i + 4
        temp = 0xFFFFFFFF
        while(i < len(value)) :
            temp = temp & value[i] << (i % 4) * 8
        ret.append(temp)
        return ret