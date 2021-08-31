from object import object
from GC import MarkSweep
import time
from heap import heap
class fakeapp:

    def __init__(self, GC, waste_time=1, mode=None, func=None):
        self.waste_time = waste_time
        self.mode = mode
        self.func = func
        self.space = []
        self.GC = GC

    def get(self, size):
        self.GC.receive(size)
        obj = self.GC.send()
        parent = self.GC.heap.ROOT
        if self.space:
            parent = self.space[-1]
        parent.child = obj
        self.space.append(obj)

    def delete(self, index=-1):
        if self.space:
            obj = self.space.pop(index)
            try:
                self.del_obj(obj)
            except:
                self.GC.heap.ROOT.child = None
        else:
            raise ValueError("None space used!")


    def del_obj(self, obj):
        r = self.GC.heap.ROOT
        while r:
            c = r.child
            if c is obj:
                r.child = c.child
                c.child = None
                break
            r = c
        print(f"del {obj} from list!")

    def run(self, time_step=10):
        t = 0
        mode_l = len(self.mode)
        while t < time_step:
            print(t)
            if self.mode:
                index = t % mode_l
                t = t + 1
                self.GC.heap.heatmap()
                time.sleep(self.waste_time)
                if self.mode[index] == 0:
                    self.GC.mark_sweep()
                    #print(self.GC.heap.FREE)
                    continue
                if self.mode[index] == -1:
                    self.delete(0)
                    continue
                self.get(self.mode[index])


if __name__ == '__main__':
    heap = heap(10)
    gc = MarkSweep(heap)
    app = fakeapp(GC=gc, mode=[1, 2, 3, 4, -1, -1, 0, 1, -1 , -1, 0])
    app.run(time_step=20)
    #gc.mark_sweep()
    print(gc.heap.space_[0])
    heap.heatmap()

