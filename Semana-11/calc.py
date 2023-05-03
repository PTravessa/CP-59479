from stack import Stack
from myexceptions import BadOperatorException

st = Stack()

def calc():
    #print('> ', end='')
    r = input('> ')
    while r != 'quit':
        # Rever este ciclo.
        # Quando o utulizador digite um número, deve
        # ser colocado na pilha quando entra um operador, o número de operandos
        # necessários devem ser tirados da pilha e o resultado da operação colocado
        # na pilha.
        #
        f = 0
        f = float(r) # esta função lança uma exceção. Cosulte a documentação.
        st.push(float(f))
        if r == '+':
            st.push(st.pop() + st.pop())
        elif r == '/':
            a = st.pop()
            b = st.pop()
            st.push(b/a)
        else:
            # esta exceção deve ser criada.
            raise BadOperatorException('Unkown operator: ' + r)
        print(st)
        r = input('> ')


