# Programação por contratos (1/1)
> Thibault Langlois / FCUL / DI /  2021-2023

Uma classe fornece, através dos seus métodos públicos, um
serviço. Geralmente usa serviços de outras classes, por exemplo
classes da biblioteca do Python. Existe portanto uma **relação
cliente - fornecedor** entre classes. Quando define uma classe, está a
conceber um serviço que será usado por outras classes e a sua classe,
por sua vez, usa o serviços de outras classes. Uma classe pode
portanto ser um fornecedor e um cliente ao mesmo tempo. 

Muitas vezes os métodos públicos de uma classe funcionam em
determinadas condições: 

> Os valores passados como parâmetros devem pertencer a um conjunto de valores válidos. (Ex.: datas, horas, idades etc...)
    
> É necessário chamar outro método antes. (Ex.: para reservar o recurso, abrir um ficheiro, estabelecer uma ligação etc...)

## Programação defensiva

Uma solução é incluir no código do método instruções que vão testar os valores dos argumentos. Por exemplo, o método seguinte é suposto alterar o valor das horas numa instância da classe Date: 

```python
def setHour(self, h):
    if h >= 0 and h < 24:
        self.hour = h
```
Esta solução apresenta vários defeitos: 

1. não é claro o valor que fica no atributo quando um valor inválido é
   fornecido. De modo geral é difícil decidir o que deve ser feito
   quando uma situação anómala é encontrada. 

2. a verificação sempre será efetuada, mesmo quando não faz sentido
   (neste exemplo, podemos imaginar uma situação onde o valor
   fornecido é sempre válido, porque é verificado antes ao nível da
   interface gráfica). 

3. a verificação pode ter um custo computacional elevado.

4. o código que efetua a validação pode ser baste mais complexo do que
   o código do método. 

Esta abordagem onde é feita uma validação no início do método é
chamada «**programação defensiva**». 

> Deve-se **evitar** a **programação defensiva**. As únicas situações onde é uma abordagem aceitável é quando os valores são introduzidos por um utilizador (humano).

## Estabelecer um **contrato**

Em reação à abordagem defensiva foi inventada a programação por
contratos. A gestão das relações entre componentes de software (entre
cliente e servidor) são inspiradas das relações
comerciais. Formaliza-se um contrato entre cliente e fornecedor :

* as **pré-condições** especificam as condições necessárias para que o
serviço seja efetuado,  

* as **pós-condições** estabelecem o que deve resultar do serviço
  (resultado, alteração do estado do objeto etc...) 

Os contratos devem fazer parte da documentação da classe. São portanto
  incluídos nos comentários do método. Dois tags são usados:  

* `Requires`: permite especificar as pre-condições
* `Ensures` : indica as pós-condições do método: 

```python
    def setHour(self, h):
        """
        setHour: modifies the hour of the date

        Args:
            h (int): the new value for the hour
        
        Requires: h in range(24)

        Ensures: self.getHour() == h
        """
        self.hour = h
```

Os contratos fazem parte da documentação, podem estar escritos em
lingua natural (inglês ou português conforme o resto da
documentação). Pode-se optar por uma descrição um pouco mais formal
como no exemplo acima.

No exemplo seguinte, estamos a usar na definição do contrato do
construtor um método da classe.

```python
    def __init__(self,y,m,d):
        """
        __init__ Constructor for Date class

        Args:
            y (int): the year
            m (int): the month number
            d (int): the day of the month

        Requires: 
            Date.isValidDate(y,m,d)
        """
        self.year = y
        self.month = m
        self.day = d

    @staticmethod
    def isValidDate(y, m, d):
        # date verification
```
É uma boa opção. Pode acontecer que a pre-condição seja
complexa. Imagine por exemplo o caso do constructor da classe
`Date`. Queremos responsabilizar o cliente por fornecer uma data
válida. A especificação de uma data válida não é trivial (temos de ter
em conta os anos bissextos). Não queremos fazer programação defensiva
(verificando em cada chamada ao constructor os valores de entrada) mas
podemos facilitar a vida ao cliente fornecendo um método que faz esta
verificação.

Note que o método `isValidDate` é static. Note também que não há
pre-condições, não faria sentido dado que o objetivo do método é
determinar se os valores de entrada estão válidos. 

> **Princípio de não redundância**. 
Em nenhuma circunstância um método deve testar as suas pré-condições.

> **Quebra de contrato**. A violação de uma pré-condição é sinal de
> erro na parte do cliente. A violação de uma pós-condição corresponde
> a um erro no fornecedor. 

