# Programação Funcional (1/2)
> Thibault Langlois / FCUL / DI /  2021-2023

**Programação imperativa**

O paradigma principal do python é a programação imperativa. 

* receitas descritas por sequências de instruções 
* global state

**Programação Orientada Objetos**

* Classes permitem encapsular a definição de novos objetos (atributos e métodos)
* Instâncias representem concretizações das classes. 
* Em vez de privilegiar um estado global, representa-se estados locais constituídos pelas instâncias.

**Programação funcional**
* funções puras
* funções como parâmetro
* funções com valor de retorno 

## Expressão vs Instrução

Uma instrução não produz um valor. Por exemplo uma atribuição não produz um valor, não pode escrever:
```python
print(x = 33) 
```
Um ciclo é também uma instrução. Permite executar **instruções** mas não produz um valor. O excerto seguinte contém três instruções: duas atribuições e uma instrução for:

```python
sum = 0
for x in range(10):
    x = sum + x
```
também contém três **expressões**:

1. `0` é uma expressão
2. `range(10)` é uma expressão
3. `sum + x` é uma expressão

> As expressões representam valores. 

Se é possível imprimir uma *coisa* então esta coisa é uma expressão.

Existem relativamente poucas instruções na linguagem python. São as instruções de atribuição (`=`, `+=`, ...), os ciclos os condicionais (`if`) mais algumas associadas aos keywords `while`, `class`, `def`, `except`, `raise`, `with`, `return` etc...

Uma chamada a uma função é uma expressão. Mesmo que a função não tenha instrução `return`, retorna o valor `None` que pode ser impresso. 


## O que é um *side effect* ?

Uma função pode alterar o estado do programa, modificando uma variável global, o estado de uma instância ou o valor de um dos seus parâmetros:

```python
def aoQuadrado(x):
    global a
    a = x ** x

def setPrice(self, value):
    self.price = value

def f46(l):
    l.append('a')
```

> Uma função sem instrução `return` produz um efeito lateral. 

O efeito lateral pode ser uma alteração no ecrã:
```python
def f1(x):
    print('O valor de x é: ' + str(x))
```

Pode também ser a criação de um ficheiro:
```python
def writeX(x):
    with open("file.txt", "w") as file:
        file.write(x)
```

Embora não seja aconselhado[1], uma função pode ter uma instrução return e ao mesmo tempo produzir um efeito lateral:

```python
def writeX(x):
    with open('file.txt', 'w') as file:
        file.write(str(x))
    return x ** 2
```

Uma função também pode ser alvo de um efeito lateral.
Pode, por exemplo,  depender de valores contidos em outras variáveis:

```python
def f2(x):
    return x + a
```
ou depender de valores contidos num ficheiro:

```python
def readXandAdd(n):
    with open('file.txt','r') as file:
        x = int(file.read())
        return x + n
```

## Funções «puras»

Funções ou métodos definidos em python com a keyword `def` podem ser de dois tipos:

* funções impuras
* funções puras

> Até agora a distinção entre os dois tipos de funções não foi considerada relevante, no contexto da aprendizagem dos conceitos básicos da linguagem mas agora vamos estudar este aspeto.

Uma função impura pode:

* alterar os seus parâmetros
* alterar variáveis globais
* fazer uso de variáveis globais
* não ter instrução `return`.

> Uma função impura produz ou é alvo de efeitos laterais.

> Uma função é pura se não produzir e não é alvo de efeitos laterais. 

> Uma consequência é que chamar uma função pura uma ou mil vezes (com os mesmos argumentos) dará sempre o mesmo resultado.   

Funções puras podem ser executadas em paralelo.
Dado que uma função pura retorna sempre o mesmo resultado para um dado conjunto de valores dos seus parâmetros, pode-se otimizar o tempo de cálculo memorizando os valores de retorno. Esta característica é conhecida como [*referential transparency*](https://en.wikipedia.org/wiki/Referential_transparency). 


Exemplos:

```python
def func3(t):
    t = t + ('aaa',)

def func4(t):
    t = t + ('aaa',)
    return t
```
`func3` é pura ou impura ? e `func4` ?

```python
def f47(l):
    l.append('a')
    return l

def f48(l):
    l = l + ['a']
    return l

def f49(l):
    l = l + ['a']
    return l[:-1]    
```

A vantagem trazida pelo uso de funções puras é que facilita muito a programação. A função não é influênciada pelo estado do «ambiente» (o ambiente é constituído pelos valores contidos em todos as outras variáveis (globais) em inglês: *global state*). O resultado produzido depende apenas dos valores dos parâmetros. A função pode portanto ser estudada isoladamente em relação ao resto do programa.


## Funções são valores

Ao definir uma função `f1` estamos a colocar na variável `f1` um objeto que é de tipo «function».

```python
def f1(a, b):
    return a * b

f2 = f1        # f2 contém o mesmo valore do que f1

print(f2(3,4)) # mostra 12 no ecrã
print(f1)      # mostra <function f1 at 0x7fcec317b280>
```
Esta característica permite usar funções como um valor qualquer. Para além de chamar uma função podemos: 

* passar uma função como parâmetro de outra função,
* definir uma função que retorna outra função.

> As funções que têm uma dessas duas características são chamadas **funções de ordem superior**.


## Funções como parâmetros

Aqui está um exemplo de passagem de uma função como parâmetro de outra função.

```python
def add(x, y):
    return x + y

def doIt(func, x, y):
    return func(x,y)     # chamada à função passada
                         # em parâmetro

print(doIt(add, 56, 78)) # mostra 134 no ecrã
```

Na biblioteca do python há muitas funções de ordem superior. Por exemplo a função `sort`:

```python
l2 = [[34, 'Ricardo'], [23, 'Felisberto'], [13, 'Raquel']]
l2.sort() 
# [[13, 'Raquel'], [23, 'Felizberto'], [34, 'Ricardo']]
print(l2)

def second(l):
    return l[1]

l2.sort(key=second)
print(l2) 
# [[23, 'Felisberto'], [13, 'Raquel'], [34,'Ricardo']]
```

### Função `map`
A função `map` recebe em parâmetro uma função `f` e um iterável. Retorna um novo it que contém o resultado de chamar a `f` em todos os elementos do iterável. 

```python
def add1(x):
    return x + 1

result = map(add1, [23,56,12,53])
print(list(result))  # list() cria uma lista com os valores do iterável.

result = map(add1, range(10))
print(list(result)) 
```
No caso geral, a função pode receber um número arbitrário de iteráveis, neste caso a função deve receber o mesmo número de argumentos. A função será chamada com o primeiro valor de cada iterável, s seguir com os segundos valores dos iteráveis até encontrar o fim de um dos iteráveis. Aqui está um exemplo com duas listas:

```python
def plus(x,y):
    return x + y

result = map(plus, [1,2,3,4,5,6], [6,5,4,3,2,1,1000, 5000])
print(list(result)) # mostra [7, 7, 7, 7, 7, 7]
```

> O número de argumentos da função passada à função `map` deve ser igual ao número de iteráveis.

### Função `filter`
A função filter recebe uma função que deve retornar `True`ou `False` (uma função com esta característica chama-se um **predicado**) e um iterável. Retorna (num iterável) os elementos do iterável para os quais o predicado retorna `True`.
Por exemplo: 

```python
def isBig(x):
    return x > 1000

result = filter(isBig, [12, 1555, 3457, -7000, 23])
print(list(result)) # [1555, 3457]
```


## Notas 
[1] [Para saber mais sobre este assunto.](http://martinfowler.com/bliki/CQRS.html)
