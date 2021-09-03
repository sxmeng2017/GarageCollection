from object import object
from heap import heap


class MarkSweep:

    ROOT = object(address=-1, child=None, size=0)
    FREE = object(address=0, child=None, size=0)

    def __init__(self, heap):
        self.heap = heap
        self.size = heap.size
        self.res = 0
        self.FREE.size = heap.size
        self.heap.space_[0] = self.FREE

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
        Free = self.FREE
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
        r = self.ROOT.child
        self.mark(r)

    def sweep_phase(self):
        sweeping = 0
        self.FREE = object(address=0, child=None, size=0)
        while sweeping < self.size:
            sweep_obj = self.heap.space_[sweeping]
            if sweep_obj.mark == True:
                sweep_obj.mark = False
            else:
                #print(self.FREE)
                for i in range(sweep_obj.size):
                    self.heap.space_mark[sweeping + i] = 0
                if sweeping == self.FREE.address + self.FREE.size:
                    self.FREE.size = self.FREE.size + sweep_obj.size
                else:
                    sweep_obj.child = self.FREE
                    self.FREE = sweep_obj
                #print(self.FREE)

            sweeping += sweep_obj.size

    def mark(self, obj):
        print(obj)
        if not obj:
            return
        if obj.mark != True:
            obj.mark = True
            c = obj.child
            self.mark(c)


class MuliList:

    ROOT = object(address=-1, child=None, size=0)

    def __init__(self, heap, max_chunk=2, backup=1):
        self.heap = heap
        self.max_chunk = max_chunk
        self.backup = backup
        self.Free_list = [object(address=0, child=None, size=0)]
        self.init(max_chunk, backup)
        self.res = None

    def init(self, chunk_size, backup):
        add = 0
        for i in range(1, chunk_size + 1):
            print(i)
            obj = object(address=add, child=None, size=i)
            self.heap.space_[add] = obj
            self.Free_list.append(obj)
            add = add + i
            start = self.Free_list[i]
            #print(start, len(self.Free_list), i)
            for j in range(backup):
                obj = object(address=add, child=None, size=i)
                self.heap.space_[add] = obj
                add = add + i
                start.child = obj
                start = start.child
            #print(add)
        obj = object(address=add, child=None, size=self.heap.size - add)
        self.Free_list.append(obj)

    def receive(self, size):
        self.res = self.new_obj(size)

    def send(self):
        return self.res

    def mark_sweep(self):
        self.mark_phase()
        self.sweep_phase()

    def mark_phase(self):
        r = self.ROOT.child
        self.mark(r)



    def new_obj(self, size):
        index= size
        if index <= self.max_chunk:
            if self.Free_list[index]:
                chunk = self.Free_list[index]
                start = chunk.address
                for i in range(size):
                    heap.space_mark[start + i] = 1
                self.Free_list[index] = self.Free_list[index].child
                return chunk
        else:
            chunk = self.pickup_chunk(size, self.heap, self.Free_list[self.max_chunk + 1])
            if chunk:
                return chunk
        return None

    def pickup_chunk(self, size, heap, Free):
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

    def sweep_phase(self):
        for i in range(1, self.max_chunk + 1):
            self.Free_list[i] = None

        sweeping = 0
        self.FREE = object(address=0, child=None, size=0)
        while sweeping < self.heap.size:
            sweep_obj = self.heap.space_[sweeping]
            if sweep_obj.mark == True:
                sweep_obj.mark = False
            else:
                if sweep_obj.size <= self.max_chunk:
                    for i in range(sweep_obj.size):
                        self.heap.space_mark[sweeping + i] = 0
                    sweep_obj.child = self.Free_list[sweep_obj.size]
                    self.Free_list[sweep_obj.size] = sweep_obj
                # print(self.FREE)
                else:
                    for i in range(sweep_obj.size):
                        self.heap.space_mark[sweeping + i] = 0
                    if sweeping == self.FREE.address + self.FREE.size:
                        self.FREE.size = self.FREE.size + sweep_obj.size
                    else:
                        sweep_obj.child = self.FREE
                        self.FREE = sweep_obj
                    # print(self.FREE)
            sweeping += sweep_obj.size

    def mark(self, obj):
        print(obj)
        if not obj:
            return
        if obj.mark != True:
            obj.mark = True
            c = obj.child
            self.mark(c)

class BitMap:
    ROOT = object(address=-1, child=None, size=0)
    FREE = object(address=0, child=None, size=0)

    def __init__(self, heap):
        self.heap = heap
        self.size = heap.size
        self.res = 0
        self.FREE.size = heap.size
        self.heap.space_[0] = self.FREE
        self.bitmap = [0 for i in range(heap.size)]

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
        Free = self.FREE
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
        r = self.ROOT.child
        self.mark(r)

    def sweep_phase(self):
        sweeping = 0
        self.FREE = object(address=0, child=None, size=0)
        while sweeping < self.size:
            sweep_obj = self.heap.space_[sweeping]
            if self.bitmap[sweeping] == 1:
                self.bitmap[sweeping] = 0
            else:
                # print(self.FREE)
                for i in range(sweep_obj.size):
                    self.heap.space_mark[sweeping + i] = 0
                if sweeping == self.FREE.address + self.FREE.size:
                    self.FREE.size = self.FREE.size + sweep_obj.size
                else:
                    sweep_obj.child = self.FREE
                    self.FREE = sweep_obj
                # print(self.FREE)

            sweeping += sweep_obj.size

    def mark(self, obj):
        print(obj)
        if not obj:
            return
        if self.bitmap[obj.address] != 1:
            self.bitmap[obj.address] = 1
            c = obj.child
            self.mark(c)


if __name__ == '__main__':
    heap = heap(500)
    gc = MuliList(heap, 4, 2)
    print(gc.Free_list[5])
    gc.receive(100)
    t = gc.send()
    print(t)
    heap.heatmap()
