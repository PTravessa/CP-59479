# Programação Funcional (2/2)
> Thibault Langlois / FCUL / DI /  2021-2023

## lambdas
Quando programamos no estilo funcional precisamos muitas vezes de criar funções curtas que serão usadas num contexto muito específico. No exemplo seguinte, a função `isBig` é de uso muito local: 
```python
def isBig(x):
    return x > 1000

result = filter(isBig, [12, 1555, 3457, -7000, 23])
print(list(result)) # [1555, 3457]
```
Uma característica adicional é que essas funções muitas vezes são funções que calculam uma expressão. Nesses casos é vantajoso usar uma **lambda**.

> Uma lambda é uma expressão cujo valor é uma função. 

Uma lambda é uma função, não definida pela keyword `def`. Não tem nome atribuído, é chamada uma **função anónima**.

Para definir uma lambda usa-se a keyword `lambda`:
```python
lambda a1, a2, a3 : a2 + 2 * a3 - a1
```
a keyword `lambda` é seguida de uma sequência de parâmetros (no exemplo são três parâmetros `a1`, `a2` e `a3`) de dois pontos e finalmente a *expressão* que calcula o valor de retorno da função.

> Em python uma função lambda contém apenas uma expressão. Não pode conter instruções.

O exemplo anterior pode ser re-escrito usando uma função lambda:

```python
result = filter(lambda x: x > 1000, [12, 1555, 3457, -7000, 23])
print(list(result)) # [1555, 3457]
```

## Funções que retornam funções
Já vimos que podemos passar como argumento uma função. Esta característica permite criar funções muito mais flexíveis (genéricas). Por exemplo uma função que procura uma informação numa estrutura de dados pode receber em parâmetro a função que realizará o teste de igualdade. 

Podemos também criar funções que retornam funções. A vantagem trazida por esta característica é que permite criar funções que «fabricam» outras funções. 

Por exemplo a função adder cria «incrementadores»:

```python
def adder(n):
    def _func(a):
        return a + n
    return _func
```
a função adder pode ser usada assim:

```python
add34 = adder(34) # cria uma função de 1 parâmetro que adiciona 34
print(add34(1))   # mostra 35
```
Outro exemplo:
```python
def multiplicator(n):
    return lambda a : a * n

mult3 = multiplicator(3)

print(mult3(3))            # mostra 9

print(multiplicator(5)(3)) # mostra 15
```

Qual é o papel da função seguinte: 
```python
def o(f,g):
    return lambda *args : f(g(*args))
```
Exemplo:
```
>>> list(map(o(lambda x : x ** 2, lambda x : x + 1), [1,2,3,4]))
[4, 9, 16, 25]
>>> list(map(o(lambda x : x + 1, lambda x : x ** 2), [1,2,3,4]))
[2, 5, 10, 17]
```

## Funções que alteram o funcionamento de outras funções

Podemos criar funções que retornam uma versão modificada da função original. A ideia é criar a partir da função f(x) passada em argumento,
uma função que:

1. realiza eventualmente um pre-processamento
2. chama a função f(x)
3. realiza um pós-processamento
4. retorna o valor calculado em 2.

Exemplo:

```python
def debug(f):
    def _f(*args):
        print('function called with args: ' + str(args))
        return f(*args)
    return _f

def poly(x, a,b,c):
    return a * x**2 + b * x + c

poly = debug(poly) # poly é substituída pela versão modificada

print(list(map(lambda x : poly(x,1,2,3), range(4,8))))

```
mostra:
```
function called with args: (4, 1, 2, 3)
function called with args: (5, 1, 2, 3)
function called with args: (6, 1, 2, 3)
function called with args: (7, 1, 2, 3)
[27, 38, 51, 66]
```

