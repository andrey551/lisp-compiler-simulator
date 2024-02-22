import struct
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from lab3.Compiler.Semantic import Opcode, Mode, OutMode
import logging

MAX_INT = 2**30
MIN_INT = -2**30

class Register():
    def __init__(self):
        self.value = 0x0
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
        self.length = 4000

    def read(self, address: int):
        return self.data[address]
    def write(self, address, value):
        self.data[address] = value
    def load(self, fileName : str):
        iter = 0
        with open (fileName, mode = 'rb') as file:
            while True:
                fileContent = file.read(8)
                if not fileContent: 
                    break
                long_integer = struct.unpack('<q', fileContent)[0]
                self.data.append(long_integer)
                iter = iter + 1
        file.close()
        for i in range(iter, self.length + 1):
            self.data.append(0x0)
'''
I should use Opcode , but to lazy to replace them 
basically, this is Enum ALU's operator, which match with ALU_OP
'''
class AluOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    AND = 5
    OR = 6
    NOT = 7
    LSL = 8
    LSR = 9
    def getOp(value):
        for i in AluOp:
            if (i.value == value):
                return i
        
        raise ValueError("enum type not found!")

'''
callable ALU operator dictionary
'''
ALU_OP : dict[AluOp, Callable[[int, int], int]] = {
    AluOp.ADD: lambda  left, right: left + right,
    AluOp.SUB: lambda left, right: left - right,
    AluOp.MUL: lambda left, right: left * right,
    AluOp.DIV: lambda left, right: int(left / right),
    AluOp.MOD: lambda left, right: left % right,
    AluOp.AND: lambda left, right: left & right,
    AluOp.OR: lambda left, right : left | right,
    AluOp.NOT: lambda left, right: left | ~right,
    AluOp.LSL : lambda left, right : left << right & 0x8FFFFFFF,
    AluOp.LSR : lambda left, right : left >> right & 0x8FFFFFFF
}

class ALU():
    def __init__(self):
        self.left : int = 0x0
        self.right : int = 0x0
        self.p : bool = False
        self.z : bool = False
    def reset(self):
        self.left : int = 0x0
        self.right : int = 0x0
        self.p : bool = False
        self.z : bool = False
    def execute(self, op: AluOp) -> int:
        operant = ALU_OP[op]
        ret = operant(self.left, self.right)
        # ret = self.handle_overflow(ret)
        self.set_flags(ret)
        return ret
    def set_flags(self, value):
        self.p = value > 0
        self.z = value == 0

    @staticmethod
    def handle_overflow(value : int) -> int:
        if value > MAX_INT :
            print("max overflow")
            return   value - MAX_INT
        if value < MIN_INT :
            print("min overflow")
            return value - MIN_INT
        return value
    
'''
General register enum
basically, I only use to 0x9 but who know when I will need to use them ?
'''
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
    
# @dataclass
# class pcSelSignal(Enum):
#     branch = 0x0
#     plusOne = 0x1a

# @dataclass
# class drSelSignal(Enum):
#     regSignal = 0x0
#     memSignal = 0x1
#     valueSignal = 0x2
#     inSignal = 0x3

# @dataclass
# class leftSignal(Enum):
#     arSgnal = 0x0
#     acSignal = 0x1
#     zero = 0x2

# @dataclass
# class rightSignal(Enum):
#     zero = 0x0
#     oneSignal = 0x1
#     drSignal = 0x2
    
# @dataclass 
# class arSelSignal(Enum):
#     memSignal = 0x0
#     valueSignal = 0x1
#     addrSignal = 0x2
    
class RegisterFile():
    def __init__(self):
        self.regs  = []
        for i in range(16):
            self.regs.append(Register())
        self.addr : int = 0x0
        self.value : int = 0x0
    def write(self, 
              reg : int, 
              value: int):
        if(reg > 0xF) :
            return
        self.regs[reg] = value
    def read(self,
             reg : int):
        if(reg > 0xF) :
            return
        return self.regs[reg].value
    def sync(self):
        if(self.addr <= 0x8): 
            self.value = self.regs[self.addr].get()

