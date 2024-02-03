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
    LAMBDA = 'lambda'
    LET = 'let'
    IF = 'if'
    CONDITION = 'cond'
    QUOTE = 'quote'
    SET = 'setq'
    DEFINE_FUNC = 'defun'
    DEFINE_GLOBAL = 'defvar'
    DEFINE_MACRO = 'defmacro'
    LOOP = 'loop'
    PRINT = 'format'
    INPUT = 'readline'
    LIST = 'list'
    TEMP = 't'
    FOR = 'for'
    REPEAT = 'repeat'
    DO = 'do'
    DOTIMES = 'dotimes'
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