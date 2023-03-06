class A:
    """
    Class A has two attributes: a1 and a2.
    """
    def __init__(self, a1, a2):
        self.a1 = a1
        self.a2 = a2

    def getA1(self):
        return self.a1

    def getA2(self):
        return self.a2

    def m1(self):
        return 'ping'

    def m2(self):
        return 'm2 (classe A)'

    def m3(self, x):
        return x + 3


class B1(A):
    """
    Class B has two attributes: a3 and a4
    """

    def __init__(self, a1, a2, a3, a4):
        super().__init__(a1, a2)
        self.a3 = a3
        self.a4 = a4

    # define here getters & setters

    def m1(self):
        return 'pong'

    def m2(self):
        """
        m2 uses super-class' m2 method
        """
        return super().m2() + ' m2 (classe B1)'

    def m3(self, x, y):
        return x * y


class B2(A):
    def __init__(self, a1, a2, z):
        super().__init__(a1, a2)
        # tentativa de redefinição do atributo a2 
        # numa sub-classe
        self.a2 = z

    def getA2(self):
        return self.a2

    def getSuperA2(self):
        return super().getA2()


# testing ----------------------------------------
def test1():
    x = A(45, 89)
    print(x.m1())
    b1 = B1(1, 2, 3, 4)
    print(b1.m1())

def test2 ():
    x = A(45, 89)
    print(x.m2())
    b1 = B1(1, 2, 3, 4)
    print(b1.m2())

def test3():
    b1 = B1(1, 2, 3, 4)
    print(b1.m3(5,8))
    #print(b1.super().m3(55))
    #print(b1.super.m3(55))
    print(b1.m3(55))

def test4():
    b1 = B1(1, 2, 3, 4)
    # print(str(b1.getA2()) + ' ' + str(b1.getSuperA2()))
    b2 = B2(1, 20000, 3)
    print(str(b2.getA2()) + ' ' + str(b2.getSuperA2()))

#test1()
#test2()
#test3()
test4()