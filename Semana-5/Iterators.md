# Iteradores
> Thibault Langlois / FCUL / DI /  2021

## *iterable* & *iterator*

> Um iterável é um objeto que possui um iterador. O iterador é obtido com o método `__iter__()` ou com a função `iter()`.

Por exemplo a função `range` é um iterável. Para obter o iterador correspondente podemos usar:
 ```python
 r = range(10)
 it1 = r.__iter__()   # usando o método ou
 it1 = iter(r)        # usando a função
 ```

O que é um iterador ? 

Um iterador é associado a um objeto que possui (ou produz) um conjunto de elementos (por exemplo, `range` produz uma sequência de valores numéricos). O papel do iterador é retornar a sequência de elementos, um da cada vez. O método que retorna os elementos é o método `___next__()` (ou a função `next()`):

```python
r = range(10)
it = r.__iter__()
a1 = it.__next__()  # a1 contém 0
a2 = it.__next__()  # a2 contém 1
a3 = it.__next__()  # a3 contém 2
# etc...
# o mesmo resultado pode ser obtido usando a função next:
a1 = next(it)
a2 = next(it)
a3 = next(it)
```

Cada vez que o método `__iter__()` é chamado num iterável, um **novo** iterador é produzido.

```python
r = range(10)
it1 = r.__iter__()
it2 = r.__iter__()
it1.__next__()     # o elemento 0 é «consumido»
it1.__next__()     # o elemento 1 é «consumido»
x = it1.__next__() # o elemento 2 é colocado em x
y = it2.__next__() # o elemento 0 é colocado em y 
```

O operador `in` pode ser usado tanto com um iterável com um iterador:

```python
r = range(10)
it1 = r.__iter__()
it2 = r.__iter__()
print(5 in r)       # mostra True
print(10 in r)      # mostra False
print(5 in it1)     # mostra True
print(3 in it1)     # mostra False
print(5 in it2)     # mostra ?
```
Para verificar a presença do valor 5 o iterador `it1` teve que avançar até este valor, usando várias vezes o método `__next__()`. Não é possível recuar no iterador, não há maneira de obter novamente os valores já consumidos. Se continuamos a sequência de instruções anterior com:

```python
print(it2.__next__())
``` 
Qual será o valor mostrado no ecrã ?

> Será o valor a seguir na estrutura: 6. 

Se a seguir escrevemos:

```python
print(2 in it2)
```
O que é que vai aparecer ?

> Vai aparecer `False` porque o elemento 2 já foi consumido.

Se a seguir escrevemos:

```python
print(8 in it2)
```
O que é que vai aparecer ?

> Vai aparecer `False` porque na instrução anterior, para verificar se o valor 2 estava presente foi necessário consumir todos os valores até o último. O iterador foi usado até o fim, já não é útil.

O iterável `range` vai produzir um novo iterator cada vez que é necessário. Por isso, se testarmos a presença de um valor num iterável `range(n)` se o valor for inferior a `n` o valor retornado será sempre `True`:

```python
r = range(10)
print(8 in r) # escreve True
print(8 in r) # escreve True
print(2 in r) # escreve True
print(10 in r) # escreve False
``` 

## Definição de um iterador
> Nesta secção vamos ver como tornar uma classe iterável.

A classe `SpecialList` adiciona a uma lista a possibilidade de haver um dos seus elementos «selecionado». Um elemento é selecionado com o uso do método `select` é retornado pelo método `getSelected`.

```python
class SpecialList:

    def __init__(self):
        self.content = []
        self.position = None

    def add(self, e):
        self.content.append(e)

    def len(self):
        return len(self.content)

    def select(self, position):
        self.selected = position
    
    def getSelected(self):
        return self.content[self.selected]
```

Quando uma classe tem como papel armazenar elementos como é o caso da classe `SpecialList`, pode ser vantajoso tornar a classe **iterável**. Para isso basta que tenha um método `__iter__()` que retorne um novo iterador cada vez que é chamado. 

```python
    def __iter__(self):
        return self.SpecialListIter(self.content)
```

O método retorna uma instância de `SpecialListIter`. Esta classe está definida como classe interna da classe `SpecialList`. Uma classe interna é uma classe definida dentro de outra. Usam-se classes internas para classe que não são usadas fora da classe que a contém. É o caso do iterador, porque apenas a classe `SpeciaList` define iteradores daquele tipo.  

Um *iterador* deve fornecer um método chamado `__next__` que retorna os elementos sucessivos. Para implementar este método temos de poder acceder ao elementos da lista e temos que memorizar a posição do último elemento retornado. O construtor inicializa dois atributos neste sentido: `elements` contém uma referência para a lista e `current` um inteiro com o índice do próximo elemento a retornar.  

O método `__next__` retorna o elemento corrente a atualiza o atributo `current`. Caso não haja mais elementos, na lista, a exceção `StopIteration` é lançada conforme a [documentação da linguagem](https://docs.python.org/3/library/exceptions.html#StopIteration). 

```python
    class SpecialListIter:
        def __init__(self, elements):
            self.current = 0
            self.elements = elements
            self.nelements = len(elements)

        def __next__(self):
            self.current = self.current + 1
            if self.current <= self.nelements:
                return self.elements[self.current - 1]
            else: 
                raise StopIteration

        def hasNext(self):
            return self.current < self.nelements
```

Adicionalmente definiu-se um método `hasNext` que retorna um valor booleano conforme existir ou não um elemento a seguir na estrutura. 

Esta definição segue o enquadramento previsto para a implementação dos iteráveis/iteradores para a linguagem python. O «enquadramento» prevê as funcionalidades a implementar bem como os nomes dos métodos que devem ser usados (`__iter__` e `__next__`). Isso permite que instruções da linguagem que funcionam com iteradores funcionam também com a nossa classe. Por exemplo poderá iterar sobre os elementos de uma instância de `SpecialList`:

```python
special = SpecialList()
special.add(888) 
special.add('hello')
special.add('world')

for thing in special:
    print(thing)
```

A classe completa é:

```python
class SpecialList:

    def __init__(self):
        self.content = []
        self.position = None

    def add(self, e):
        self.content.append(e)

    def len(self):
        return len(self.content)

    def select(self, position):
        self.selected = position
    
    def getSelected(self):
        return self.content[self.selected]

    def __iter__(self):
        return self.SpecialListIter(self.content)

    class SpecialListIter:
        def __init__(self, elements):
            self.current = 0
            self.elements = elements
            self.nelements = len(elements)

        def __next__(self):
            self.current = self.current + 1
            if self.current <= self.nelements:
                return self.elements[self.current - 1]
            else: 
                raise StopIteration

        def hasNext(self):
            return self.current < self.nelements
 
```