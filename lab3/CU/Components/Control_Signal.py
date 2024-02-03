
class Control_Signal():
    def __init__(self, status):
        self.status = status
    def set_status(self, status):
        self.status = status

# first 4 bit store type of signal
# last 4 bit store value of signal

# 0: RegDst {0: $rt, 1: $rd} | Decode | Select the destination register number
# 1: RegWrite {0: no write, 1: write} | Decode/Writeback | Enable writing of register
# 2: ALUSrc {0: $rt, 1: immediate} | ALU | Select the 2nd operand for ALU
# 3: ALUcontrol {0: AND, 1: OR, 2: ADD, 6: SUB, 7: SLT, C: NOR} | ALU | Select the operation to be performed by the ALU
# 4: MemRead { 0: no read, 1: read} | Memory | Enable reading of data memory
# 5: MemWrite { 0: no write, 1: write} | Memory | Enable writing of data memory
# 6: MemToReg { 0: ALU result, 1: memory data} | Writeback | Select the result to be written back to register file
# 7: Branch {0: $PC+4, 1: ($PC+4)+(immediate×4) } | Memory/Writeback | Select the next $PC value