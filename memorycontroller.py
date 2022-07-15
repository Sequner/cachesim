MC_POLICIES = ['InOrder', 'RowOpenish']

class MemoryController:
    def __init__(self, buff_size, policy = 'InOrder'):
        assert policy in MC_POLICIES
        self.__buff_size = buff_size
        self.__policy = policy
        self.__buff = []
        if policy == 'RowOpenish':
            self.__prevReq = None
    
    def enqueueReq(self, addr):
        assert len(self.__buff) < self.__buff_size
        self.__buff.append(addr)
    
    def issueReq(self):
        if not self.__buff:
            return None
        if self.__policy == 'InOrder':
            return self.__buff.pop(0)
        if self.__policy == 'RowOpenish':
            id = 0
            if self.__prevReq and self.__prevReq in self.__buff:    # if there is a request with same addr
                id = self.__buff.index(self.__prevReq)              # schedule it. Else, take from the top
            self.__prevReq = self.__buff.pop(id)
            return self.__prevReq

    def isFull(self):
        return len(self.__buff) == self.__buff_size

    def isEmpty(self):
        return len(self.__buff) == 0