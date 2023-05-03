class A():

    z = 33

    def m1(self, x):
        print('Running m1 '+str(self)+',' + str(x) + ',' + 
              str(self.z))

    @classmethod
    def m2(cls, x):
        print('Running m2('+str(cls)+ ',' + str(x) + ') ' + 
            str(cls.z)) 

    @staticmethod
    def m3(x):
        # z é desconhecido aqui.
        # print('Running m3('+ str(x) + ') ' + str(z))    
        print('Running m3('+ str(x) + ')')

a = A()

a.m1(666)
# A.m1(777) # não pode ser ! m1 é um método de instância.
a.m2(444)
A.m2(222)
a.m3(555)
A.m3(999) 