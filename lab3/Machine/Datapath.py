from Components import (
    Register, Memory, 
    RegisterFile, Mux, 
    ALU, InterruptHandler, 
    IOBuffer, InPort, OutPort
)

from dataclasses import dataclass
from enum import Enum

@dataclass
class branchInstruction(Enum):
    BEQ = 4
    BGT = 5
    JMP = 2
    CALL = 3
class Datapath():
    def __init__(self):
        self.pc = Register()
        self.memory = Memory()
        self.ir = Register()
        self.registerFile = RegisterFile()
        self.pcMux = Mux()
        self.ar = Register()
        self.ac = Register()
        self.drMux = Mux()
        self.ac = Register()
        self.dr = Register()
        self.leftMux = Mux()
        self.rightMux = Mux()
        self.ALU = ALU()
        self.interruptHandler = InterruptHandler()
        self.buffer = IOBuffer()
        self.inPort = InPort()
        self.outPort = OutPort()
    def setup(self):
        self.pc.set(0x0)
        self.drMux.setConn([0x0, 0x0, 0x0, 0x0])
        self.leftMux.setConn([0x0, 0x0, 0x0])
        self.rightMux.setConn([0x0, 0x0])
    def latchIR(self):
        self.ir.set(self.memory[self.pc.get()])
        regWithIR = self.registerFile[self.ir.get_byte_at(4)]
        self.drMux.conn[1] = regWithIR
    
