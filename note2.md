from AST tree, how to convert it to HEX code ?
address : 16 bit
Address Mode: 
    00 : register(4 bit)
    01 : value on register(4 bit)
    10 : address(16 bit)
    11 : value(16 bit)
-> It's necessary to build instruction command set and it's represented in 1 machine word
there are 26 instruction, so it should be stored in 5 bits 

I : Mode(2bit)

# rax : 0x0
# rbx : 0x3
# rcx: 0x1
# rdx: 0x2
# rsp: 0x4
# sbp: 0x5 : begin of stack( end of memory) 
# rsi: 0x6
# rdi: 0x7
# r8: IO reg

1. 0-addressing instruction
    1.1 RET(00001) transfers the contents of rbx(address that program counter lies on) to the PC(program counter). 
    1.2 NOP(00000) do nothing
    1.3 HALT(11111) end program 
    1.4 DI(11001) start interrupt
    1.5 EI(11010) end interrupt
    1.6 IN(00110) - interrupt in
    1.7 OUT(00111) - interrupt out
    instruction format: [opcode(5)]
    
2. 1-addressing instruction
    2.1 JMP(00010) - jump to specific address
    2.2 CALL(00011) - instructions takes a single argument – the label of the first instruction of the function. 
    It transfers control to the label and saves the return address in register 
    2.3 BEQ(00100) - branch if equal(Z = 0)
    2.4 BGT(00101) - branch if greater than()
    2.5 PUSH(01000)
    2.6 POP (01001)
    2.7 INC (11011)
    2.8 NOT(11000)
    2.9 RB(11100)
    instruction format: [opcode(5)][I(2)][value] ( length change)
    
3. 2-addressing instruction
    3.1 LOAD(01010) - loads values from memory into registers
    3.2 STORE(01011) -  saves values in registers to memory locations
    instruction format: [opcode(5)][I-1(1)][reg_dest(4)][reg-source(4)][immediate(18)]
    3.3 CMP(10110)
        instruction format: [opcode(5)][I -1(1)][(4)][reg-source-1(4)][reg-source-2/immediate(18)]
    
    3.4 MOV(10111) - transfer values from one register to another, or can load a register with a constant
    mov from to
        instruction format: [opcode(5)][I - 1(1)][reg-dest(4)][(4)][reg-source(4)/immediate(18)]
    3.6 LSL(10011) - shifts the value in the first source register to the left
    3.7 LSR(10100) - shifts the value in the first source register to the right.
4. althmetic instruction
    4.1 ADD(01100)
    4.2 SUB(01101) 
    4.3 MUL(01110)
    4.4 DIV(01111)
    4.5 MOD(10000)
    4.6 AND(10001)
    4.7 OR(10010)
    instruction format:
        [opcode(5)][I(2)][I(2)][I(2)][value][value][value] (length change)