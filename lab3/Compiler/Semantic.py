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

class code_generate():
    def generate_ret(self):
        return 0x10000000
    def generate_nop(self):
        return 0x00000000
    def generate_halt(self):
        return 0xF8000000
    def generate_di(self):
        return 0xC8000000
    def generate_ei(self):
        return 0xD0000000
    def generate_jmp(self, offset):
        return (0x1 << 28 | offset)
    def generate_call(self, offset):
        return (0x18 << 24 | offset)
    def generate_beq(self, offset):
        return (0x2 << 28 | offset)
    def generate_bgt(self, offset):
        return (0x28 << 24 | offset)
    def generate_in(self, offset):
        return (0x3<<28 | offset)
    def generate_out(self, offset):
        return (0x38 << 24 | offset)
    def generate_push(self, mode, src):
        if(mode == 0):
            return 0x4 << 28 | src << 14
        elif(mode == 1):
            return 0x44<< 24 | src
        else:
            pass
    def generate_pop(self,mode, src):
        if(mode == 0):
            return 0x48 << 24 | src << 14
        elif(mode == 1):
            return 0x4C<< 24 | src
        else:
            pass
    def generate_load(self, reg_des, reg_src, imm):
        return (((0x54 << 24 | reg_des << 22) | reg_src << 18) | imm)
    def generate_store(self, reg_des, reg_src, imm):
        return (((0x5C << 24 | reg_des << 22) | reg_src << 18) | imm)
    def generate_add(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x6<<28 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x6<<28 | mode << 26 |dest << 22 | src1 << 18 | src2
        else:
            pass
    def generate_sub(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x68 << 24 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x68 << 24 | mode << 26 |dest << 22 | src1 << 18 | src2
        else:
            pass 
    def generate_mul(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x7<<28 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x7<<28 | mode << 26 |dest << 22 | src1 << 18 | src2
    def generate_div(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x78<<24 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x78<<24 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_mod(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x8<<28 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x8<<28 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_and(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x88<<24 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x88<<24 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_or(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x9<<28 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x9<<28 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_lsl(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0x98<<24 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0x98<<24 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_lsr(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0xA<<28 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0xA<<28 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_asr(self, mode, dest, src1, src2):
        if(mode == 0):
            return 0xA8<<24 |dest << 22 | src1 << 18 | src2 << 14
        elif(mode == 1):
            return 0xA8<<24 | mode << 26 |dest << 22 | src1 << 18 | src2
        else :
            pass
    def generate_cmp(self, mode, reg_src_1, src2):
        if(mode == 0):
            return 0xB0 << 24 | reg_src_1 << 18 | src2 << 14
        elif(mode == 1):
            return 0xB4 << 24 | reg_src_1 << 18 | src2
    def generate_mov(self, mode, reg_dest, src):
            return 0xB0 << 24 |mode <<25 | reg_dest << 21 | src << 17
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