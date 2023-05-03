# Programação Orientada Objetos (2/3)
> Thibault Langlois / FCUL / DI /  2021-2023

## Classes e módulos
Um módulo corresponde a um ficheiro `.py` que agrupa um conjunto de funções. A ideia é fornecer um serviço para o resto da aplicação ou outras aplicações. As funções agrupadas num módulo patilham um objetivo: podem fornecer operações sobre matrizes, permitir fazer plots, disponibilizar funções para programas de contabilidade etc...

A organização do código é um aspeto muito importante no desenvolvimento de uma aplicação. Os módulos não são a única ferramenta usada para resolver o problema. Exitem em python, «packages» que podem ser vistos como o agrupamento de vários módulos (são portanto uteis para sistemas de software de grande dimensões). Provavelmente já conhece *Matplotlib* ou *Numpy* que são bibliotecas complexas organizadas em packages.

As classes são uteis a uma escala menor, servem para representar objetos que fazem parte do problema a resolver. Ver por exemplo, a classe Ad que representa um anuncio (aula passada).

É necessário declarar o uso de um módulo via a instrução `import`. 

> **Para clarificar esta organização vamos sempre usar nomes que começam com uma letra minúscula para chamar módulos e nomes que começam com uma letra maiúscula para representar nomes de classes.**

É boa prática definir poucas classes em cada ficheiro (módulo). Idelamente uma classe por módulo. Neste caso uma pessoa vai crer definir o módulo com o mesmo nome do que a classe. Seguindo a regra definida anteriormente teremos, por exemplo o módulo `user` e a classe `User`. Olhando para a perspectiva do cliente (quem usa a classe), terá que incluir no seu ficheiro:

```python
import user
```
e a seguir usar a classe `User`:
```python
u1 = user.User('Pedro')
```
ou em alternativa:
```python
from user import User
u1 = User('Pedro')
```

## Herança
O mecanismo de herança permite definir um classe de forma a **herdar** características de outra classe. O um dos benefícios é reutilizar o código escrito para outra classe.

Por exemplo, num sistema de gestão de anúncios, todos os anúncios não são iguais. Os anúncios para venda de carros devem ter itens associados diferentes dos anúncios de oferta de emprego.

Mas também têm características comuns. Por exemplo a data de publicação, o número de vez que foi vista, o utilizador que criou o anuncio etc...

Como organizar esta informação ?

Uma das maneira é organiza-la de forma hierárquica ou seja numa estrutura de árvore. Na raíz da árvore está a descrição de um anúncio muito genérico. Pode ter como atributos:

* autor (o utilizador que a criou)
* data de criação
* item para transação
* tipo de transação (compra/venda/aluguer etc...)

> ver o código no modulo `ad`

Um anúncio para venda de um carro deve ter mais características:

* marca
* modelo
* ano de fábrico
* número de quilómetros
* estado

No objeto de tipo anúncio-para-vender-carro não queremos repetir os atributos identificados no anúncio genérico descrito acima. Para isso basta estabelecer uma relação de herança entre as duas classes.

Para isso, basta indicar a seguir ao nome da classe o nome da super-classe, entre parêntesis:

```python
class CarAd(Ad):
```
O construtor merece uma atenção especial. Deve inicializar os atributos da própria classe mas também os atributos da super-classe. Deve portanto chamar o construtor da super-classe: 

```python
    def __init__(self, author, publicationDate, item, transactionType, 
                brand, model, year, km, state):
        super().__init__(author, publicationDate, item, transactionType)   
        self.brand = brand
        self.model = model
        self.year = year
        self.state = state
```

### Métodos de instância

> Uma instância de uma classe `B` sub-classe de `A` pode usar todos os métodos de instância das suas super-classes.

Seja a classe `Feline` sub-classe da classe `Animal` e a classe `Cat` subclasse da classe `Feline`. 

* O método `run` definido na classe `Feline` poderá ser usado pelas instâncias de `Cat`. 

* O método `breathe` da classe `Animal` poderá ser usado pelas instâncias de `Feline`, `Cat` e de modo geral por todas as instâncias das sub-classes de `Animal`.

O que é que acontece se um método `m1` definido na super-classe `A` for definido na sua sub-classe `B`? 

---
> ver `test1()` no módulo `supersub`
---

> Se um método for **redefinido** (*override*) numa sub-classe, será este o método que será executado quando for chamado via uma instância da sub-classe.

> Um método redefinido numa sub-classe, pode ter uma assinatura diferente daquela definida na super-classe.

> Um método definido na sub-classe pode fazer uso do mesmo método definido na super-class usando `super().m2(x)`.

