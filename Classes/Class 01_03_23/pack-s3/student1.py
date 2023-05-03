class Student:

    availableCourses = ['PPO', 'FP', 'CP', 'ETC1', 
                        'ETC2', 'ETC3']

    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.courses = []

    def getName(self):
        return self.name

    def registerCourse(self, course):
        if course in Student.availableCourses:
            self.courses.append(course)

    @classmethod 
    def getNumberOfAvailableCourses(cls):
        return len(cls.availableCourses)

    
##------------------------------------------------

s1 = Student(56333, "Maria")
s2 = Student(32111, "Luis")

print(s1.availableCourses)
# s2.availableCourses[0] = 'XXX'
print(s1.availableCourses)

print(len(Student.availableCourses))

print(Student.getNumberOfAvailableCourses())

##------------------------------------------------
