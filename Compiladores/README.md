# Compilador de Expressões Regulares para Autômatos

Um compilador completo que converte expressões regulares em autômatos finitos determinísticos (DFA), implementado em Python.

## Estrutura do Projeto

```
Compiladores/
├── automatos/              # Pacote principal
│   ├── __init__.py           # Interface do pacote
│   ├── constantes.py         # Caracteres e tokens comuns
│   ├── estruturas.py         # Classes NFA, DFA, EstadoNFA
│   ├── tokenizer.py          # Análise léxica
│   ├── parser.py             # Conversão para postfix
│   ├── thompson.py           # Construção de NFA
│   ├── subconjuntos.py       # Conversão NFA → DFA
│   └── compilador.py         # Função principal
├── main.py                   # Exemplos e testes
├── automato.py              # Arquivo original (monolítico)
└── README.md                # Este arquivo
```

## Como Usar

### Uso Básico
```python
from automatos import compile_regex_to_dfa

# Compila regex em autômato
dfa = compile_regex_to_dfa(r"\d+")  # números

# Testa strings
print(dfa.accepts("123"))    # True
print(dfa.accepts("abc"))    # False
```

### Executar Testes
```bash
python main.py
```

## Funcionalidades

### Operadores Suportados
- **Literais**: `a`, `b`, `1`, etc.
- **Escapes**: `\d` (dígitos), `\w` (alfanuméricos), `\s` (espaços)
- **Classes**: `[abc]`, `[0-9]`, `[^a]` (negação)
- **Operadores**: `|` (ou), `*` (zero+), `+` (um+), `?` (opcional)
- **Parênteses**: `(ab)*`
- **Ponto**: `.` (qualquer caractere)

### Exemplos de Regex
```python
compile_regex_to_dfa(r"[A-Za-z_]\w*")     # Identificadores
compile_regex_to_dfa(r"\d+")              # Números inteiros
compile_regex_to_dfa(r"\d+\.\d+")         # Números decimais
compile_regex_to_dfa(r"(ab)*")            # Zero ou mais "ab"
compile_regex_to_dfa(r"[01]+")            # Números binários
```

## Como Funciona

### Pipeline de Compilação
1. **Tokenização**: Quebra regex em tokens
2. **Parser**: Converte para notação postfix
3. **Thompson**: Constrói NFA (não-determinístico)
4. **Subconjuntos**: Converte NFA → DFA (determinístico)

### Exemplo de Processamento
```
Regex: "ab*"
↓
Tokens: ['a', 'b', '*']
↓
Postfix: ['a', 'b', '*', '.']
↓
NFA: Estados conectados por epsilon
↓
DFA: Máquina determinística final
```

## Módulos

| Módulo | Responsabilidade |
|--------|------------------|
| `constantes.py` | Caracteres ASCII e tokens comuns |
| `estruturas.py` | Classes para estados e autômatos |
| `tokenizer.py` | Análise léxica de regex |
| `parser.py` | Conversão para notação postfix |
| `thompson.py` | Construção de NFA |
| `subconjuntos.py` | Algoritmo de construção de subconjuntos |
| `compilador.py` | Orquestração do pipeline |

## Tokens Pré-definidos

O sistema inclui tokens comuns para análise léxica:

- **IDENT**: `[A-Za-z_][A-Za-z0-9_]*` (identificadores)
- **INT**: `\d+` (números inteiros)
- **FLOAT**: `\d+\.\d+` (números decimais)
- **STRING**: `"(\\.|[^"])*"` (strings com escapes)
- **OP**: `==|!=|<=|>=|...` (operadores)
- **WS**: `[ \t\n\r]+` (espaços em branco)

## Exemplos de Saída

```
COMPILADOR DE EXPRESSÕES REGULARES PARA AUTÔMATOS
============================================================

TESTANDO TOKENS COMUNS:
✅ IDENT : '[A-Za-z_][A-Za-z0-9_]*' → 3 estados no DFA
✅ INT   : '\d+' → 2 estados no DFA
✅ FLOAT : '\d+\.\d+' → 4 estados no DFA

IDENT:
  'abc' → ✅ ACEITA
  '_var1' → ✅ ACEITA
  '9bad' → ❌ REJEITA
```

## Estados do Autômato

- **Menos estados** = máquina mais eficiente
- **Estado inicial**: onde começa a leitura
- **Estados finais**: onde a string é aceita

## Casos de Uso

- **Analisadores léxicos** para compiladores
- **Validação de entrada** (emails, números, etc.)
- **Matching de padrões** em texto
- **Estudo de autômatos** e teoria da computação

## Referências

- Algoritmo de Thompson para construção de NFA
- Algoritmo Shunting-yard para parsing
- Construção de subconjuntos para NFA→DFA
- Teoria de autômatos finitos