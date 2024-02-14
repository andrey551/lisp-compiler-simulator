import struct
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, cast


MAX_INT = 2^30
MIN_INT = -2^30
class Register():
    def __init__(self):
        self.value = 0xFFFFFFFF
    def set(self, value):
        self.value = value
    def get(self):
        return self.value
    def get_bit_at(self, index : int):
        return self.value >> index & 0x1
    def get_byte_at(self, index : int):
        return (self.value >> (index * 4 - 1)) & 0xF


class Flag():
    def __init__(self):
        self.value = False
    def set(self, val) :
        self.value = val
    def get(self):
        return self.value

class Mux():
    def __init__(self):
        self.conn = []
        self.latch = 0x0
    def execute(self, to : Register):
        to.set(self.conn[self.latch])
    def setLatch(self, latch : int):
        self.latch = latch
    def setConn(self, conn : [Register]):
        self.conn = conn
class Memory():
    def __init__(self):
        self.data = []
        self.length = 65536
    def read(self, address: int):
        return self.data[address]
    def write(self, address, value):
        self.data[address] = value
    def load(self, fileName : str, numOfInstr : int):
        with open (fileName, mode = 'rb') as file:
            fileContent = file.read()
            for i in range (int(len(fileContent)/ 8)):
                self.data.append(
                    struct.unpack('q' * int(len(fileContent)/ 8), 
                                  fileContent))
        file.close()
        for i in range(len(self.data), self.length):
            self.data.append(None)

class AluOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    AND = 5
    OR = 6
    NOT = 7
    CMP = 8

ALU_OP : dict[AluOp, Callable[[int, int], int]] = {
    AluOp.ADD: lambda  left, right: left + right,
    AluOp.SUB: lambda left, right: left - right,
    AluOp.MUL: lambda left, right: left * right,
    AluOp.DIV: lambda left, right: int(left / right),
    AluOp.MOD: lambda left, right: left % right,
    AluOp.AND: lambda left, right: left & right,
    AluOp.OR: lambda left, right : left | right,
    AluOp.NOT: lambda left, right: ~left
}

class ALU():
    def __init__(self):
        self.p : bool = False
        self.z : bool = False
    def execute(self, op: AluOp, left : int, right : int = 0) -> int:
        operant = ALU_OP[op]
        ret = operant(left, right)
        ret = self.handle_overflow(ret)
        self.set_flags(ret)
        return ret
    def set_flags(self, value):
        self.p = value > 0
        self.z = value == 0
    @staticmethod
    def handle_overflow(value : int) -> int:
        if value > MAX_INT :
            return   value - MAX_INT
        if value < MIN_INT :
            return value - MIN_INT
        return value
@dataclass
class GeneralRegister(Enum):
    rax = 0x0 
    rbx = 0x3
    rcx = 0x1
    rdx = 0x2
    rsp = 0x4
    sbp = 0x5
    rsi = 0x6
    rdi = 0x7
    rhb = 0x8
    rhp = 0x9
    rio = 0xA
    r11 = 0xB
    r12 = 0xC
    r13 = 0xD
    r14 = 0xE
    r15 = 0xF

class RegisterFile():
    def __init__(self):
        self.regs : [Register] = []
        for i in range(16):
            self.regs.append(Register())
    def write(self, 
              reg : GeneralRegister, 
              value: int):
        self.regs[reg.value] = value
    def read(self,
             reg : GeneralRegister):
        return self.regs[reg.value]

@dataclass
class IOState(Enum):
    Lock = 0
    Unlock = 1
class InterruptHandler():
    def __init__(self):
        self.state : IOState = IOState.Unlock
    def lock(self):
        self.state = IOState.Lock
    def unlock(self):
        self.state = IOState.Unlock
    def getState(self):
        return self.state

class InPort():
    def receiveData(self, src):
        pass
class OutPort():
    def sendData(self, data):
        pass

class IOBuffer():
    def __init__(self):
        self.size = 4096
        self.iter = 0
        self.memory = []
    def outProcess(self, data, port : OutPort, handler : InterruptHandler):
        if(handler.state == IOState.Lock):
            return
        if(self.iter < self.size):
            self.memory.append(data)
            self.iter = self.iter + 1
        else:
            port.sendData(self.memory)
            self.memory.clear()
            self.iter = 0
    def inProcess(self, port : InPort, handler : InterruptHandler):
        if(handler.state == IOState.Lock):
            return
        port.receiveData("")
