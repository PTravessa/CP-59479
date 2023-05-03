## Colocar o repositório local no servidor remoto

As instruções anteriores (cf última aula) correram como indicado porque começamos com um repositório novo. Iremos ver mais à frente que o comando `git push` pode não resultar logo. 
Se o repositório estiver partilhado com outra(s) pessoa(s), um colega pode ter feito um commit antes de si. Neste caso o comando `git push` vai falhar, o seu commit será rejeitado (reject). 

O passo a seguir para resolver a situação é trazer a última versão do repositório (que está no servidor remoto) para o seu computador. 

## Copiar o repositório remoto para o local

Uma vez que um repositório está armazenado num computador remoto podemos passar a trabalhar em qualquer computador. Há duas situações :

1. O repositório ainda não existe neste computador. Neste caso deve-se usar o comando `git clone` seguido do URL do repositório. Este comando já foi apresentado na última aula. 
2. O repositório já existe no computador. Neste caso quer *atualizar* o repositório local.
Neste caso o comando `git pull` deve ser usado. Este passo é necessário antes de poder "empurrar" o seu repositório para o servidor remoto. 

A situação pode estar um pouco mais complexa se :
- tiver modificado algum ficheiro da sua área de trabalho
- estiver a partilhar o repositório com outras pessoas.

Se você ou o seu colega tiver modificado o mesmo ficheiro, pode acontecer um *conflito*.

### Porque?
O comando `git pull` realiza dois passos :
1. `git fetch` que faz uma cópia local do repositório remoto para uma área escondida (na pasta `. git`).
2. `git merge` que funde o seu último commit com o commit vindo do repositório remoto.

O git usa um algoritmo apropriado para fundir os repositórios. Os ficheiros criados de ambos os lados estão adicionados tal como os ficheiros que foram alterados de um lado *ou* de outro. Caso um ficheiro foi modificado de ambos os lados, há duas hipóteses :

A- as modificações estão distantes e o algoritmo vai as incluir na nova versão do ficheiro ou 
B- se forem próximas vai desistir e assinalar o conflito.

No caso A o algoritmo conseguiu conciliar os dois commit e o resultado da operação 'merge' será um novo commit. O git vai pedir-lhe para introduzir uma mensagem a associar ao commit. Pode optar por usar a mensagem por omissão. 

No caso B, deve editar o ficheiro onde ocorreram os conflitos e escolher a versão que pretende que seja usada. 

Concluir o commit com o comando XXX. 

Nesta fase o comando `git push` foi concluído. Se a sua intenção era publicar o seu trabalho no repositório remoto, ainda tem que repetir o comando `git push` que, desta vez não deve falhar. 

## Ramos

O git permite o desenvolvimento paralelo. Isto significa que pode manter várias versões dos ficheiros. Está facilidade pode ser usada por exemplo para 

- isolar o seu trabalho do dos seus colegas de equipa e minorar os eventuais conflitos ou 
- desenvolver alguns aspectos do projeto mantendo uma versão estável e cujo funcionamento está comprovado. 

Todos os repositórios têm pelo menos um ramo: o ramo principal, chamado "master" ou "main". 

Em qualquer altura um repositório apresenta o conteúdo de um ramo na área de trabalho. Para ver qual é o ramo corrente pode usar o comando `git branch`:

```
$ git branch 
master *
```

O comando permite também criar um ramo:

```
$ git branch archibaldo
```
Cria um ramo chamado archibaldo.
```
$ git branch 
master *
archibaldo
```

O * assinala o ramo corrente. Para mudar de ramo deve usar o comando `git checkout` seguido do nome do ramo.

```
$ git checkout archibaldo
$ git branch
master 
archibaldo *
```

O novo ramo contém inicialmente os ficheiros do ramo principal. Podemos modifica-los e memorizar as alterações numa sequência de commits. Os commits pertencem ao ramo corrente.

Para voltar a trabalhar no ramo principal podemos usar novamente o comando `git checkout master`.

> É necessário no entanto assegurar que o repositório está "limpo" antes de fazer a mudança de ramo.

> Um repositório está limpo se não houver nenhuma modificação ainda não inserida num commit. Basta usar o comando `git status`.

Conforme as organizações várias convenções de trabalho (workflow) podem ser adoptadas para a gestão dos ramos.

Os ramos podem ser usados para desenvolver novas características do projecto, corrijir bugs ou para separar o trabalho de pessoas ou equipas.

Os ramos podem estar definidos apenas localmente ou estar espelhados no repositório remoto.

Para empurrar um ramo local para o remoto deve usar o comando `git push --set-upstream origin <your branch name>` onde "origin" representa o repositório remoto.

### Fundir ramos

Uma vez terminado o trabalho planeado num certo ramo vamos querer publicá-lo no ramo principal. Para este efeito temos que :

1. Verificar que o nosso ramo está limpo (`git status`) 
2. Mudar para o ramo "destino" (para o qual queremos publicar as alterações), por exemplo o ramo master (`git checkout master`). 
3. Fundir o ramo pretendido. Por exemplo `git merge archibaldo`
4. Caso ocorrer algum conflito, resolvê-los. 