@dataclass
class IOState(Enum):
    Lock = 0
    Unlock = 1

class InPort():
    def __init__(self, src = None):
        self.iter = 0
        with open(src , 'r') as file :
            self.ascii_code = [ord(char) for char in list(file.read())]

    def read(self) -> int:
        if self.iter >= len(self.ascii_code):
            return 0xd
        self.iter = self.iter + 1
        logging.debug('In: %s', chr(self.ascii_code[self.iter - 1]))
        return self.ascii_code[self.iter - 1]
    
class OutPort():
    def __init__(self, dest = None):
        self.dest = open(dest, 'w')
        self.isPrintingStr: bool = False
    def write(self, data):
        if self.isPrintingStr :
            if data == 47:
                self.dest.write('\n')
                logging.debug('Out: EOL')
            else:
                self.dest.write(chr(data))
                logging.debug('Out: %s', chr(data))
        else:
            self.dest.write(str(data))
            logging.debug('Out: %s', data)
    def close(self):
        self.dest.close()

class IOBuffer():
    def __init__(self):
        self.size = 500
        self.memory = []
        self.mappedTable : dict = {}
        self.crtReadElement = 0
        self.crtReadIter = 0
        self.crtWrite = 0
    def checkOverflow(self):
        if(len(self.memory) > self.size):
            raise OverflowError('Buffer overflow')
    def loadDataIn(self, data):
        self.memory.append(data)
        if data == 10:
            self.crtWrite = self.crtWrite + 1
            self.mappedTable[self.crtWrite] = len(self.memory)
        self.checkOverflow()
    def resetRead(self):
        self.crtReadElement = 0
        self.crtReadIter = 0
    def loadDataOut(self, element) -> int:
        self.crtReadElement = element
        self.crtReadIter = self.crtReadIter + 1
        crtAddr = self.mappedTable[element]
        return self.memory[crtAddr + self.crtReadIter - 1]
    def createInstance(self, inx):
        self.mappedTable[inx] = 0
    
class InterruptHandler():
    def __init__(self, 
                 inport : InPort, 
                 outPort: OutPort):
        self.state : IOState = IOState.Unlock
        self.value = 0x0
        self.inport = inport
        self.outport = outPort
    def lock(self):
        self.state = IOState.Lock
    def unlock(self):
        self.state = IOState.Unlock
    def checkUnlocked(self):
        if self.state == IOState.Lock:
            raise InterruptedError('Interrupt is not opened yet!')
    def getState(self):
        return self.state
    def toOut(self, data):
        if(self.state == IOState.Unlock):
            self.outport.write(data)
    def fromIn(self):
        if(self.state == IOState.Unlock):
            return self.inport.read()

#----------------------------CU components ----------------------------------#

''''
    class for classify type of instruction, group by number of params / althmetic instr
'''

class InstructionType(Enum):
    ZeroAttribute = 0x0
    OneAttribute = 0x1
    TwoAttribute = 0x2
    AlthmeticInstruction = 0x3

''''
    class to modify dataflow without execute unneccesary action
    for example: NOP : pc <- pc + 1
    instead of execute all step: fetch ar, fetch dr, alu execute, check write ,...
    datapath just simple select PC : 0x1 (pc + 1) -> update pc
'''
class datapathAction(Enum):
    activeSelDest = 0x0
    activeDestIndirectReg = 0x1
    activeArSel = 0x2
    activeSelSrc = 0x3
    activeSrcIndirectReg = 0x4
    activeIndirectAddr = 0x5
    activeAlthmetic = 0x6
    activeIn = 0x7
    activeDrSel = 0x8
    activeBufferRead = 0x9
    activeOut = 0xA
    activeLeftSel = 0xB
    activeRightSel = 0xC
    activeCmp = 0xD
    activeAC = 0xE
    activeWriteReg = 0xF
    activeWriteMem = 0x10
    activePcSel = 0x11

'''
special signal to control system, that is not datapath's work
'''
class SystemSignal(Enum):
    END_PROGRAM = 0x0
    DI = 0x1
    EI = 0x2
    STR = 0x3
    
