# -*- coding: utf-8 -*-

def adder(n):
    def _func(a):
        return a + n
    return _func

add34 = adder(34)

print(add34(1)) 

def multiplicator(n):
    return lambda a : a * n

mult3 = multiplicator(3)

print(mult3(3))

print(multiplicator(5)(3))

# parâmetros especiais em python:
def xx(a, *args, z):
    print('a:' + str(a) + ' ' + 'args: ' + str(args) + ' z: ' + str(z))

xx(1,2,3,z=4)

def o(f,g):
    return lambda *args : f(g(*args))

# Para obter os primeiros 5 caracteres em maiúsculas de uma lista de strings:

l = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
print(list(map(o(lambda s : s[0:5], lambda s: s.upper()), l)))
# a função 'o' permite cria uma função que e a composição das duas lambdas.
# o(f, g) -> (f o g)


def debug(f):
    def _f(*args):
        print('function called with args: ' + str(args))
        return f(*args)
    return _f

def poly(x, a,b,c):
    return a * x**2 + b * x + c

poly = debug(poly)

# print(poly(4,1,2,3))
print(list(map(lambda x : poly(x,1,2,3), range(4,8))))

def trace(f):
    def _f(*args):
        print('function called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result
    return _f

def poly2(x, a,b,c):
    return a * x**2 + b * x + c

poly2 = trace(poly2)

poly2(4,1,2,3)

print('-------------------')

# esta versão memoriza as funções decoradas para poder repor
# a definição original
funclist={}

def trace2(f):
    funclist[f.__name__] = f
    def _f (*args):
        print('function called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result

    return _f

def myFunc3(x, a,b,c):
    return a * x**2 + b * x + c

myFunc = trace2(myFunc3)
myFunc(4,1,2,3)

print(funclist)

def untrace(f):
    _f = funclist[f.__name__]
    funclist[f.__name__] = None
    return _f

myFunc = untrace(myFunc3)
print(myFunc(4,1,2,3))

def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)

print(fact(5))

fact = trace2(fact)

print(fact(5))

def fib(n):
    # quem nao sabe o que sao os números de Fibonacci ?
    # que tal escrever esta função (recursiva) ?
    pass

print(list(map(fib, range(10))))

# esta versão e igual, e apenas para testar a decoração @trace
@trace
def fib2(n):
    # quem nao sabe o que sao os números de Fibonacci ?
    # que tal escrever esta função (recursiva) ?
    pass

# fib2(3)

    
from functools import wraps

def trace3(f):
    # experimentar com a linha seguinte comentada e sem ser comentada
    # @wraps(f)
    def _f (*args):
        print('function ' + f.__name__ + ' called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result

    return _f

@trace3
def fib3(n):
    """
    fib3 The fibonacci function returns the fibonacci number of rank n

    Args:
        n (integer): a positive integer

    Returns:
        integer: a fibonacci number 
    """
    # definição da função
    pass

print(fib3(4))

print(fib3.__name__)
# help(fib3)

