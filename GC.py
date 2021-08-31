from object import object
from heap import heap

class MarkSweep:

    def __init__(self, heap):
        self.heap = heap
        self.size = heap.size
        self.res = 0

    def receive(self, size):
        self.res = self.new_obj(size)

    def send(self):
        return self.res

    def mark_sweep(self):
        self.mark_phase()
        self.sweep_phase()

    def new_obj(self, size):
        chunk = self.pickup_chunk(size, self.heap)
        if chunk:
            return chunk
        else:
            raise ValueError("No space")

    def pickup_chunk(self, size, heap):
        Free = heap.FREE
        while Free:
            if Free.size >= size:
                start = Free.address
                for i in range(size):
                    heap.space_mark[start + i] = 1
                obj = object(address=start, child=None, size=size)
                heap.space_[start] = obj
                Free.size = Free.size - size
                Free.address = start + size
                heap.space_[Free.address] = Free
                return obj
            Free = Free.child
        return None


    def mark_phase(self):
        r = self.heap.ROOT.child
        self.mark(r)


    def sweep_phase(self):
        sweeping = 0
        self.heap.FREE = None
        while sweeping < self.size:
            sweep_obj = self.heap.space_[sweeping]
            if sweep_obj.mark == True:
                sweep_obj.mark = False
            else:
                #print(self.heap.FREE)
                for i in range(sweep_obj.size):
                    self.heap.space_mark[sweeping + i] = 0
                sweep_obj.child = self.heap.FREE
                self.heap.FREE = sweep_obj
                #print(self.heap.FREE)

            sweeping += sweep_obj.size

    def mark(self, obj):
        if not obj:
            return
        if obj.mark != True:
            obj.mark = True
            c = obj.child
            self.mark(c)

if __name__ == '__main__':
    heap = heap(50)
    gc = MarkSweep(heap)
    gc.receive(5)
    t = gc.send()
    print(t)
    heap.heatmap()
