
class Person:
    def __init__(self, name, age):
        self.name =  name
        self.age = age

    def __str__(self):
        return self.name + ' (' + str(self.age) + ')'

    def __eq__(self,p):
        return isinstance(p, Person) and self.name == p.name and self.age == p.age
        

    def __hash__(self):
        print('Olá !!!')
        return hash((self.name, self.age))

    

    
p1 = Person('John', 23)
p2 = Person('Mary', 33)
p3 = Person('John', 23)
p4 = Person('Mary', 32)

print(p1 == p2)
print(p1 == p3)
s = set()
s.add(p1)
s.add(p2)
print(p1.__hash__() % 100)
print(p2.__hash__() % 100)
print(p4.__hash__() % 100)
quit()

s = set([p1, p2])
for p in s:
    print(p)

print('----------')
p3 = Person('John', 23)
s.add(p3)

for p in s:
    print(p)



