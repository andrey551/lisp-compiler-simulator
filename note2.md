from AST tree, how to convert it to HEX code ?

-> It's necessary to build instruction command set and it's represented in 1 machine word
there are 21 instruction, so it should be stored in 5 bits 
1. 0-addressing instruction
    1.1 RET(10100) transfers the contents of ra(address that program counter lies on) to the PC(program counter). 
    1.2 NOP(01110) do nothing
    instruction format: [opcode(5)][(27)]
    
2. 1-addressing instruction
    2.1 JMP(10010) - jump to specific address
    2.2 CALL(10011) - instructions takes a single argument – the label of the first instruction of the function. 
    It transfers control to the label and saves the return address in register 
    2.3 BEQ(10000) - branch if equal(Z = 0)
    2.4 BGT(10001) - branch if greater than()
    because 5 bits store opcode, so we can't store direct address, so we will store the address by it off set from PC
    instruction format: [opcode(5)][offset(27)]
3. 2-addressing instruction
    3.1 LOAD(01110) - loads values from memory into registers
    3.2 STORE(01111) -  saves values in registers to memory locations
    instruction format: [opcode(5)][I-1(1)][reg_dest(4)][reg-source(4)][immediate(18)]
4. 3-addressing instruction
    4.1 ADD(00000)
    4.2 SUB(00001) 
    4.3 MUL(00010)
    4.4 DIV(00011)
    4.5 MOD(00100)
    4.6 AND(00110)
    4.7 OR(00111)
    4.8 LSL(01010) - shifts the value in the first source register to the left
    4.9 LSR(01011) - shifts the value in the first source register to the right.
    4.10 ASR(01100) - performs an arithmetic right shift

    instruction format:
        register mode: [opcode(5)][I - 0(1)][reg-dest(4)][reg-source-1(4)][reg-source-2(4)]
        immediate mode: [opcode(5)][I -1(1)][reg-dest(4)][reg-source(4)][immediate(18)]
5. two source operands
    5.1 CMP(00101)
        instruction format: [opcode(5)][I -1(1)][(4)][reg-source-1(4)][reg-source-2/immediate(18)]
    
    5.2 MOV(01001) - transfer values from one register to another, or can load a register with a constant
        instruction format: [opcode(5)][I -1(1)][reg-dest(4)][(4)][reg-source-2/immediate(18)]
    
    5.3 NOT(01000)
        instruction format: [opcode(5)][I -1(1)][reg-dest(4)][(4)][reg-source-2/immediate(18)]