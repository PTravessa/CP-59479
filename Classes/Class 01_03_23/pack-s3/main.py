from user import *

u1 = User('John', 'john@example.com')

print('User: ' + u1.getName() + ' email: ' + u1.getEmail())

u2 = User('Mary', 'mary@example.com')
u2.setEmail('mary@gmail.com')
print(u2.getEmail())




