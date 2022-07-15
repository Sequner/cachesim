from configs import *
from memorycontroller import MemoryController
from traffic_gen import *
import random

class Cache:
    def __init__(self, size, policy):
        self.policy = policy
        self.size = size
        self.entries = [-1 for _ in range(size)]
        self.mapping = {}
        self.evictionCounter = [0 for _ in range(size)]
        self.addrActCounter = {}
        if self.policy == 'FIFO':
            self.fifoPointer = 0

    def processRequest(self, addr):
        if not addr in self.mapping:
            self.processMiss(addr)
    
    def processMiss(self, addr):
        if len(self.mapping) != self.size: # if cache is not full
            self.entries[len(self.mapping)] = addr
            self.mapping[addr] = len(self.mapping)
        else:
            if self.policy == 'RANDOM':
                entry = random.randint(0, self.size-1)
            elif self.policy == 'FIFO':
                entry = self.fifoPointer
                self.fifoPointer += 1
                if self.fifoPointer == self.size:
                    self.fifoPointer = 0
            self.mapping.pop(self.entries[entry]) # can add another function for this
            self.mapping[addr] = entry
            self.entries[entry] = addr
            self.evictionCounter[entry] += 1
        for i in [addr-1, addr+1]:
            if not i in self.addrActCounter:
                self.addrActCounter[i] = 1
            else:
                self.addrActCounter[i] += 1

def simulate(cache, mc, pattern_dir):
    with open(pattern_dir) as f:
        row = f.readline()
        while row:
            # mc.enqueueReq(int(row))
            # if mc.isFull():
            #     cache.processRequest(mc.issueReq())
            cache.processRequest(int(row))
            row = f.readline()

        # while not mc.isEmpty():
        #     cache.processRequest(mc.issueReq())

if __name__ == '__main__':
    entries = 20
    for i in range(entries//2, W//T_RH+1):
        victims = generateAttack(rows=i, pattern='LimitedRandom')
        mc = MemoryController(MC_BUFFER_SIZE, policy=MC_SCH_POLICY)
        cache = Cache(entries, EVICT_POLICY)
        simulate(cache, mc, 'output.txt')
        print("Number of victims: " + str(len(victims)))
        # print(cache.addrActCounter)
        for i in cache.addrActCounter:
            if cache.addrActCounter[i] >= T_RH:
                print("Breached")
                break