
# Testes unitários em python
> Thibault Langlois / FCUL / DI / 2023

## Testing
Os testes fazem parte integral da atividade de desenvolvimento de
software. Antes de publicar uma apliação convêm que esteja
covenientemente testada. Uma vez publicada a aplicação vai evoluir
(novas versões). Como assegurar que continua a funcionar como desejado
após modificações dno código ?

Os testes untários servem este propósito. A palavra «unitário» vem do
facto que se vai procurar testar cada função/metodo de forma isolada. 

## O módulo unittest
O módulo `unittest` foi originalmente inspirada pelo `JUnit`(usado em
java) e tem um mecanismo semelhante aos principais sistemas de teste
unitários em outras linguagens. 

`unittest` suporta alguns conceitos importantes de forma orientada a objetos:

1. mecanismo de teste

	O mecanismo de teste vai incluir: 
	1) a preparação para executar um ou mais testes e
	2) ações de limpeza associadas. 
	Isso pode envolver, por exemplo, criar bancos de dados
	temporários ou proxy, diretórios ou iniciar um processo de
	servidor. 

2. caso de teste (unit test)
     Um caso de teste é a unidade individual de teste. Ele verifica
     uma resposta específica a um determinado conjunto de
     entradas. `unittest` fornece uma classe base, `TestCase`, que pode
     ser usada para criar novos casos de teste. 
	 
3. conjunto de testes

     Um conjunto de testes é uma coleção de casos de teste, conjuntos
	 de testes ou ambos. É usado para agregar testes que devem ser
	 executados em conjunto. 

4. mecanismo de excução dos testes

     Um executor de teste é um componente que orquestra a execução de
     testes e fornece o resultado ao utilizador. O executor pode usar uma
     interface gráfica, uma interface textual ou retornar um valor
     especial para indicar os resultados da execução dos testes. 
	 
## Exemplo

A classe `Trotinette` representa uma trotinette numa hipotetica
aplicação de gestão de frota de trotinettes para aluger em livre
serviço. 
Neste contexto são representadas (para além da trotinette) apenas um
esboço das operações de check-in e check-out. 

```python
class Trotinette:
    def __init__(self, id, cost_per_minute):
        self.id = id
        self.rent_timestamp_start = None
        self.rent_timestamp_end = None
        self.user_id = None
        self.cost_per_minute = cost_per_minute
        self.total_benefit = 0

    def check_in(self, user_id):
        assert not self.in_use(), 'The trotinette is being used.'
        self.user_id = user_id
        self.rent_timestamp_start = datetime.now()

    def check_out(self):
        self.rent_timestamp_end = datetime.now()
        duration = self.rent_timestamp_end - self.rent_timestamp_start
        amount = self.cost_per_minute * int(round(duration.total_seconds()/60))
        self.total_benefit = self.total_benefit + amount
        self.free()

    def in_use(self):
        return self.user_id is not None

    def free(self):
        self.user_id = None

    def __str__(self):
        return str(self.id) + "_Benefit_" + str(self.total_benefit)
```

Para testar esta classe usando o módulo `unittest` deve-se criar uma
classe `TestTrotinette`, num módulo separado (`test_trotinette`): 

```python
import unittest
from datetime import datetime
from trotinette import Trotinette
import time

t1 = Trotinette(1000, 0.25)
t2 = Trotinette(1001, 0.25)

class TestTrotinetteMethods(unittest.TestCase):
```
Após importar os módulos necessários, definmos a classe que *deve
herdar a classe `unittest.TestCase`*. A classe não tem atributos logo
não será necessário definir um construtor. As varáveis `t1` e `t2`
contêm duas instâncias que vão ser usadas nos testes. Estamos a ssumir
que o contrutor funciona corretamente e não será testado.

O primeiro teste verifica o funcionamento do método `__str__()`:
```python
   def test__str__(self):
        t1 = Trotinette(1234, 0.25)
        expected = "1234_Benefit_0"
        self.assertEqual(str(t1), expected)
```
Notas: o nome do método começa com 'test', é necessário. A classe
`TestCase` disponibiliza vários métodos para realizar os testes. Neste
exemplo estamos a usar o método `assertEqual(a,b)` que compara os seus
dois parâmetros. Se não forem iguais, o test falha. 

