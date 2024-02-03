class Logic_Executor:
    def __init__(self, operand_1, operand_2 = None):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
    def AND(self):
        return self.operand_1 & self.operand_2
    def OR(self):
        return self.operand_1 | self.operand_2
    def NOT(self):
        return ~self.operand_1 & 0xFFFF