# Uma calculadora que usa a notação polaca inversa

## A notação Polaca inversa (RPN)
Existem duas maneiras de introduzir expressões aritméticas numa calculadora:

Usando a notação «infix», por exemplo:
```
    (3 + 5) * (5 - 3 * 4)
```
onde os operandos aparecem à esquerda e à direita do operador. Esta 
notação tem a vantagem de ser «natural», é a notação usada em
matemática. Tem um defeito: obriga a definir a precedência entre
os operadores. Por exemplo, a expressão `(5 - 3 * 4)` deve ser
interpretada como `((5 - 3) * 4) = 8` ou `(5 - (3 * 4)) = -7`) ?
Um outro defeito é que, devido ao uso dos parêntesis, a análise da expressão (pelo computador) é mais difícil.
Usando a notação Polaca inversa, a mesma expressão é calculada assim:
```
    3 5 + 5 3 4 * - *
```
![](HP41CV.jpg)

Os operandos precedem os operadores. Esta notação tem o defeito de não
ser muito legível por uma pessoa que não está habituada mas,
em contrapartida, é facil escrever programas para lidar com
ela. No exemplo anterior, o mecanismo de avaliação é o
seguinte:

	- Os operandos são guardados à medida que são encontrados. O 3 e o 5 são portanto os dois primeiros operandos encontrados.
    - Quando um operador é encontrado, no nosso exemplo o +, os dois últimos operandos armazenados são tirados, a operação é efectuada e o resultado é guardado no lugar dos operandos.
        Aqui está a sequência dos valores guardados durante a avaliação da expressão `3 5 + 5 3 4 * - *` :
```
        3 5
        8
        8 5 3 4
        8 5 12
        8 -7
        -56
```

O algoritmo constiste em:
ler cada token na entrada, considerando o espaço como separador.

 - caso o token corresponder a um número, coloca-lo numa pilha.
 - caso o token corresponder a uma operção:
     1. remover da pilha o número de operandos necessários,
     2. calcular o resultado da operação
     3. colocar o resultado na pilha
 - repetir até não haver mais tokens na entrada.
 
 ## Implementação
 Tem que usar a classe `Stack` fornecida completando o código cada vez
 aque achar necessário.
 
 Qualquer que seja o input do utilizador, o programa nunca deve
 terminar com um erro.
 
 Deve usar exceções para lidar com os eventuais erros.
 O ficheiro `calc.py` é um esboço de solução.
 Os operadores que devem ser implemntados são os operadores
 aritméticos, as funções trigonométricas, `exp`, `log` e `sqrt`.
 
