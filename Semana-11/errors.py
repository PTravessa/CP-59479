
try:
    x = 50
    y = 1
    print(x / y)
    f = open("inexistent.txt", mode='r')
except Exception as e:
    print('Something is bad: ' + str(e))
    pass


 
try:
    x = 50
    y = 1
    print(x / y)
    f = open("inexistent.txt", mode='r')
except FileNotFoundError as e:
    print('O ficheiro não existe ! (' + str(e) + ')')
except ZeroDivisionError as e:
    print('You cannot divide by zero.')
else:
    print('this line is executed if no errors occured.')
    f.close()
finally:
    print('this line is executed in all cases.')

try:
    x = 50
    y = 0
    print(x / y)
    f = open("inexistent.txt", mode='r')
except Exception as e:
    print('Something is bad: ' + str(e))
except ZeroDivisionError as e:
    print('You cannot divide by zero.')
else:
    print('this line is executed if no errors occured.')
    f.close()
finally:
    print('this line is executed in all cases.')

def between(x, min, max):
    if min > max:
        raise ValueError('The value of min must be less than max') 
    return x >= min and y <= max


try:
    if between(x, 1, -1):
        print('x is between -1 and 1.')
except ValueError as e:
    print('Ooops !')
