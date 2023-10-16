import time

class PrivateBlock:
    def __init__(self, id, blockSize, prevHash, patientId, doctorId, hashEMR, signature):
        # Block header
        self.id = id
        self.blockSize = blockSize
        self.prevHash = prevHash

        # Payload
        self.patientId = patientId
        self.doctorId = doctorId
        self.hashEMR = hashEMR

        self.signature = signature
        self.timestamp = time.time()


class ConsortiumBlock:
    def __init__(self,id,blockSize,prevHash, generatorId, secureSearchIndex,signature) :
        self.id = id
        self.blockSize = blockSize
        self.prevHash = prevHash

        # Payload
        self.generatorId = generatorId
        self.secureSearchIndex = secureSearchIndex

        self.signature = signature
        self.timestamp = time.time()