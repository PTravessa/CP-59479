# -*- coding: utf-8 -*-

class Student:
    """
    Author: 45672 Amadeus Mozart 

    Descrever o papel desta classe aqui.
    """

    availableCourses = ['PPO', 'FP', 'CP', "ETC1",
                        'ETC2', 'ETC3']

    def __init__(self,number,name):
        self.number = number
        self.name = name
        self.courses = []

    def getName(self):
        return self.name

    def registerCourse(self, course):
        if (course in Student.availableCourses):
            self.courses.append(course)

    @classmethod
    def getNumberOfCoursesAvailable(cls):
        return len(cls.availableCourses)

    # mutability problem
    # version 1 
    def setCourses1(self, courses):
        self.courses = courses
    # version 1
    def getCourses1(self):
        return self.courses

    # version «copy»
    def setCourses(self, courses):
        self.courses = courses.copy()
    # version «copy»
    def getCourses(self):
        return self.courses.copy()


# # Exemplo1 : criação de duas instâncias    
# s1 = Student(52123, 'Magarida Sousa')
# s2 = Student(55555, 'Herbert Schmit')     
# # acesso a um atributo de classe via uma instância (BAD)
# print(s1.availableCourses)
# # modificação do atributo de classe que 
# # parece ser um atributo de instância
# s1.availableCourses[0] = 'XXX'
# # o atributo não pertence a uma instância em particular.
# print(s2.availableCourses)
# # acesso a um atributo de classe via a classe (GOOD)
# print(Student.availableCourses)
# print(s2.availableCourses)
# # s1.registerCourse('FP')
# # uso de um método de classe
# print(Student.getNumberOfCoursesAvailable())  

# mutability problem
s3 = Student(34343, 'Anatolio Picota')
s3.setCourses(['PPO', 'FP', 'CP'])
print(s3.getCourses1())
# so far so good.
s4 = Student(12121, 'Anatolio Picoto')
c = ['PPO', 'FP', 'CP']
s3.setCourses(c)
print(s3.getCourses1())
# so far so good
c[0] = 'LOL'
# problem ! 
print('>> ' + str(s3.getCourses1()))
# test com o valor de retorno
c1 = s3.getCourses()
c1[0] = 'LOL'
print(s3.getCourses())




