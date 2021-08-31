class object:

    def __init__(self, address, child, size):
        self.address = address
        #self.parent = parent
        self.size = size
        self.child = child
        self.mark = False

    def __str__(self):
        return f"address:{self.address}, size:{self.size}"
