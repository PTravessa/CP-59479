# Programação Orientada Objetos (1/3)
> Thibault Langlois / FCUL / DI /  2021

## Definições
### Classe
Uma classe é um plano que permite a criação de um objeto. Pode ser visto como um molde a partir do qual vários objetos (ou **instâncias**) podem ser criados. Uma classe tem geralmente um conjunto de atributos e de funções associadas. As funções associadas a uma classe são chamadas **métodos**.
Uma classe representa um conceito relevante para o problema a resolver. 

Exemplo de classe encontrada em muitas aplicações: a classe `User` que representa um utilizador da aplicação.  
### Instância
Uma instância é um objeto (um valor que pode ser associado a uma variável) que corresponde a um exemplar (uma instância) de uma classe. 
### Atributos
Existem dois tipos de atributos:
1. atributos de instância: são associados a cada instância. Cada instância tem um valor próprio para o atributo. No exemplo da classe `User` os atributos de instância podem ser o nome do utilizador, a sua password etc...
2. atributos de classe: são atributos cujo valor é partilhado por todas as instâncias. É associado à classe e não a instância. O papel de um atributo de classe é semelhante a uma variável global num módulo. Um uso comum para o atributo e classe é quando queremos contar o número de instâncias de uma classe. Este contado tem de ser um atributo de classe.

### Métodos
Existem dois tipos de métodos:
1. métodos de instância
2. métodos de classe
A distinção é semelhante ao caso dos atributos. Mais exemplos a seguir...

---
>>>>>> exemplo: classe User
---

## Estrutura de uma classe
1. A definição da classe começa com a palavra reservada `class` seguida do nome da classe.
Exemplo:
```python
class User:
```
> Não sendo um requisito da linguagem, é considerado *boa prática da programação* começar o nome da classe por **uma letra maiúscula**.

2. Define-se um método especial cujo papel é criar e inicializar uma instância: `__init__`
Exemplo: 
```python
    def __init__(self, name, email):
        self.name = name
        self.email = email
```
> Este método é chamado o **construtor**.

> O construtor, **como todos os métodos** de instância recebe como primeiro parâmetro `self` uma referência à própria instância. Permite aceder aos atributos e métodos da classe.

3. Define-se getters e setters
São métodos que permitem obter e alterar o valor dos atributos de uma instância.
Exemplo:
```python
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email

    def setName(self, newname):
        self.name = newname

    def setEmail(self, newemail):
        self.email = newemail
``` 
Muitas vezes não queremos que o estado do objeto seja alterado. Nesses casos não se define setters

> Não sendo um requisito da linguagem, a definição de getters (e, eventualmente, setters) é uma **obrigação** ditada pelas *boas práticas de programação*. 

## Como usar uma classe ?
Se estiver num módulo diferente é necessário importar o módulo.
Para criar uma instância basta invocar o construtor :
```python
u1 = User('John', 'john@example.com')
```
Os métodos de instância são acessíveis via o ponto:
```python
print(u1.getName())
```
> Os atributos também são acessíveis via o ponto i.e. `u1.name` mas **não se devem usar** ! Deve antes usar o *getter*.

## Atributos de classe
Um atributo de classe é um atributo cujo valor é associado à classe e não às instâncias. Não pode armazenar um valor que será especifico a cada instância. É definido como uma variável global ao nível da classe.

> Exemplo: Numa classe `Student` existe um atributo (de instância) chamado `courses` que armazena os cursos aos quais o aluno está inscrito. Para verificar que as inscrições estão corretas a classe possui um atributo de classes `availableCourses` que contém a lista das disciplinas às quais o aluno pode inscrever-se. 

---
>>>>>> exemplo
---

```python
    availableCourses = ['PPO', 'FP', 'CP', "ETC1",
                        'ETC2', 'ETC3']
```
O método que trata da inscrição usa esta lista:
```python
    def registerCourse(self, course):
        if (course in Student.availableCourses):
            self.courses.append(course)
```
> Para aceder a um atributo de classe, fora da classe, deve-se fazê-lo via o nome da classe i.e. `Student.availableCourses` e não (embora seja possível) via uma instância.


## Métodos de classe
Enquanto é necessário existir uma instância para usar um método de instância, não é o caso para um método de classe. Um método de classe é usado quando nenhuma instância é necessária ou disponível.
Por exemplo, numa classe `PlayList` que representa listas de músicas, podemos ter uma operação `concatenate` que cria uma nova instância de playlist a partir de duas:
```python
myNewPlaylist = PlayLists.concatenate(listA, listB)
``` 
Neste exemplo toda a informação necessária a criação da nova playlist é passada nos argumentos. O método cria uma nova instância de `PlayList` e adiciona as músicas contidas nas duas listas. Este método é portanto um método de classe. 
```python
    @classmethod
    def concatenate(cls, list1, list2):
        result = PlayList()
        result.musics = list1.musics + list2.musics
        print(cls)
        return result
```
Se, em alternativa, queremos adicionar a uma `PlayList` os elementos de um segunda `PlayList`, o mais lógico é criar um método de instância:
```python
    def appendMusics(self, other):
        self.musics.extend(other.musics)
```
Também poderíamos ter optado por um método de classe mas não faz muito sentido:
```python
    @classmethod
    def appendMusics(cls, list1, list2):
        list1.musics.extend(list2.musics)
```


## Valores mutáveis e classes
Como em qualquer ocasião, é preciso ter especial atenção aos valores mutáveis no contexto da definição de uma classe.
Acrescentamos na classe `Student` um método `addCourses` que tem como objetivo acrescentar vários cursos a uma instância de aluno. 

---
>>>>>> exemplo
---

Quando se usar valores mutáveis nos argumentos e/ou retorno de métodos é preciso: 

* copiar os valores recebidos através dos parâmetros,
* retornar cópias dos valores caso correspondem ao estado do objeto.

> Isto é também válido no caso de funções, não apenas para métodos.

A solução da «cópia» dos valores não é 100% segura. No exemplo da classe `Student` se os cursos são representados por instâncias de uma classe `Course`, será que a cópia da lista de cursos é suficiente ?

Depende !

---
>>>>>> exemplo
---

### Solução
Não permitir que as instâncias de `Course` seja alteráveis. Para isso basta não definir setters.

> Nesta caso a classe é chamada **imutável**.

Usar estruturas imutáveis. Preferir tuples a listas. Na classe `Student` se os métodos recebem parâmetros e retornam valores de tipo tuple em vez de listas, não será possível altera-las. (quase)

> Em qualquer caso não há receita infalível para este problema em Python. A solução consiste em entender em profundidade esses mecanismos, estar atento e rigoroso na aplicação das *boas práticas de programação*.







