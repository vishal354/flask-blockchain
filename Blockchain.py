from Block import Block

class Blockchain:
    def __init__(self):
        self.blockSize = 10
        self.chain = []
        self.doctors = []
        self.patients = []
        self.chain.append(self.createGenesisBlock())
    
    def createGenesisBlock(self):
        return Block(0, self.blockSize, "0", "0", "0", "0", "0")