## Conjuntos

### Variáveis (Não-terminais)
```
V = {
  Program, DeclarationsBlock, Declaration, VariableDeclaration,
  FunctionDeclaration, ClassDeclaration, ContractDeclaration, CommandsBlock,
  Command, ConditionalCommand, LoopCommand, AssignmentCommand,
  WriteCommand, Expression, LogicalExpression, RelationalExpression,
  ArithmeticExpression, Term, Factor, ParametersList, ArgumentsList, Type
}
```

### Terminais
```
T = {
  if, else, else if, for, while, function, string, int, float, bool, list,
  var, in, class, return, +, -, *, /, %, and, or, <, >, <=, >=, =, ==,
  {, }, [, ], (, ), ., ,, ;, :, \n, \, not, private, public
}
```

### Símbolo Inicial
```
S = Program
```

---

## Regras Fundamentais da Linguagem

```
Program → DeclarationsBlock MainCommandsBlock

DeclarationsBlock → Declaration DeclarationsBlock | ε
Declaration → VariableDeclaration | FunctionDeclaration | ClassDeclaration

VariableDeclaration → var Type literal as identifier 
                    | var mutable Type literal as identifier
Type → int | float | string | bool

FunctionDeclaration → function Type identifier ( ParametersList ) CommandsBlock return
ClassDeclaration → class identifier ClassBlock return
                 | class identifier inherits identifier ClassBlock return

CommandsBlock → Command CommandsBlock | ε
Command → AssignmentCommand | ConditionalCommand | LoopCommand | WriteCommand
MainCommandsBlock → Command MainCommandsBlock | ε

ConditionalCommand → if Expression { CommandsBlock } return
                   | if Expression { CommandsBlock } else { CommandsBlock } return

LoopCommand → while Expression { CommandsBlock } return
            | for Type identifier in literal .. literal { CommandsBlock } return

WriteCommand → print ArgumentsList

Expression → LogicalExpression
LogicalExpression → RelationalExpression
                  | LogicalExpression and RelationalExpression
                  | LogicalExpression or RelationalExpression
                  | not LogicalExpression

RelationalExpression → ArithmeticExpression
                      | ArithmeticExpression == ArithmeticExpression
                      | ArithmeticExpression != ArithmeticExpression
                      | ArithmeticExpression > ArithmeticExpression
                      | ArithmeticExpression < ArithmeticExpression
                      | ArithmeticExpression >= ArithmeticExpression
                      | ArithmeticExpression <= ArithmeticExpression

ArithmeticExpression → Term
                     | ArithmeticExpression + Term
                     | ArithmeticExpression - Term

Term → Factor
     | Term * Factor
     | Term / Factor
     | Term % Factor

Factor → identifier
       | int_literal
       | float_literal
       | string_literal
       | bool_literal
       | ( Expression )
       | identifier ( ArgumentsList )
```

---

## Classificação na Hierarquia de Chomsky

**Tipo da gramática:** **Tipo 2 (Livre de Contexto)**

### Justificativa
- Todas as produções têm a forma **A → α** (lado esquerdo com apenas um não-terminal).  
  Exemplo:  
  ```
  ConditionalCommand → if Expression { CommandsBlock }
  ```
- A gramática consegue **"lembrar" estruturas**, como if/else e expressões recursivas.

### Verificação
- ❌ **Não é Tipo 3 (Regular):** não consegue reter contexto.  
- ⚠️ **Parcialmente Tipo 1 (Sensível ao contexto):** linguagem é tipada.  
  - Ex.: verificar se `int x = 5;` é válido, mas `int x = "hello";` não é.  
- ❌ **Não é Tipo 0 (Irrestrita):** possui estruturação rígida.
   
 

### Exemplo de derivação:

#### Código:  
function parImpar(num) { if (num % 2 \== 0\) { return “É par”; } else { return “É impar” }

#### Derivação: 
``` 
Programa  
⇒ BlocoDeclarações  
⇒ Declaração BlocoDeclarações  
⇒ DeclaraçãoFunção BlocoDeclarações  
⇒ function Type identificador ( ParametersList ) BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( ParametersList ) BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( identifier ) BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( num ) BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( num ) Comando BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( num ) ComandoCondicional BlocoComandos return BlocoDeclarações  
⇒ function string parImpar ( num ) if Expressão { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if ExpressãoLógica { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if ExpressãoRelacional { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if ExpressãoAritmética \== ExpressãoAritmética { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if Termo \== Termo { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if Fator % Fator \== Fator { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if identificador % literal\_inteiro \== literal\_inteiro { BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { BlocoComandos } else { BlocoComandos } return BlocoDeclarações

\-- bloco 'then'  
⇒ function string parImpar ( num ) if num % 2 \== 0 { Comando BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { ReturnCommand BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return string\_literal ; BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; BlocoComandos } else { BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; ε } else { BlocoComandos } return BlocoDeclarações

\-- bloco 'else'  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; } else { Comando BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; } else { ReturnCommand BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; } else { return string\_literal ; BlocoComandos } return BlocoDeclarações  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; } else { return "É impar" ; ε } return BlocoDeclarações

\-- finalizar função e programa (declarações e comandos vazios)  
⇒ function string parImpar ( num ) if num % 2 \== 0 { return "É par" ; } else { return "É impar" ; } return  
⇒ (Programa concreto com a função parImpar)
```

## Análise de ambiguidades potenciais e estratégias de resolução

Expressões aritméticas (precedência/associatividade)  
Ex.: id \+ id \* id — pode ser interpretado como (id \+ id) \* id ou id \+ (id \* id) se a gramática não fixa precedência entre \+/- e \*///%.

Expressões lógicas (and / or / not)  
Ordem entre and e or e escopo do not pode ser ambíguo: a or b and c deve ser (a) or (b and c) normalmente, mas a gramática precisa deixar isso explícito.

A estratégia para resolver ambos os exemplos seria colocar os parenteses na expressão que possui prioridade.  
