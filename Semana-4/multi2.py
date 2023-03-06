class A1:
    def __init__(self):
        print('inicialize A1')  
        self.a1 = 1

    def m1(self):
        return "From m1 !"

class A2:
    def __init__(self):
        print('inicialize A2')
        self.a2 = 2

    def m2(self):
        return "From m2 !"

class B(A1, A2):
    def __init__(self):
        #super(A1,self).__init__()
        #super(A2,self).__init__()
        A1.__init__(self)
        A2.__init__(self)
        self.b1 = 12


## testing 

b = B()

print(b.m1())
print(b.m2())

