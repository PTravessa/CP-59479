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

    def m1(self, z):
        return "From m2 z = " + str(z)

class B(A1, A2):
    def __init__(self):
        A1.__init__(self)
        A2.__init__(self)
        self.b1 = 12

    def m1(self, z):
        return A2.m1(self,z)

## testing -----------------------------------------

b = B()

# print(b.m1())
print(b.m1(5))

print(B.__mro__)
print(B.mro())
 