class InstructionDecoder():
    def __init__(self):
        self.opcode : Opcode
        self.type : InstructionType
        self.mode_1 : Mode
        self.mode_2 : Mode
        self.dest : int
        self.src : int
    def decode(self, ir: Register):
        value = ir.get()
        self.opcode = Opcode.get(value >> 24 & 0xFF)
        if self.opcode.value in [ 0, 1, 6, 7, 25, 26, 29, 31]:
            self.type = InstructionType.ZeroAttribute
        elif self.opcode.value in [2, 3, 4, 5, 6, 7, 8, 9, 27, 28]:
            self.type = InstructionType.OneAttribute
        elif self.opcode.value in [10, 11, 19, 20, 21, 22, 23, 24]:
            self.type = InstructionType.TwoAttribute
        else:
            self.type = InstructionType.AlthmeticInstruction
        if self.opcode.value != 28:
            self.mode_1 = Mode.getMode(value >> 22 & 0x3)
            self.mode_2 = Mode.getMode(value >> 20 & 0x3)
            self.dest = value >> 16 & 0xF
            self.src = value & 0xFFFF
        else:
            self.mode_1 = Mode.getMode(value >> 22 & 0x3)
            self.mode_2 = OutMode.getMode(value >> 20 & 0x3)
            self.dest = value >> 16 & 0xF
            self.src = value & 0xFFFF

'''
    class to save data, which  is reused for instruction more-than-one machine word
'''
class NextInstructionPreparation():
    def __init__(self):
        self.nextIsData = False
        self.operator :AluOp
        self.destAddr : int
    def on(self):
        self.nextIsData = True
    def off(self):
        self.nextIsData = False
    def isOn(self):
        return self.nextIsData

'''
    time unit
'''
class TimingUnit():
    def __init__(self):
        self.tick = 0
    def inc(self):
        self.tick = self.tick + 1
    def getTick(self):
        return self.tick
