import struct
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from Semantic import Opcode, Mode


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
    def execute(self, to : Register):
        to.set(self.conn[self.latch])
    def setConn(self, conn ):
        self.conn = conn
    def setConnAt(self, index, value):
        self.conn[index] = value
class Memory():
    def __init__(self):
        self.data = []
        self.length = 65536

    def read(self, address: int):
        return self.data[address]
    def write(self, address, value):
        self.data[address] = value
    def load(self, fileName : str):
        with open (fileName, mode = 'rb') as file:
            fileContent = file.read()
            filelen =  (int(len(fileContent)/ 8))
            for i in range (filelen):
                self.data.append(
                    struct.unpack('q' * filelen, 
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
    def getOp(value):
        for i in AluOp:
            if (i.value == value):
                return i
        
        raise ValueError("enum type not found!")


ALU_OP : dict[AluOp, Callable[[int, int], int]] = {
    AluOp.ADD: lambda  left, right: left + right,
    AluOp.SUB: lambda left, right: left - right,
    AluOp.MUL: lambda left, right: left * right,
    AluOp.DIV: lambda left, right: int(left / right),
    AluOp.MOD: lambda left, right: left % right,
    AluOp.AND: lambda left, right: left & right,
    AluOp.OR: lambda left, right : left | right,
    AluOp.NOT: lambda left, right: left | ~right
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

    def getReg(value):
        for i in GeneralRegister:
            if (i.value == value):
                return i
        
        raise ValueError("enum type not found!")
    
@dataclass
class pcSelSignal(Enum):
    branch = 0x0
    plusOne = 0x1a

@dataclass
class drSelSignal(Enum):
    regSignal = 0x0
    memSignal = 0x1
    valueSignal = 0x2
    inSignal = 0x3

@dataclass
class leftSignal(Enum):
    arSgnal = 0x0
    acSignal = 0x1
    zero = 0x2

@dataclass
class rightSignal(Enum):
    zero = 0x0
    oneSignal = 0x1
    drSignal = 0x2
    
@dataclass 
class arSelSignal(Enum):
    memSignal = 0x0
    valueSignal = 0x1
    addrSignal = 0x2
    
class RegisterFile():
    def __init__(self):
        self.regs  = [Register]
        for i in range(16):
            self.regs.append(Register())
        self.addr : int = 0x0
        self.value : int = 0x0
    def write(self, 
              reg : GeneralRegister, 
              value: int):
        self.regs[reg.value] = value
    def read(self,
             reg : GeneralRegister):
        return self.regs[reg.value].value
    def sync(self):
        self.value = self.regs[self.addr].get()

@dataclass
class IOState(Enum):
    Lock = 0
    Unlock = 1

class InPort():
    def __init__(self, src = None):
        self.src = src
    def setSrc(self, src):
        self.src = src
    def read(self) -> [int]: # type: ignore
        with open(self.src , 'r') as file :
            content = file.read
        ascii_code = [ord(char) for char in list(content)]
        file.close()
        return ascii_code
    
class OutPort():
    def __init__(self, dest = None):
        self.dest = dest
    def setDest(self, dest):
        self.dest = dest
    def write(self, data):
        chars = [chr(code) for code in data]
        with open(self.dest, 'w') as file :
            file.write.join(''.join(chars))
        
        file.close()

class IOBuffer():
    def __init__(self, inPort, outPort):
        self.size = 4096
        self.iter = 0
        self.memory = []
        self.inPort = inPort
        self.outPort = outPort
    def checkOverflow(self):
        if(len(self.memory) > self.size):
            raise OverflowError('Buffer overflow')
    def storeData(self, char):
        self.checkOverflow()
        self.memory.append(char)
    def retrieveData(self) -> int:
        if len(self.memory) == 0 :
            raise BufferError('Failure when trying to read empty buffer')
        ret = self.memory[len(self.memory - 1)]
        self.memory.pop(-1)
        return ord(ret)
    def loadDataIn(self):
        self.data = self.inPort.read()
        self.checkOverflow()
    def loadDataOut(self):
        self.outPort.write(self.memory)
        self.memory.clear()
    
class InterruptHandler():
    def __init__(self, buffer : IOBuffer):
        self.state : IOState = IOState.Unlock
        self.value = 0x0
        self.buffer = buffer
    def lock(self):
        self.state = IOState.Lock
    def unlock(self):
        self.state = IOState.Unlock
        self.buffer.loadDataOut()
    def checkUnlocked(self):
        if self.state == IOState.Lock:
            raise InterruptedError('Interrupt is not opened yet!')
    def inSignal(self):
        self.checkUnlocked()
        self.value = ord(self.buffer.retrieveData())
    def outSignal(self):
        self.checkUnlocked()
        self.buffer.storeData(chr(self.value))
    def getState(self):
        return self.state
    def getNextValue(self, buffer):
        self.value = buffer.extractValue()
    def writeToBuffer(self, buffer):
        buffer.insertData(self.value)

##########################
class InstructionType(Enum):
    ZeroAttribute = 0x0
    OneAttribute = 0x1
    TwoAttribute = 0x2
    AlthmeticInstruction = 0x3
    
class InstructionDecoder():
    def __init__(self):
        self.opcode : Opcode
        self.type : InstructionType
        self.mode_1 : Mode
        self.mode_2 : Mode
    def decode(self, ir: Register):
        value = ir.get()
        self.opcode = Opcode.getname(value >> 24 & 0xFF)
        if self.opcode in [ 0, 1, 25, 26, 31]:
            self.type = InstructionType.ZeroAttribute
        elif self.opcode in [2, 3, 4, 5, 6, 7, 8, 9, 27]:
            self.type = InstructionType.OneAttribute
        elif self.opcode in [10, 11, 19, 20, 21, 22, 23, 24]:
            self.type = InstructionType.TwoAttribute
        else:
            self.type = InstructionType.AlthmeticInstruction
        self.mode_1 = Mode.getMode(value >> 22 & 0x3)
        self.mode_2 = Mode.getMode(value >> 20 & 0x3)

class GenerateSignal():
    def __init__(self):
        self.selReg : int
        self.isReg : bool
        self.isAddr : bool
        self.isVal : bool
        self.isBranch : bool
        self.isWriteReg : bool
        self.input : bool
        self.output : bool

        self.PCsel : pcSelSignal
        self.DRsel : drSelSignal
        self.leftsel : leftSignal
        self.rightsel : rightSignal
        self.althmetic : AluOp

    def generate(self, decoder : InstructionDecoder):
        pass
class NextGenerateState():
    def __int__(self):
        pass

class TimingUnit():
    def __init__(self):
        self.tick = 0
    def inc(self):
        self.tick = self.tick + 1
    def getTick(self):
        return self.tick