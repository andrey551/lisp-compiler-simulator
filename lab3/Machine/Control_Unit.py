from lab3.Machine.Components import GenerateSignal, InstructionDecoder, SystemSignal, TimingUnit
from lab3.Machine.Datapath import Datapath



class CU:
    def __init__(self):
        self.decoder = InstructionDecoder()
        self.tu = TimingUnit()
        self.generate = GenerateSignal()
        self.datapath = Datapath()
    def setup(self, input, output, src):
        self.datapath.setup(input, output, src)
        self.datapath.pc.set(self.datapath.memory.data[0])
    def fetch(self):
        self.datapath.ir.set(self.datapath.memory.data[self.datapath.pc.get()])
        self.decoder.decode(self.datapath.ir)
        
    '''
    fetch IR(CU) -> generate signal(CU) -> execute(Datapath) -> writeback(datapath)
    '''
    def run(self):
        while(1):
            self.fetch()
            signals = self.generate.generateSignal(self.decoder.type,
                                         self.decoder.opcode,
                                         self.decoder.mode_1,
                                         self.decoder.dest,
                                         self.datapath.ALU.z,
                                         self.datapath.ALU.p,
                                         self.decoder.mode_2,
                                         self.decoder.src
                                         )
            if isinstance(signals[0], SystemSignal):
                if signals[0] == SystemSignal.END_PROGRAM:
                    break
                if signals[0] == SystemSignal.DI:
                    self.datapath.interruptHandler.unlock()
                    
                if signals[0] == SystemSignal.EI:
                    self.datapath.interruptHandler.lock()
                    self.datapath.interruptHandler.outport.isPrintingStr = False
                    self.datapath.buffer.resetRead()

                if signals[0] == SystemSignal.STR:
                    self.datapath.interruptHandler.outport.isPrintingStr = True
                
                self.datapath.runCycle(signals[1])
                self.tu.inc()
            else:
                for i in signals:
                    self.datapath.runCycle(i)
                    self.tu.inc()
            self.datapath.getLog(self.tu.getTick())
