class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        print('get name')
        return self._name
    
    @name.setter
    def name(self, name):
        print('set name ' + name)
        self._name = name

    @name.deleter
    def name(self):
        print('del name ' + self.name)
        print('del name ' + self._name)
        del self._name

    def __str__(self):
        return 'Name: ' + self.name

# testing

p1 = Person('John')
print(p1)
print('A: ' + str(p1))
print('B: Name is ' + str(p1.name))
p1.name = 'Mary'
print('C: Name is ' + str(p1.name))
del p1.name
# print(p1)