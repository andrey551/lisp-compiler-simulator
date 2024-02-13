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
        return self.value >> index & 0xF

class Flag():
    def __init__(self):
        self.value = False
    def set(self, val) :
        self.value = val
    def get(self):
        return self.value

class Mux():
    pass

class Memory():
    def __init__(self):
        self.data = []
        self.length = 65536
    def read(self, address: int):
        return self.data[address]
    def write(self, address, value):
        self.data[address] = value


