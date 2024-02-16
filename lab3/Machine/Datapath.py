from Machine.Components import (
    Register, Memory, 
    RegisterFile, Mux, 
    ALU, InterruptHandler, 
    IOBuffer, InPort, OutPort,
    GeneralRegister, AluOp,
    pcSelSignal, drSelSignal,
    leftSignal, rightSignal,
    IOState
)

from dataclasses import dataclass
from enum import Enum

@dataclass
class branchInstruction(Enum):
    BEQ = 4
    BGT = 5
    JMP = 2
    CALL = 3
    RET = 1
class Datapath():
    def __init__(self):
        self.memory = Memory(),

        self.registers.pc = Register(),
        self.registers.ir = Register(),
        self.registers.ar = Register(),
        self.registers.ac = Register(),
        self.registers.dr = Register(),

        self.muxs.pcMux = Mux(),
        self.muxs.drMux = Mux(),
        self.muxs.leftMux = Mux(),
        self.muxs.rightMux = Mux(),

        self.registerFile = RegisterFile()
        self.ALU = ALU()

        self.io.interruptHandler = InterruptHandler(),
        self.io.buffer = IOBuffer(),
        self.io.inPort = InPort(),
        self.io.outPort = OutPort()

        self.state.selReg = GeneralRegister.rax
        self.state.isReg = False,
        self.state.isAddr = False,
        self.state.isVal = False,
        self.state.isBranch = False,
        self.state.isWriteReg = False,
        self.state.input = False,
        self.state.output = False,

        self.select.PCsel = pcSelSignal.plusOne 
        self.select.DRsel = drSelSignal.acSignal 
        self.select.leftsel = leftSignal.zero
        self.select.rightsel = rightSignal.zero 
        self.select.althmetic = AluOp.ADD

    def setup(self):
        self.registers.pc.set(0x0)
        self.muxs.pcMux.setCOnn([0x0, 0x0])
        self.muxs.drMux.setConn([0x0, 0x0, 0x0, 0x0])
        self.muxs.leftMux.setConn([0x0, 0x0, 0x0])
        self.muxs.rightMux.setConn([0x0, 0x0])
        
    def latchIR(self):
        self.registers.ir.set(self.memory.read(self.registers.pc.get()))
        self.state.selReg = self.ir.get_byte_at(4)
    
    def latchAR(self):
        if(self.state.isAddr):
            content = self.registerFile[self.selReg].get()
            self.registers.ar.set(content)
        else:
            self.registers.ar.set(self.state.selReg)

    def updateDrMux(self):
        if(self.state.isReg):
            reg = self.registers.ir.get() & 0xF
            self.muxs.drMux.conn[1] = self.registerFile.regs[reg].get()
        self.muxs.drMux.conn[0] = self.registers.ac.get()
        if(self.state.isVal) :
            self.muxs.drMux.conn[2] = self.registers.ir.get() & 0xFFFF
        if(self.io.InterruptHandler.state == IOState.Unlock
           and self.state.input):
            self.muxs.drMux.conn[3] = self.io.interruptHandler.value
            self.io.interruptHandler.getNextValue(self.io.buffer)
        
    
    def latchDR(self):
        self.registers.dr.set(self.muxs.drMux.conn[self.select.DRsel])
        if(self.io.interruptHandler.state == IOState.Unlock
           and self.state.output):
            self.io.interruptHandler.value = self.registers.dr.get()
            self.io.interruptHandler.writeToBuffer(self.io.buffer)
    
    def updatePcMux(self):
        if(self.state.isBranch):
            self.muxs.pcMux.conn[0] = self.regiters.dr.get()
        self.muxs.pcMux.conn[1] = self.registers.pc.get() + 1
    
    def pcLatch(self):
        self.register.pc.set(self.muxs.pcMux.conn[self.select.pcSel])
    
    def updateLeftMux(self):
        self.muxs.leftMux.conn[0] = self.registers.ar.get()
        self.muxs.leftMux.conn[1] = self.registers.ac.get()
        self.muxs.leftMux.conn[2] = 0x0
    
    def updateRightMux(self):
        self.muxs.rightMux.conn[0] = 0x0
        self.muxs.rightMux.conn[1] = self.registers.dr.get()
    
    def updateAlu(self):
        self.registers.ac.set(self.ALU.execute(self.select.althmetic,
                                               self.muxs.leftMux.conn[self.select.leftSel],
                                               self.muxs.rightMux.conn[self.select.rightSel]))
        self.registerFile.regs[0].set(self.registers.ac.get())
        if(self.state.isWriteReg):
            self.registerFile.regs[self.registers.ar.get()].set(self.registers.ac.get())


    
