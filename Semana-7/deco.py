from functools import wraps

calls = {}

def countcalls(f):
    calls[f.__name__] = 0
    @wraps(f)
    def _f(*args):
        calls[f.__name__] = calls[f.__name__] + 1
        return f(*args)
    return _f

def howManyCalls(f):
    return calls[f.__name__]

def resetCalls(f):
    calls[f.__name__] = 0

@countcalls
def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


print(howManyCalls(fact))
print(fact(5))
print(howManyCalls(fact))
resetCalls(fact)
print(howManyCalls(fact))
print(fact(5))

 
