# Programação Orientada Objetos (2/3)
> Thibault Langlois / FCUL / DI /  2022-2023

## Course
Defina a classe `Course` referida na aula teórica.

## Anúncios

Defina, para além da classe `Ad` as classes `CarAd` e `RealEstateAd` especializadas em anúncios para caros e para casas.

Decide se vai usar uma relação de herança entre as classes.

Escreva um programa de teste (num módulo separado) que cria um anúncio de cada tipo e imprime os valores no ecrã. Poderá ser útil definir um método que retorna esses valores sob-forma de uma string.

Escreva um método nas classes de anúncios que recebem um ficheiro já aberto e escreve os valores dos anúncios para esse ficheiro.

```python
write(self, f):
    # ....
```

Incluir no programa de teste as instruções para testar esta funcionalidade.

```python
with open(filename, 'w') as f:
    # ....
```

## Shapes
O enunciado está disponível na página da disciplina (formato PDF).

