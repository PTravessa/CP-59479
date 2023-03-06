# Programação Orientada Objetos (1/3)
> Thibault Langlois / FCUL / DI /  2021-2023

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

```python
   # version 1:
   def setCourses1(self, courses):
       self.courses = courses

   def getCourses1(self):
       return self.courses
```
No programa cliente:
```python
s3 = Student(34343, 'Anatolio Picota')
s3.setCourses1(['PPO', 'FP', 'CP'])
# ...
print(s3.getCourses1())
s4 = Student(12121, 'Anatolio Picoto')
c = ['PPO', 'FP', 'BM']
s4.setCourses(c)
# ...
print(s4.getCourses1())
# ...
c[0] = 'XXX'
# ...
print(s4.getCourses1())
```
Nova versão:
```python
   # version 2:
    def setCourses2(self, courses):
        self.courses = courses.copy()

    def getCourses2(self):
        return self.courses.copy()
```
Mesmo test:
```python
s5 = Student(12121, 'Archibaldo Rabanete')
c = ['PPO', 'FP', 'BM']
s5.setCourses2(c)
# ...
print(s5.getCourses2())
# ...
c[0] = 'XXX'
# ...
print(s5.getCourses2())
```

Quando se usar valores mutáveis nos argumentos e/ou retorno de métodos é preciso: 

* copiar os valores recebidos através dos parâmetros,
* retornar cópias dos valores caso correspondem ao estado do objeto.

> Isto é também válido no caso de funções, não apenas para métodos.

A solução da «cópia» dos valores não é 100% segura. No exemplo da classe `Student` se os cursos são representados por instâncias de uma classe `Course`, será que a cópia da lista de cursos é suficiente ?

Depende !

```python
fp = Course('Fundamentos de Programação', 'MSc')
cp = Course('Complementos de Programação', 'MSc')

s1 = Student(34444, 'Baltazar')
d = [fp, cp]
s1.setCourses2(d)
# s1 contém uma cópia de d
# podemos alterar d ?
d[0] = 'LOL'
print(s1.getCourses()[0].asString())
print(s1.getCourses()[1].asString())
# sim, não há problema
# mas... se altermos fp ?
fp.setName('YYY')
print(s1.getCourses()[0].asString())
# PROBLEMA !
```

### Solução
Não permitir que as instâncias de `Course` seja alteráveis. Para isso basta não definir setters.

> Nesta caso a classe é chamada **imutável**.

Usar estruturas imutáveis. Preferir tuples a listas. Na classe `Student` se os métodos recebem parâmetros e retornam valores de tipo tuple em vez de listas, não será possível altera-las. (quase)

> Em qualquer caso não há receita infalível para este problema em Python. A solução consiste em entender em profundidade esses mecanismos, estar atento e rigoroso na aplicação das *boas práticas de programação*.







