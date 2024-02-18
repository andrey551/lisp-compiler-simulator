from Machine.Components import (
    Register, Memory, 
    RegisterFile, Mux, 
    ALU, InterruptHandler, 
    IOBuffer, InPort, OutPort,
    datapathAction, AluOp,
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

        self.interruptHandler = InterruptHandler()

        # self.state.isAlthmetic = False,
        # self.state.isDestIndirectReg = False,
        # self.state.isSrcIndirectReg = False,
        # self.state.isWriteMem = False,
        # self.state.isWriteReg = False,
        # self.state.isCmp = False

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
        buffer = IOBuffer(inport, outport)
        self.io.interruptHandler = InterruptHandler(buffer)

        self.pcMux.setConn([0x0, 0x0])
        self.drMux.setConn([0x0, 0x0, 0x0, 0x0])
        self.arMux.setConn([0x0, 0x0, 0x0])
        self.leftMux.setConn([0x0, 0x0, 0x0])
        self.rightMux.setConn([0x0, 0x0, 0x0])
        self.memory.load(src)
    
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
        self.ar.set(self.arMux.conn[self.ARsel])
    
    def activeSelSrc(self, value):
        self.selSrc = value
        self.registerFile.addr = value
        self.registerFile.sync()
        self.drMux.conn[0] = self.registerFile.value

    def activeIndirectAddr(self):
        self.drMux.conn[1] = self.memory.read(self.registerFile.value)
    
    # this is must-be execute action
    # update drMux[2] = self.ir & 0xFFFF
    def activeAlthmetic(self):
        self.drMux.conn[2] = self.ir.get()
    
    def activeIn(self):
        self.drMux.conn[3] = self.interruptHandler.getValue()
    
    def activeDrSel(self, value):
        self.DRsel = value
        self.dr.set(self.drMux.conn[value])
        
    
    def activeLeftSel(self, value):
        self.leftSel = value
        self.ALU.left = self.leftMux.conn[value]
    
    def activeRightSel(self, value):
        self.rightSel = value
        self.ALU.right = self.rightMux.conn[value]

    def activeCmp(self, operatorSignal : AluOp):
        self.ALU.execute(operatorSignal)

    def activeAC(self, operatorSignal : AluOp):
        self.ac.set(self.ALU.execute(operatorSignal))
        self.registerFile.regs[0].set(self.ac.get())
    
    def activeWriteReg(self):
        self.registerFile.regs[self.ar.get()].set(self.ac.get())
    
    def activeWriteMem(self):
        self.memory.write(self.ar.get(), self.ac.get())
    # this is must-be execute action
    # self.pcMux.conn[0] = self.dr.get()
    def activePcSel(self, value):
        self.pcMux.conn[1] = self.pc.get() + 1
        self.pc.set(self.pcMux.conn[value])

    def runCycle(self, signal : dict):
        if datapathAction.activeSelDest in signal :
            self.activeSelDest(signal[datapathAction.activeSelDest])

        self.arMux.conn[1] = self.registerFile.addr
        self.arMux.conn[2] = self.registerFile.value

        if datapathAction.activeDestIndirectReg in signal :
            self.activeDestIndirectReg()

        if datapathAction.activeArSel in signal :
            self.activeArSel(signal[datapathAction.activeArSel])

        if datapathAction.activeSelSrc in signal :
            self.activeSelSrc(signal[datapathAction.activeSelSrc])

        if datapathAction.activeIndirectAddr in signal :
            self.activeIndirectAddr()

        self.drMux.conn[2] = self.ir & 0xFFFF

        if datapathAction.activeAlthmetic in signal :
            self.activeAlthmetic()

        if datapathAction.activeIn in signal :
            self.activeIn()

        if datapathAction.activeDrSel in signal :
            self.activeDrSel(signal[datapathAction.activeDrSel])

        if datapathAction.activeLeftSel in signal :
            self.activeLeftSel(signal[datapathAction.activeLeftSel])

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
    

    # def latchIR(self):
    #     self.register.ir.set(self.memory.read(self.register.pc.get()))
    
    # def updateARMux(self):
    #     self.registerFile.addr = self.select.selDest
    #     self.registerFile.sync()
    #     self.mux.arMux.conn[1] = self.registerFile.addr
    #     self.mux.arMux.conn[2] = self.registerFile.value
    #     if(self.state.isDestIndirectReg):
    #         self.mux.arMux.conn[0] = self.memory.read(self.registerFile.value)
    
    # def latchAR(self):
    #     self.register.ar.set(self.mux.arMux.conn[self.select.ARsel])

    # def updateDRMux(self):
    #     if self.state.isAlthmetic :
    #         self.mux.drMux.conn[2] = self.register.ir.get()
    #     else:
    #         self.mux.drMux.conn[2] = self.register.ir.get() & 0xFFFF
    #     self.mux.drMux.conn[3] = self.interruptHandler.getValue()
    #     self.registerFile.addr = self.select.selSrc
    #     self.registerFile.sync()
    #     self.mux.drMux.conn[0] = self.registerFile.value
    #     if self.state.isSrcIndirectReg :
    #         self.mux.drMux.conn[1] = self.memory.read(self.registerFile.value)
    
    # def latchDR(self):
    #     self.register.dr.set(self.mux.drMux.conn[self.select.DRsel])
    
    # def updateLeftMux(self):
    #     self.mux.leftMux.conn[0] = self.register.ar.get()
    #     self.mux.leftMux.conn[1] = self.register.ac.get()
    #     self.mux.leftMux.conn[2] = 0x0
    
    # def updateRightMux(self):
    #     self.mux.rightMux.conn[0] = 0x0
    #     self.mux.rightMux.conn[1] = 0x1
    #     self.mux.rightMux.conn[2] = self.register.dr.get()
    
    # def latchAC(self):
    #     ret = self.ALU.execute(self.select.althmeticSignal,
    #                            self.mux.leftMux.conn[self.select.leftSel],
    #                            self.mux.rightMux.conn[self.select.rightSel])
    #     if self.state.isCmp:
    #         self.register.ac.set(ret)
    #         self.registerFile.regs[0x0].set(self.register.ac.get())
    #         if self.state.isWriteReg:
    #             self.registerFile.regs[self.register.ar.get].set(self.register.ac.get())
    #         if self.state.isWriteMem:
    #             self.memory.data[self.register.ar] = self.register.ac.get()
    
    # def updatePCMux(self):
    #     self.mux.pcMux.conn[0] = self.register.dr.get()
    #     self.mux.pcMux.conn[1] = self.register.pc + 1
    
    # def latchPC(self):
    #     self.register.pc.set(self.mux.pcMux.conn[self.select.PCsel])


        
    # def latchIR(self):
    #     self.registers.ir.set(self.memory.read(self.registers.pc.get()))
    #     self.state.selReg = self.ir.get_byte_at(4)
    
    # def latchAR(self):
    #     if(self.state.isAddr):
    #         content = self.registerFile[self.selReg].get()
    #         self.registers.ar.set(content)
    #     else:
    #         self.registers.ar.set(self.state.selReg)

    # def updateDrMux(self):
    #     if(self.state.isReg):
    #         reg = self.registers.ir.get() & 0xF
    #         self.muxs.drMux.conn[1] = self.registerFile.regs[reg].get()
    #     self.muxs.drMux.conn[0] = self.registers.ac.get()
    #     if(self.state.isVal) :
    #         self.muxs.drMux.conn[2] = self.registers.ir.get() & 0xFFFF
    #     if(self.io.InterruptHandler.state == IOState.Unlock
    #        and self.state.input):
    #         self.muxs.drMux.conn[3] = self.io.interruptHandler.value
    #         self.io.interruptHandler.getNextValue(self.io.buffer)
        
    
    # def latchDR(self):
    #     self.registers.dr.set(self.muxs.drMux.conn[self.select.DRsel])
    #     if(self.io.interruptHandler.state == IOState.Unlock
    #        and self.state.output):
    #         self.io.interruptHandler.value = self.registers.dr.get()
    #         self.io.interruptHandler.writeToBuffer(self.io.buffer)
    
    # def updatePcMux(self):
    #     if(self.state.isBranch):
    #         self.muxs.pcMux.conn[0] = self.regiters.dr.get()
    #     self.muxs.pcMux.conn[1] = self.registers.pc.get() + 1
    
    # def pcLatch(self):
    #     self.register.pc.set(self.muxs.pcMux.conn[self.select.pcSel])
    
    # def updateLeftMux(self):
    #     self.muxs.leftMux.conn[0] = self.registers.ar.get()
    #     self.muxs.leftMux.conn[1] = self.registers.ac.get()
    #     self.muxs.leftMux.conn[2] = 0x0
    
    # def updateRightMux(self):
    #     self.muxs.rightMux.conn[0] = 0x0
    #     self.muxs.rightMux.conn[1] = self.registers.dr.get()
    
    # def updateAlu(self):
    #     self.registers.ac.set(self.ALU.execute(self.select.althmetic,
    #                                            self.muxs.leftMux.conn[self.select.leftSel],
    #                                            self.muxs.rightMux.conn[self.select.rightSel]))
    #     self.registerFile.regs[0].set(self.registers.ac.get())
    #     if(self.state.isWriteReg):
    #         self.registerFile.regs[self.registers.ar.get()].set(self.registers.ac.get())


    