'''
    classify, generate signal to datapath
    main function : generateSignal()
'''
class GenerateSignal():
    def __init__(self):
        self.nextSignal = NextInstructionPreparation()
    def generateSrcSignal(self, mode : Mode, src):
        if mode == Mode.DIRECT_REG:
            return {
                datapathAction.activeSelSrc : src,
                datapathAction.activeDrSel : 0x0
            }
        if mode == Mode.INDIRECT_REG:
            return {
                datapathAction.activeSelSrc : src,
                datapathAction.activeSrcIndirectReg : 0x1,
                datapathAction.activeDrSel : 0x1
            }
        if mode == Mode.ADDRESS:
            return {
                datapathAction.activeSelSrc : src,
                datapathAction.activeIndirectAddr : 0x1,
                datapathAction.activeDrSel : 0x1
            }
        if mode == Mode.VALUE:
            return {
                datapathAction.activeSelSrc: src,
                datapathAction.activeDrSel : 0x2
            }
    def generateDestSignal(self, mode: Mode, dest):
        if mode == Mode.DIRECT_REG:
            return {
                datapathAction.activeSelDest : dest,
                datapathAction.activeArSel : 0x2
            }
        if mode == Mode.INDIRECT_REG :
            return {
                datapathAction.activeSelDest : dest,
                datapathAction.activeDestIndirectReg : 0x1,
                datapathAction.activeArSel : 0x1
            }
    def generateWriteBackSignal(self, mode : Mode) :
        if mode == Mode.DIRECT_REG :
            return {
                datapathAction.activeWriteReg : 0x1
            }
        else :
            return {
                datapathAction.activeWriteMem : 0x1
            }
    def Opcode2AluOp(self,
                              op: Opcode):
        if op == Opcode.ADD:
            return AluOp.ADD
        if op == Opcode.SUB:
            return AluOp.SUB
        if op == Opcode.MUL:
            return AluOp.MUL
        if op == Opcode.DIV:
            return AluOp.DIV
        if op == Opcode.MOD:
            return AluOp.MOD
        if op == Opcode.AND:
            return AluOp.AND
        if op == Opcode.OR:
            return AluOp.OR
    def generateZeroType(self, 
                 op :Opcode ):
        if op == Opcode.RET :
            return {
                datapathAction.activeSelSrc : 0x3,
                datapathAction.activeDrSel: 0x0,
                datapathAction.activePcSel : 0x0,
            }
        if op == Opcode.NOP:
            return [{
                datapathAction.activePcSel : 0x1
            }]
        if op == Opcode.HALT:
            return [SystemSignal.END_PROGRAM]
        if op == Opcode.DI:
            return [SystemSignal.DI, {
                        datapathAction.activePcSel: 0x1
                    }]
        if op == Opcode.EI:
            return [SystemSignal.EI, {
                        datapathAction.activePcSel: 0x1
                    }]
        if op == Opcode.IN:
            return [{
                datapathAction.activeSelDest : 0x8,
                datapathAction.activeArSel : 0x2,
                datapathAction.activeIn: 0x1,
                datapathAction.activeDrSel : 0x3,
                datapathAction.activeLeftSel: 0x2,
                datapathAction.activeRightSel: 0x2,
                datapathAction.activeCmp: AluOp.OR,
                datapathAction.activeWriteReg: 0x1,
                datapathAction.activePcSel: 0x1
            }]
        if op == Opcode.OUT:
            return [{
                datapathAction.activeSelSrc : 0x8,
                datapathAction.activeDrSel: 0x0,
                datapathAction.activeOut: 0x1,
                datapathAction.activePcSel: 0x1
            }]
        if op == Opcode.STR:
            return [
                SystemSignal.STR, {
                datapathAction.activePcSel: 0x1
            }]
    def generateFirtsType(self, 
                              op : Opcode,
                              mode : Mode,
                              src, 
                              z : bool = False,
                              p : bool = False ):
        if op == Opcode.JMP:
            loaddata : dict = self.generateSrcSignal(mode, src)
            return [{
                **loaddata,
                datapathAction.activePcSel  : 0x0
            }]
        if op == Opcode.CALL:
            pass

        if op in  [Opcode.BGT, Opcode.BEQ]:
            if (p and op == Opcode.BGT) or (z and op == Opcode.BEQ) :
                return [{
                    datapathAction.activeSelSrc: src,
                    datapathAction.activeDrSel: 0x2,
                    datapathAction.activePcSel  : 0x0
                }]
            else :
                return [{
                    datapathAction.activePcSel : 0x1
                }]

        if op == Opcode.PUSH:
            loaddata : dict = self.generateSrcSignal(mode, src)
            return [
                {
                    datapathAction.activeSelDest: 0x4,
                    datapathAction.activeArSel: 0x1,
                    **loaddata,
                    datapathAction.activeLeftSel: 0x2,
                    datapathAction.activeRightSel: 0x2,
                    datapathAction.activeCmp: AluOp.OR,
                    datapathAction.activeWriteMem: 0x1

                },
                {
                    datapathAction.activeSelDest: 0x4,
                    datapathAction.activeArSel: 0x1,
                    datapathAction.activeLeftSel: 0x0,
                    datapathAction.activeRightSel: 0x1,
                    datapathAction.activeCmp: AluOp.SUB
                },
                {
                    datapathAction.activeSelDest: 0x4,
                    datapathAction.activeArSel: 0x2,
                    datapathAction.activeWriteReg: 0x1,
                    datapathAction.activePcSel: 0x1
                }
            ]

        if op == Opcode.POP:
            return [
                {
                    datapathAction.activeSelDest: src,
                    datapathAction.activeArSel: 0x2,
                    datapathAction.activeSelSrc: 0x4,
                    datapathAction.activeSrcIndirectReg: 0x1,
                    datapathAction.activeDrSel: 0x1,
                    datapathAction.activeLeftSel: 0x2,
                    datapathAction.activeRightSel: 0x2,
                    datapathAction.activeCmp: AluOp.OR,
                    datapathAction.activeWriteReg: 0x1
                },
                {
                    datapathAction.activeSelDest: 0x4,
                    datapathAction.activeArSel: 0x1,
                    datapathAction.activeLeftSel: 0x0,
                    datapathAction.activeRightSel: 0x1,
                    datapathAction.activeCmp: AluOp.ADD
                },
                {
                    datapathAction.activeSelDest: 0x4,
                    datapathAction.activeArSel: 0x2,
                    datapathAction.activeWriteReg: 0x1,
                    datapathAction.activePcSel: 0x1
                }
            ]
        
        if op == Opcode.INC:
            loadaddr : dict = self.generateDestSignal(mode, src)
            loadwrite : dict = self.generateWriteBackSignal(mode)
            return [{
                **loadaddr,
                datapathAction.activeArSel : 0x1 if mode == Mode.DIRECT_REG else 0x0,
                datapathAction.activeLeftSel: 0x0,
                datapathAction.activeRightSel : 0x1,
                datapathAction.activeAC : AluOp.ADD 
            },
            {
                **loadaddr,
                **loadwrite,
                datapathAction.activePcSel : 0x1
            }]
        
        if op == Opcode.NOT:
            loadaddr : dict = self.generateDestSignal(mode, src)
            loaddata : dict = self.generateSrcSignal(mode, src)
            loadwrite : dict = self.generateWriteBackSignal(mode)
            return [{
                **loadaddr,
                **loaddata,
                datapathAction.activeArSel : 0x2,
                datapathAction.activeLeftSel: 0x2,
                datapathAction.activeRightSel : 0x2,
                datapathAction.activeCmp : AluOp.ADD if op == Opcode.INC else AluOp.NOT,
                **loadwrite,
                datapathAction.activePcSel : 0x1
            }]
        
        if op == Opcode.RB:
            temp : dict = {
                    datapathAction.activeSelSrc: src,
                    datapathAction.activeSelDest: 0x8,
                    datapathAction.activeArSel: 0x2,
                    datapathAction.activeLeftSel: 0x2,
                    datapathAction.activeRightSel: 0x2,
                    datapathAction.activeCmp: AluOp.OR,
                    datapathAction.activeWriteReg: 0x1,
                    datapathAction.activePcSel: 0x1
            }
            if mode == OutMode.REG:
                return [ SystemSignal.STR ,{
                    datapathAction.activeDrSel: 0x0,
                    **temp
                }]
            if mode == OutMode.ADDRESS:
                return [SystemSignal.STR ,{
                    datapathAction.activeIndirectAddr: 0x1,
                    datapathAction.activeDrSel: 0x1,
                    **temp
                }]
            if mode == OutMode.BUF:
                return[SystemSignal.STR ,{
                    datapathAction.activeBufferRead: src,
                    **temp
                }]
    def generateSecondType(self, 
                           op : Opcode,
                           mode1 : Mode,
                           mode2 : Mode,
                           dest : int,
                           src : int):
        if op == Opcode.LOAD:
            loadaddr : dict = self.generateDestSignal(mode1, dest)
            loaddata : dict = self.generateSrcSignal(mode2, src)
            return [{
                **loadaddr,
                **loaddata,
                datapathAction.activeLeftSel : 0x2,
                datapathAction.activeRightSel : 0x2,
                datapathAction.activeCmp : AluOp.OR,
                datapathAction.activeWriteReg : 0x1,
                datapathAction.activePcSel : 0x1
            }]
        if op == Opcode.STORE:
            loaddata : dict = self.generateSrcSignal(mode1, dest)
            return [{
                datapathAction.activeSelDest : src,
                datapathAction.activeArSel: 0x2,
                **loaddata,
                datapathAction.activeLeftSel: 0x2,
                datapathAction.activeRightSel : 0x2,
                datapathAction.activeCmp: AluOp.OR,
                datapathAction.activeWriteMem: 0x1,
                datapathAction.activePcSel : 0x1
            }]
        if op == Opcode.CMP:
            
            loadaddr: dict = self.generateDestSignal(mode1, dest)
            loaddata : dict = self.generateSrcSignal(mode2, src)
            return [{
                **loadaddr,
                **loaddata,
                datapathAction.activeArSel: 0x1 if mode1 == Mode.DIRECT_REG else 0x0,
                datapathAction.activeLeftSel : 0x0,
                datapathAction.activeRightSel: 0x2,
                datapathAction.activeCmp : AluOp.SUB,
                datapathAction.activePcSel: 0x1
            }]
        if op == Opcode.MOV:
            loadaddr: dict = self.generateDestSignal(mode1, dest)
            loaddata : dict = self.generateSrcSignal(mode2, src)
            loadwrite : dict = self.generateWriteBackSignal(mode1)
            return [{
                **loadaddr,
                **loaddata,
                datapathAction.activeLeftSel: 0x2,
                datapathAction.activeRightSel : 0x2,
                datapathAction.activeCmp : AluOp.OR,
                **loadwrite,
                datapathAction.activePcSel : 0x1 
            }]
        if op in [Opcode.LSL, Opcode.LSR]:
            loadaddr: dict = self.generateDestSignal(mode1, dest)
            loaddata : dict = self.generateSrcSignal(mode2, src)
            return [
                {
                    **loadaddr,
                    **loaddata,
                    datapathAction.activeArSel: 0x1,
                    datapathAction.activeLeftSel: 0x0,
                    datapathAction.activeRightSel: 0x2,
                    datapathAction.activeAC: AluOp.LSL if op == Opcode.LSL else AluOp.LSR
                 },
                 {
                     **loadaddr,
                     datapathAction.activeArSel: 0x2,
                     datapathAction.activeWriteReg : 0x1,
                     datapathAction.activePcSel: 0x1
                 }
            ]
    def generateAlthmeticType(self, 
                              op : Opcode,
                              mode1 : Mode,
                              mode2 : Mode,
                              dest, 
                              src) :
        operator = self.Opcode2AluOp(op)
        if mode2 != Mode.VALUE:
            loadaddr: dict = self.generateDestSignal(mode1, dest)
            loaddata : dict = self.generateSrcSignal(mode2, src)
            return [
                {
                    **loadaddr,
                    **loaddata,
                    datapathAction.activeArSel: 0x1,
                    datapathAction.activeLeftSel: 0x0,
                    datapathAction.activeRightSel: 0x2,
                    datapathAction.activeAC: operator
                    },
                    {
                        datapathAction.activeArSel: 0x2,
                        datapathAction.activeWriteReg : 0x1,
                        datapathAction.activePcSel: 0x1
                    }
            ]
        else:
            self.nextSignal.on()
            self.nextSignal.operator = operator
            self.nextSignal.destAddr = dest
            loadaddr: dict = self.generateDestSignal(mode1, dest)
            return [{
                **loadaddr,
                datapathAction.activeArSel : 0x1,
                datapathAction.activePcSel: 0x1
            }]
    def DataInstruction(self):
        return [
            {
                datapathAction.activeAlthmetic: 0x1,
                datapathAction.activeDrSel: 0x2,
                datapathAction.activeLeftSel: 0x0,
                datapathAction.activeRightSel: 0x2,
                datapathAction.activeAC: self.nextSignal.operator
             },
            {
                datapathAction.activeArSel: 0x2,
                datapathAction.activeWriteReg : 0x1,
                datapathAction.activePcSel: 0x1
            }
        ]
    
    def generateSignal(self, 
                       type : InstructionType,
                       op: Opcode,
                       mode1: Mode = None,
                       dest : int = 0,
                       z: bool = False,
                       p : bool = False,
                       mode2 : Mode = None,
                       src : int = 0
                       ):
        if self.nextSignal.isOn():
            self.nextSignal.off()
            return self.DataInstruction()
        else:
            if type == InstructionType.ZeroAttribute:
                return self.generateZeroType(op)
            if type == InstructionType.OneAttribute:
                return self.generateFirtsType(op, mode2, src, z, p)
            if type == InstructionType.TwoAttribute:
                return self.generateSecondType(op, mode1, mode2, dest, src)
            if type == InstructionType.AlthmeticInstruction:
                return self.generateAlthmeticType(op, mode1, mode2,dest, src )
        return []



        