Uma versão melhorada:
```python
def trace(f):
    def _f(*args):
        print('function called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result
    return _f

poly = trace(poly) 
# Atenção ! A função poly foi modificada pela função debug no exemplo anterior.
# Deve redefinir a função poly de forma a que esteja no seu estado inicial
# antes de a modificar novamente com a função trace. 
```
Testando:
```
>>> poly(4,1,2,3)
function called with args: (4, 1, 2, 3)
function returned: 27
```

Seria prático poder voltar a definição inicial da função. Para conseguir temos de memorizar a definição original. Aqui está uma nova versão:

```python
funclist={} # um dicionário para guardar as versões originais das funções

def trace2(f):
    funclist[f.__name__] = f # memorizar a definição original
    def _f (*args):
        print('function called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result

    return _f
```
As versões originais das funções transformadas estão guardadas no dicionário `funclist`. Podemos definir uma função que retorna a definição original:

```python
def untrace(f):
    _f = funclist[f.__name__]
    funclist[f.__name__] = None
    return _f
```
Para repor a definição original, basta fazer:
```
poly = untrace(poly)
```


## Decorações
A modificação de funções existentes como vimos na secção anterior, tem muitas aplicações. O python permite facilitar este processo através de «decorações». 

Uma vez definida a função `trace` (como feito na secção anterior) podemos aplicar a transformação a qualquer função usando a decoração correspondente:

```python
@trace
def someFunction(x,y,z):
     # .... definição da função

```

> Uma decoração é uma função que tem como primeiro parâmetro a função a transformar e retorna a função transformada. 

A notação `@somedecoration` seguida da definição da função `someFunction` é équivalente a :

```python
def someFunction(x,y,z):
    # definição da função
someFunction = somedecoration(someFunction)
```

Várias decorações podem estar associadas à mesma função. Neste caso, a função é alvo de várias transformações.

Várias transformações fazem parte da linguagem : `@staticmethod` `@classmethod` etc...

## functools

O módulo `functools` agrupa várias funcionalidades úteis no contexto da programação funcional.

* `@cache`: ver exercício. Esta decoração foi introduzida na versão 3.9 do python.

* `@property` pode ser usado para a definição de atributos. Por exemplo na classe `Person`, para definir o atributo `name` : 

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
	    print('call getter')
        return self._name
    
    @name.setter
    def name(self, name):
	    print('call setter')
        self._name = name

    @name.deleter
    def name(self):
        del self._name
```
Test:
```python
a = Person('Johnny')
print(a.name)
a.name = 'Jeremy'
print(a.name)
```


* A função `reduce` tem como parâmetros uma função de dois parâmetros `f(a,b)` e um iterável. `reduce` aplica a função `f` ao primeiro elemento do iterável e recursivamente aos elementos no resto da lista. É equivalente a :

```python
f(l[0],f(l[1], f(l[2], f(l[3], f(l[4], ...)))))
```
Por exemplo:

```python
reduce(lambda a, b: a + b, [13,65,67,-111])
```    
é equivalente a:
```python
13 + (65 + (67 + -111))
```
Opcionalmente, a função `reduce` pode ter mais um parâmetro que corresponde ao valor usado como segundo parâmetro da última chamada.

```python
reduce(lambda a, b: a + b, [13,65,67,-111], 1000)
```
é equivalente a:
```python
13 + (65 + (67 + (-111 + 1000)))
```

* `@wraps` esta decoração é útil no contexto da definição de outras decorações. Como uma decoração substitui uma função por outra, a sua documentação e os seus atributos deixam de estar presentes.

```python
def trace3(f):
    @wraps(f)
    def _f (*args):
        print('function ' + f.__name__ + ' called with args: ' + str(args))
        result = f(*args)
        print('function returned: ' + str(result))
        return result

    return _f

@trace3
def fact(n):
    """
    Computes the factorial of n. 
    """
    if n == 1: 
        return 1
    return n * fact(n-1)
```

Sem a decoração `@wraps` na função `trace3`, não seria possível aceder à documentação da função `fact` nem aos atributos, como por exemplo o nome (`fact.__name__`).





