class A1:
    def __init__(self):
        print('inicialize A1')  
        self.a1 = 1


class A2:
    def __init__(self):
        print('inicialize A2')
        self.a2 = 2


class B(A1, A2):
    def __init__(self):
        # super().__init__()
        # super().__init__()
        A1.__init__(self)
        A2.__init__(self)
        self.b1 = 12


## testing 

b = B()

print(str(b.a1) + ' ' + str(b.a2) + ' ' + str(b.b1))