---
> ver `test2()` e `test3()` no módulo  `supersub`
---

### Atributos de instância

Não se pode redefinir na sub-classe um atributo definido na super-classe.

---
> ver `test4()` no módulo  `supersub`
---

### Métodos de classe

No contexto de uma classe, um método de classe pode fazer uso de um método de classe da sua super-classe usando `super().myClassMethod()` (onde myClassMethod corresponde ao método da super-classe)

---
> ver o módulo  `classmethodexample`
---

### Uma alternativa a super()

Existe uma alternativa ao uso do método `super` para aceder à super-classe. Pode-se nomear explicitamente a classe. Em vez de escrever:

```python
    def __init__(self, a1, a2, a3, a4):
        super().__init__(a1, a2)
        self.a3 = a3
        self.a4 = a4
```
Pode escrever :
```python
    def __init__(self, a1, a2, a3, a4):
        A.__init__(self, a1, a2)
        self.a3 = a3
        self.a4 = a4
```
Note que no segundo caso deve-se passar o parâmetro `self`.


## Herança múltipla

Uma classe pode herdar as características de várias classes. Neste caso falamos de herança múltipla. Para definir uma classe `B` que herda as características das classes `A1` e `A2` deve-se escrever:

```python
class B (A1, A2):
        # definição da classe
```

### Construtores

Uma classe `B` que herda duas classes `A1` e `A2` pode ter que inicializar atributos que pertencem as suas super-classes. Para isso, on construtor de `B` deve invocar explicitamente os construtores das super-classes: 

```python
    def __init__(self, a1, a2, a3):
        A1.__init__(self, a1)
        A2.__init__(self, a2)
        self.a3 = a3
```
Note que é necessário passar o parâmetro `self` para os construtores das super-classes.

Ao invocar o construtor *implícito* (através de `super()`) do nível antérior será o construtor da primeira super-classe que será executado (no exemplo, o construtor de `A1`)

### Métodos

Se um método `m1` existir em várias super-classes, será sempre o método da primeira classe onde o método se encontra que será executado.
A procura do método a executar é feita em profundidade e da esquerda para a direita. O sentido da esquerda para a direita entende-se segundo a ordem das super-classes na definição da sub-classe. No exemplo seguinte a classe `Z` tem precedência sobre a classe `W` e `W` sobre a classe `R`:

```python
class G(X, W, R):
        # definição da classe aqui.
```
No exemplo anterior, caso nã se encontre o método na classe `X`, a procura continua nas super-classes de `X` antes de procurar na classe `W`.

> o primeiro método encontrado é executado.

---
> ver exemplos nos módulos  `multi1`, `multi2`, `multi3`, `multi4` e `multi5`
---

### Cores e sabores 

A herança múltipla encoraja um estilo de programação objeto chamado *Mixins* onde se cria classes baseadas em várias super-classes que podem ter funcionalidades próximas (e até métodos com mesmo nome). A classe criada implementa uma escolha ou uma composição das funcionalidades das super-classes. Por exemplo, várias super-classes `A1`, `A2`, etc...implementam o método `m1`. Queremos usar a implementação presente na classe `A2`. Para isso basta na sub-classe escrever um método que chama o método desejado:

```python
    def m1(self, z):
        return A2.m1(self,z)
```  

Podemos também «remover» funcionalidades indesejadas. Se uma ou mais super-classes implementa um método `mx` que não queremos disponibilizar na sub-classe, podemos definir:

```python
    def mx(self, y):
        raise NotImplementedError
```
para prevenir o seu uso.

## Composição
Existe uma alternativa ao uso da herança (e até ao uso da herança múltipla): a *composição* 

Enquanto a herança representa uma relação de tipo «*is-a*», a composição tem como objetivo representar relações de tipo «*has-a*». [Note que não há equivalência entre as duas abordagens]. Temos uma relação de tipo composição quando um atributo de uma classe `A` é de tipo «classe B». Neste caso as instâncias de `A` possuem uma instância de `B`. Uma ilustração desta abordagem é a representação de veículos (por exemplo num simulador que ajuda a escolha do modelo). Nessa situação é vantajoso representar uma classe `Vehicle` que será composta de elementos que por sua vez são instâncias de outras classes: 

* a classe `Engine` e suas sub-classes definem as opções de motorização,
* a classe `EntertainmentSystem` e as suas subclasses definem o tipo de rádio, acesso internet, ecrã e colunas instalados no veículo, 
* a classe `NavigationSystem` define o tipo de GPS instalado,
* etc ...

