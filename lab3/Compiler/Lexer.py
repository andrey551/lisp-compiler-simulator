from Compiler.Semantic import *
import re
class Lexer:
    def __init__(self, source : __file__):
        self.source = source
        self.hasher = []
        self.tokens = []
    def get_hasher(self):
        temp = []
        for line in self.source.read().splitlines():
            for i in re.split('(")', line):
                if(i != ''):
                    temp.append(i)
        i = 0
        while (i < len(temp)):
            if(temp[i] == '"'):
                str = '"'
                i += 1
                while (temp[i] != '"'):
                    str += temp[i]
                    i += 1
                str += temp[i]
                self.hasher.append(str)
            else :
                for t in temp[i].split(' '):
                    for a in re.split(r'(\()', t):
                        for b in re.split(r'(\))', a):
                            if(len(b) > 0):
                                if(SPECIAL_CHARACTER.is_Special_Character(b[0])):
                                    # self.hasher.append(b[0])
                                    if(len(b[slice(1,-1)]+ b[-1]) > 0):
                                        self.hasher.append(b[slice(1,-1)] + b[-1]) 
                                else:
                                    self.hasher.append(b)
            i += 1

    def get_tokens(self):
        for i in self.hasher:
            if(i != ''):
                self.tokens.append(to_Token(i))
    def print_Tokens(self):
        for i in self.tokens:
            print(i , '\n')
                                   

