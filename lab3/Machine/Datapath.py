from lab3.Machine.Components import (
    Register, Memory, 
    RegisterFile, Mux, 
    ALU, InterruptHandler, 
    IOBuffer, InPort, OutPort,
    datapathAction, AluOp
)
import logging
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
        self.memory = Memory()

        self.pc = Register()
        self.ir = Register()
        self.ar = Register()
        self.ac = Register()
        self.dr = Register()

        self.pcMux = Mux()
        self.drMux = Mux()
        self.arMux = Mux()
        self.leftMux = Mux()
        self.rightMux = Mux()

        self.registerFile = RegisterFile()
        self.ALU = ALU()

        self.interruptHandler = None
        self.buffer = IOBuffer()

        self.selDest = 0x0
        self.selSrc = 0x0
        self.PCsel = 0x0
        self.ARsel = 0x0
        self.DRsel = 0x0
        self.leftSel = 0x0
        self.rightSel = 0x0
        self.althmeticSignal = 0x0


    def setup(self, input, output, src):
        inport = InPort(input)
        outport = OutPort(output)
        self.interruptHandler = InterruptHandler(inport, outport)

        self.pcMux.setConn([0x0, 0x0])
        self.drMux.setConn([0x0, 0x0, 0x0, 0x0])
        self.arMux.setConn([0x0, 0x0, 0x0])
        self.leftMux.setConn([0x0, 0x0, 0x0])
        self.rightMux.setConn([0x0, 0x1, 0x0])
        self.registerFile.regs[0x4].set(self.memory.length)
        self.memory.load(src)
    def getLog(self, tick):
        getBuffer = str(len(self.buffer.memory))
        getAc = self.ac.get()
        getAr = self.ar.get()
        getDr = self.dr.get()
        getPc = self.pc.get() - 1
        getRax = self.registerFile.regs[0].get()
        getRcx = self.registerFile.regs[1].get()
        getRdx = self.registerFile.regs[2].get()
        getRbx = self.registerFile.regs[3].get()
        getRsp = self.registerFile.regs[4].get()
        getSbp = self.registerFile.regs[5].get()
        getRsi = self.registerFile.regs[6].get()
        getRdi = self.registerFile.regs[7].get()
        getRio= self.registerFile.regs[8].get()
        getInt = self.interruptHandler.getState()
        getP = self.ALU.p
        getz = self.ALU.z
        a = ' tick: %5s, AC: %8s, AR: %8s, DR: %8s, PC: %8s, rax: %8s, rcx: %8s,'
        b = ' rdx: %8s, rbx: %8s, rsp: %8s, sbp: %8s, rsi: %8s, rdi: %8s, rio: %8s,'
        format = a + b + '  interrupt: %8s, buffer: %8s, p : %5s, z: %5s'
        logging.debug(format, tick, getAc, getAr, getDr, hex(getPc),  
                      getRax, getRcx, getRdx, getRbx, getRsp, 
                      getSbp, getRsi, getRdi, getRio, 
                      getInt, getBuffer, getP, getz)
    
    def activeSelDest(self, value):
        self.selDest = value
        self.registerFile.addr = value
        self.registerFile.sync()
    # this is must be executed action:
    # self.arMux.conn[1] = self.registerFile.addr
    # self.arMux.conn[2] = self.registerFile.value
    
    def activeDestIndirectReg(self):
        self.arMux.conn[0] = self.memory.read(self.registerFile.value)

    def activeArSel(self, value):
        self.ARsel = value
        self.ar.set(self.arMux.conn[value])
        self.leftMux.conn[0] = self.ar.get()
    
    def activeSelSrc(self, value):
        self.selSrc = value
        self.registerFile.addr = value
        self.registerFile.sync()
        self.drMux.conn[0] = self.registerFile.value

    def activeSrcIndirectReg(self):
        self.drMux.conn[1] = self.memory.read(self.registerFile.value)

    def activeIndirectAddr(self):
        self.drMux.conn[1] = self.memory.read(self.registerFile.addr)
    
    # this is must-be execute action
    # update drMux[2] = self.ir & 0xFFFF
    def activeAlthmetic(self):
        self.drMux.conn[2] = self.ir.get()
    
    def activeIn(self):
        self.drMux.conn[3] = self.interruptHandler.fromIn()
        self.buffer.loadDataIn(self.drMux.conn[3])
    
    def activeDrSel(self, value):
        self.DRsel = value
        self.dr.set(self.drMux.conn[value])

    def activeBufferRead(self, value):
        self.dr.set(self.buffer.loadDataOut(value))
        self.rightMux.conn[2] = self.dr.get()

    def activeOut(self):
        self.interruptHandler.toOut(self.dr.get())
    
    def activeLeftSel(self, value):
        self.leftSel = value
        self.ALU.left = self.leftMux.conn[value]
    
    def activeRightSel(self, value):
        self.rightSel = value
        self.ALU.right = self.rightMux.conn[value]

    def activeCmp(self, operatorSignal : AluOp):
        self.ac.set(self.ALU.execute(operatorSignal))

    def activeAC(self, operatorSignal : AluOp):
        temp = self.ALU.execute(operatorSignal)
        self.ac.set(temp)
        self.registerFile.regs[0].set(self.ac.get())
    
    def activeWriteReg(self):
        self.registerFile.regs[self.ar.get()].set(self.ac.get())
    
    def activeWriteMem(self):
        self.memory.write(self.ar.get(), self.ac.get())

    def activePcSel(self, value):
        self.pcMux.conn[1] = self.pc.get() + 1
        self.pc.set(self.pcMux.conn[value])

    def runCycle(self, signal : dict):
        if datapathAction.activeSelDest in signal :
            self.activeSelDest(signal[datapathAction.activeSelDest])

        self.arMux.conn[2] = self.registerFile.addr
        self.arMux.conn[1] = self.registerFile.value

        if datapathAction.activeDestIndirectReg in signal :
            self.activeDestIndirectReg()

        if datapathAction.activeArSel in signal :
            self.activeArSel(signal[datapathAction.activeArSel])

        if datapathAction.activeSelSrc in signal :
            self.activeSelSrc(signal[datapathAction.activeSelSrc])

        if datapathAction.activeIndirectAddr in signal :
            self.activeIndirectAddr()
        if datapathAction.activeSrcIndirectReg in signal :
            self.activeSrcIndirectReg()
        self.drMux.conn[2] = self.ir.get() & 0xFFFF

        if datapathAction.activeAlthmetic in signal :
            self.activeAlthmetic()

        if datapathAction.activeIn in signal :
            self.activeIn()

        if datapathAction.activeDrSel in signal :
            self.activeDrSel(signal[datapathAction.activeDrSel])
            self.rightMux.conn[2] = self.dr.get()
        
        if datapathAction.activeBufferRead in signal:
            self.activeBufferRead(signal[datapathAction.activeBufferRead])

        if datapathAction.activeLeftSel in signal :
            self.activeLeftSel(signal[datapathAction.activeLeftSel])

        if datapathAction.activeOut in signal :
            self.activeOut()

        if datapathAction.activeRightSel in signal :
            self.activeRightSel(signal[datapathAction.activeRightSel])

        if datapathAction.activeCmp in signal :
            self.activeCmp(signal[datapathAction.activeCmp])

        if datapathAction.activeAC in signal :
            self.activeAC(signal[datapathAction.activeAC])

        if datapathAction.activeWriteReg in signal :
            self.activeWriteReg()

        if datapathAction.activeWriteMem in signal :
            self.activeWriteMem()
        
        self.pcMux.conn[0] = self.dr.get()

        if datapathAction.activePcSel in signal :
            self.activePcSel(signal[datapathAction.activePcSel])
    


    