Para correr os testes temos que acrecentar no final fo fciheiro:

```python
if __name__ == '__main__':
    unittest.main()
```

e usar:
```
> python test_trotinette.py -v -f
```
A opção `-v` (verbose) mostra o resultado de cada teste numa linha
separada a medida que estão a ser executados. A opção `-f` (failfast)
interrompe os testes quando encontrar a primeira falha (caso contrário
efetua todos os testes da classe).

```
> python test_trotinette.py -v -f
test__str__ (__main__.TestTrotinetteMethods) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Continuamos com mais testes:
```python
    def test_check_in1(self):
        date = datetime.now()
        t1.check_in(100)
        delta = t1.rent_timestamp_start - date
        self.assertTrue(delta.seconds >= 0 and delta.seconds < 5)
```
Este teste verifica se o timestamp de inicio de aluguer esta registado
na instância. Usa-se o método `assertTrue`.

O próximo teste verifica que não se pode registar uma trotinette que
já está em uso. Por isso temos que verificar que a asserção falha (que
a exceção é lançada).
```python
    def test_check_in2(self):
        with self.assertRaises(AssertionError):
            t1.check_in(100)
```
O bloco `with self.assertRaise():` permite verificar que uma exceção
foi lançada durante a execução do bloco de instruções associado. Note
que neste exemplo teria sido mais adequado criar um tipo de exceção
especifica para este problema.

O teste seginte verifica que o id do utilizador foi corretamente
inicializado:
```python
    def test_check_in3(self):
        t2.check_in(101)
        self.assertEqual(t1.user_id, 100)
```

Para testar a operação de check out temos que verificar se o tempo ed
utilização foi corretamente registado:

```python
    def test_check_out1(self):
        time.sleep(5)
        date = datetime.now()
        t1.check_out()
        duration = (date - t1.rent_timestamp_start).seconds
        self.assertTrue(abs(duration - 5) < 0.1)
```

Uma vez feito o checkout, a trotinette deve estar livre:

```python
    def test_check_out2(self):
        self.assertFalse(t1.in_use())
```

Finalmente vamos verificar que o montante do aluguer foi calculado com
especificado:
```python
    def test_check_out3(self):
        time.sleep(2*60)
        total = t2.total_benefit
        t2.check_out()
        total_after = t2.total_benefit
        duration = t2.rent_timestamp_end - t2.rent_timestamp_start
        duration = round(duration.seconds/60)
        value = t2.cost_per_minute * duration
        self.assertTrue(total_after - total == value)
```

```
> python test_trotinette.py -v -f
test__str__ (__main__.TestTrotinetteMethods) ... ok
test_check_in1 (__main__.TestTrotinetteMethods) ... ok
test_check_in2 (__main__.TestTrotinetteMethods) ... ok
test_check_in3 (__main__.TestTrotinetteMethods) ... ok
test_check_out1 (__main__.TestTrotinetteMethods) ... ok
test_check_out2 (__main__.TestTrotinetteMethods) ... ok
test_check_out3 (__main__.TestTrotinetteMethods) ... ok

----------------------------------------------------------------------
Ran 7 tests in 125.105s

OK
```

## Mais detalhes

Pode-se definir um método que será executado antes de cada teste:
```python
    def setUp(self):
        print('will run before each test.')
```
será útil definir este método para incializar um contexto no qual os
testes devem correr (inicializar instâncias, definir variáveis, criar
ficheiros etc...). 

É também possível definir um método que será executado antes de correr
os testes:

```python 
@classmethod
def setUpClass(cls):
    ...
```

O método `tearDown` é um método que será execudado a seguir a cada
teste. Será útil para repor o contexto da classe para poder correr os
restantes testes (destruir instâncias, apagar ficheiros etc...). 
```python
    def tearDown(self):
        ...
```

Finalmente o método `tearDownClass` será executado após o último
teste: 
```
@classmethod
def tearDownClass(cls):
    ...
```
Note que deve ser um método de classe.

As vezes temos os testes podem demorar a correr. Para não executar um
teste (temporiaramente) pode-se adicionar a decoração
`@unittest.skip(reason)`. Alternativas a esta anotação são:
`@unittest.skipIf(conition, reason)` e
`@unittest.skipUnless(condition, reason)`.

## Documentação

https://docs.python.org/3/library/unittest.html
