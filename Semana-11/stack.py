
# Implementação incompleta da classe Stack que representa uma pilha.

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, n):
        self.stack.append(n)

    def pop(self):
        n = self.stack[-1]
        self.stack = self.stack[0:-1]
        return n

    def __str__(self):
        return str(list(reversed(self.stack)))
    

    
