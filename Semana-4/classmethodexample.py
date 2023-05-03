import math
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

    @classmethod
    def myClassMethod(cls,z):
        return math.cos(z)

    @classmethod
    def m4(cls,z):
        return math.sin(z) ** 2 + A.myClassMethod(z) ** 2

class B1(A):
    """
    Class B has two attributes: a3 and a4
    """
    def __init__(self, a1, a2, a3, a4):
        super().__init__(a1, a2)
        self.a3 = a3
        self.a4 = a4
    
    @classmethod
    def myClassMethod(cls,z):
        return math.sin(z) ** 2 + A.myClassMethod(z) ** 2


    ## define here getters & setters 


class C1 (B1):
    def __init__(self, a1, a2, a3, a4, x):
        super().__init__(a1, a2, a3, a4)
        self.x = x

    @classmethod
    def myClassMethod(cls,z):
        return - super().myClassMethod(z)


# Testing -------------------------------------------------
print('1. ' + str(A.myClassMethod(3.14))) 
print('2. ' + str(A.myClassMethod(3.1415926)))  

print('3. ' + str(B1.myClassMethod(3.14))) 
print('4. ' + str(B1.myClassMethod(3.1415926))) 

print('5. ' + str(C1.myClassMethod(3.14)))
print('6. ' + str(C1.m4(3.14)))


