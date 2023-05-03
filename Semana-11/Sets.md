# Sets (1/1)
> Thibault Langlois / FCUL / DI /  2022

## Sets
Para além das listas e dos dicionários, o Python oferece um estrutura de dados chamada **Set**. 

> Um **set** é um conjunto não ordenado de elementos não repetidos.

Um set é criado com a função `set`:

```python
s = set()  # define um conjunto vazio
print(s)   # mostra: set()
```
Pode-se criar um conjunto inicializando-o com os elementos de uma lista:

```python
s = set([1,3,'a',4,'c'])
print(s)   # mostra: {1, 3, 4, 'a', 'c'}
```
Se a lista tiver elementos repetidos:
```python
s = set([1,3,'a',4,'c',1,3,'a'])
print(s)   # mostra: {1, 3, 4, 'a', 'c'}
```
não aparecem duplicados no conjunto.

Pode-se criar um set a partir de uma cadeia de caracteres. Neste caso os elementos do conjunto correspondem aos caracteres presentes na cadeia.

É igualmente possível criar um conjunto enumerando os seus elementos entre chavetas: 
```python
s = {'o', 'meu', 'conjunto'}
```

> Não se pode obter os elementos de um set via um índice. Mas um set é iterável:
```python
s = set([1,3,'a',4,'c',1,3,'a'])
for a in s:
    print(a) 
```
Note que não sabemos em qual ordem os elementos do conjunto vão aparecer.

## Métodos do set:

| método, função ou operador | descrição |
|------------------|----------|
| `len(s)`           | número de elementos |
| `s.add(e)`         | adiciona o elemento e |
| `s.update(it)`     | adiciona os elementos que se encontram no iterável.
| `str(s)`           | representação sob forma de string
| `s.__str__()`      | idem      |
| `e in s`           | `True` se o elemento `e` faz parte de `s`; `False` caso contrário|
| `s.remove(e)`      | remove o elemento `e` do conjunto `s`. Lança uma exceção se `not e in s` | 
| `s.discard(e)`     | remove o elemento `e` do conjunto `s`. Se `not e in s` não dá erro. |
| `s.pop()`          | remove e retorna um elemento de `s` |
| `s.clear()`        | remove todos os elementos do conjunto `s`. |
| `s1.union(s2)`     | retorna um novo conjunto composto pela união de `s1` e `s2` |
| `s1.intersection(s2)` |  retorna um novo conjunto composto pela intersecção de `s1` e `s2` |   
| `s1.difference(s2)` | retorna um novo conjunto composto pelos elementos de `s1` que não pertencem a `s2` |
| `s1 - s2` | idem |
| `s1.issubset(s2)`   | Retorna True se todos os elementos de `s1` pertencem a `s2`; False caso contrário |
| `s1.isdisjoint(s2)` | Retorna `True` se a intersecção de `s1` e `s2` está vazia; `False` caso contrário
| `s1.issuperset(s2)`  | Retorna `True` se todos os elementos de `s2` encontram-se em `s1`; `False` caso contrário

Notas:

* s.update(it) funciona com qualquer tipo de iterável (listas, tuples, sets etc...)

## Igualdade
A noção de conjunto não pode ser pensada sem a noção de igualdade. Para adicionar um elemento a um conjunto é necessário verificar se já existe o que não pode ser feito sem recorrer a uma função de igualdade. Esta verificação é feita automaticamente mas temos que definir a noção de igualdade apropriada para o problema a tratar. 

### O operador `is`
O operador `is` realiza um teste sobre a identidade. Significa que se `x is y` é verdadeiro, então:

* `x` e `y`são de tipo inteiro ou string e têm o mesmo valor *OU*
* `x` e `y` contêm a mesma referência de memória

### O operador `==`

mostrar um exemplo onde x == y e not x is y


### O método `__eq__()`
Seja a classe `Person`:
```python
class Person:
    def __init__(self, name, age):
        self.name =  name
        self.age = age
```
e duas instâncias desta classe:

```python
p1 = Person('John', 23)
p2 = Person('Mary', 33) 
```

Como testar se duas instâncias são iguais ?

```python
print(p1 == p2)    # mostra: False
```

Mas se definimos uma terceira instância:

```python
p3 = Person('John', 23)
print(p1 == p3)   # mostra: False
```

Para os objetos o teste realizado é o teste de identidade. Como funciona ?

O operador `==` chama o método `__eq__()`:
> `p1 == p2` é equivalente a `p1.__eq__(p2)`. Mas `__eq__()` não está definido na classe `Person` ! Está definida na classe `object`. A definição do método na classe object é mais ou menos equivalente a:

```python
def __eq__(self, other):
    return self is other
```
pelo menos é o que podemos deduzir do comportamento observado.

Para definir um noção de igualdade adequada para a classe `Person` podemos redefinir o método (*override*): 

```python 
def __eq__(self,p):
    return self.name == p.name and self.age == p.age
```

Esta definição tem um defeito, o parâmetro `p` pode não conter uma instância de `Person` e neste caso não ter os atributos `name` e `age`. Para que não dê erro neste caso podemos isar:

```python
def __eq__(self,p):
    if isinstance(p, Person):
        return self.name == p.name and self.age == p.age
    return False
```
> Deve-se **sempre** fazer um teste usando a função `isinstance()` antes de aceder aos atributos do parâmetro do método `__eq__()`.

Podemos retomar o exemplo anterior:
```python
p3 = Person('John', 23)
print(p1 == p3)   # mostra: True
```
e observar que agora obtemos o comportamento esperado.

Qual a relação com os conjuntos ? 
Internamente os conjuntos usam a noção de igualdade, faz portanto sentido especificar a implementação deste método numa classe cujas instâncias serão inseridas num conjunto.

Mas não é o único requisito. 

Se experimentamos adicionar uma instância de `Person` (onde a classe já tem o método `__eq__()`), vamos obter um erro:

```
s = set([p1])
TypeError: unhashable type: 'Person'
```

Portanto o que é que significa que a classe deve ser *hashable* ? 

Deve possuir um método `__hash__()`. Este método deve retornar uma chave que é tal que, para duas instâncias `a` e `b`:

* se `a == b` então `a.__hash__()` e `b.__hash__()` são iguais. 
* o valor retornado deve ser um número.
* se houver uma «pequena» diferença entre `a` e `b` então a diferença entre os valores `a.__hash__()` e `b.__hash__()` é grande (deve favorecer a «dispersão»)
* pode acontecer que `a.__hash__() == b.__hash__()`
e `a != b`. Neste caso dizemos que existe uma **colisão**. É inevitável mas deve ser, na medida do possível, raro.

A condição de «dispersão» é difícil obter mas felizmente o Python dá uma ajuda com a função `hash()`. 

A implementação pode portanto ser feita da seguinte forma:

```python
class Person:
    def __init__(self, name, age):
        self.name =  name
        self.age = age

    def __hash__(self):
        return hash((self.name, self.age))
    
    def __eq__(self,p):
        return self.name == p.name and self.age == p.age
```
Ou seja:

> Redefinir um método `__hash__()` que cria um tuple com os valores dos atributos do objeto e usa a função `hash` para obter o valor desejado. 

