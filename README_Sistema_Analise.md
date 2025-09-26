# 🔬 Sistema de Análise Léxica - Linguagem Proposta

Este sistema integra autômatos DFA (Deterministic Finite Automaton) com análise léxica de uma linguagem de programação proposta, baseada nas especificações do repositório [github.com/Raul-Mozart/compiladores](https://github.com/Raul-Mozart/compiladores).

## 🚀 GUIA RÁPIDO - Como Executar

### ▶️ Opções de Execução

#### Opção 1: Menu Principal Completo
```bash
python main.py
```
- Escolha entre autômatos básicos, análise léxica ou ambos
- Interface completa com todas as funcionalidades

#### Opção 2: Análise Léxica Direta  
```bash
python teste_analise_lexica.py
```
- Acesso direto ao analisador léxico
- Menu interativo especializado

#### Opção 3: Teste Automatizado
```bash
python teste_automatizado.py
```
- Executa todos os testes automaticamente
- Verifica funcionamento do sistema

### 📝 Como Testar Seus Próprios Códigos

#### Método 1: Arquivo .txt
1. Crie um arquivo `.txt` com código na linguagem proposta
2. Execute: `python main.py` → opção 2 → opção 1
3. Digite o caminho do arquivo
4. Veja o relatório completo

#### Método 2: Código Inline
1. Execute: `python main.py` → opção 2 → opção 2  
2. Digite seu código linha por linha
3. Pressione Enter em linha vazia para finalizar
4. Veja tokens encontrados em tempo real

#### Método 3: Arquivo de Exemplo
1. Execute: `python main.py` → opção 2 → opção 3
2. Sistema cria `codigo_exemplo.txt` automaticamente
3. Processe o exemplo para ver todas as funcionalidades

## 📋 Funcionalidades

### 🔧 Autômatos Básicos (Regex → DFA)
- Compilação de expressões regulares para autômatos DFA
- Teste de padrões como números, identificadores, operadores
- Demonstração do funcionamento interno dos autômatos

### 🔬 Análise Léxica da Linguagem
- Reconhecimento de tokens da linguagem proposta
- Processamento de arquivos de código
- Interface interativa para teste
- Relatórios detalhados de análise

## 🎯 Tokens Reconhecidos

### Palavras-chave
```
if, else, for, while, function, var, in, class, return,
string, int, float, bool, list, and, or, not, private,
public, mutable, inherits, new
```

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`, `%`
- **Relacionais**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Atribuição**: `=`
- **Lógicos**: `and`, `or`, `not`
- **Range**: `..`

### Literais
- **Inteiros**: `123`, `0`, `42`
- **Ponto flutuante**: `3.14`, `1.5e10`, `2.3e-5`
- **Strings**: `"hello"`, `"texto com \"aspas\""`, `"linha1\nlinha2"`
- **Booleanos**: `true`, `false`

### Delimitadores
- **Parênteses**: `(`, `)`
- **Chaves**: `{`, `}`
- **Colchetes**: `[`, `]`
- **Pontuação**: `;`, `,`, `.`, `:`

## 📋 Exemplo de Código Válido

```javascript
// Comentário na linguagem
var int idade as 25;
var string nome as "João";

function bool ehMaior(idade) {
    if (idade >= 18) {
        return true;
    } else {
        return false;
    }
}

print("Resultado: " + ehMaior(idade));
```

## � Saída Esperada

```
📊 Total de tokens: 45
📝 Linhas de código: 12

📈 ESTATÍSTICAS POR TIPO DE TOKEN:
IDENTIFIER     :    8 ocorrências  
KEYWORD        :    7 ocorrências
STRING_LITERAL :    4 ocorrências
INT_LITERAL    :    3 ocorrências
RELOP          :    2 ocorrências
```

## ⚡ Dicas Rápidas

- 📁 **Arquivos de teste**: Use extensão `.txt` 
- 🔄 **Relatórios**: Salvos automaticamente em `relatorio_analise.txt`
- ❌ **Erros**: Tokens desconhecidos são marcados como `UNKNOWN`
- 🎨 **Formatação**: Use encoding UTF-8 para caracteres especiais

## �📝 Exemplos de Uso

### 1. Testando um Arquivo
O sistema inclui um arquivo de exemplo (`codigo_exemplo.txt`) que demonstra todos os tipos de tokens:

```
// Exemplo de código na linguagem
var int idade as 25;
var string nome as "João";

function bool ehMaiorIdade(idade) {
    if (idade >= 18) {
        return true;
    } else {
        return false;
    }
}
```

### 2. Interface Interativa
No menu da análise léxica:
- **Opção 1**: Processa arquivos `.txt` com código
- **Opção 2**: Permite digitar código diretamente
- **Opção 3**: Cria arquivo de exemplo automaticamente
- **Opção 4**: Testa tokens individuais

### 3. Relatórios Gerados
O sistema gera relatórios detalhados incluindo:
- Lista completa de tokens encontrados
- Estatísticas por tipo de token
- Posição (linha/coluna) de cada token
- Contagem total e métricas do código

## 🏗️ Arquitetura do Sistema

```
├── main.py                    # Menu principal e testes básicos
├── teste_analise_lexica.py    # Sistema completo de análise léxica
├── codigo_exemplo.txt         # Arquivo de exemplo da linguagem
├── automatos/                 # Módulos dos autômatos
│   ├── __init__.py
│   ├── compilador.py          # Compilação regex → DFA
│   ├── constantes.py          # Tokens e constantes
│   ├── parser.py              # Conversão para notação postfix
│   ├── subconjuntos.py        # Algoritmo de subconjuntos
│   ├── thompson.py            # Construção de Thompson
│   └── tokenizer.py           # Tokenização de regex
└── README_Sistema_Analise.md  # Esta documentação
```

## 🔍 Funcionamento Interno

### 1. Compilação de Tokens
Cada tipo de token é definido como uma expressão regular e compilado para um autômato DFA:

```python
tokens_linguagem = {
    "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
    "INT_LITERAL": r"\d+",
    "FLOAT_LITERAL": r"\d+\.\d+([eE][+-]?\d+)?",
    # ... outros tokens
}
```

### 2. Análise Léxica
O processo de análise segue estes passos:
1. **Tokenização**: Quebra o código em tokens usando os DFAs
2. **Classificação**: Identifica o tipo de cada token
3. **Posicionamento**: Rastreia linha e coluna de cada token
4. **Validação**: Verifica tokens válidos/inválidos

### 3. Geração de Relatórios
Os relatórios incluem:
- Análise estatística completa
- Lista detalhada de todos os tokens
- Identificação de tokens desconhecidos
- Métricas do código analisado

## 🛠️ Personalização

### Adicionando Novos Tokens
Para adicionar um novo tipo de token:

1. **Defina a regex** em `AnalisadorLexico.__init__()`:
```python
self.tokens_linguagem["NOVO_TOKEN"] = r"sua_regex_aqui"
```

2. **O sistema automaticamente**:
   - Compila a regex para DFA
   - Inclui o token na análise
   - Adiciona às estatísticas dos relatórios

### Modificando Tokens Existentes
Edite as expressões regulares em `tokens_linguagem` para ajustar o reconhecimento de padrões.

## 🎯 Casos de Teste

### Tokens Válidos
- ✅ Identificadores: `variavel`, `_private`, `contador1`
- ✅ Números: `123`, `3.14`, `1.5e10`
- ✅ Strings: `"texto"`, `"com \"aspas\""`
- ✅ Palavras-chave: `if`, `function`, `return`

### Tokens Inválidos (Detectados pelo Sistema)
- ❌ Identificador inválido: `9variavel` (começa com número)
- ❌ String malformada: `"sem fechamento`
- ❌ Operador inexistente: `===`

## 📊 Saída de Exemplo

```
📋 RELATÓRIO DE ANÁLISE LÉXICA
=====================================
📁 Arquivo: codigo_exemplo.txt
📊 Total de tokens: 157
📝 Linhas de código: 45

📈 ESTATÍSTICAS POR TIPO DE TOKEN:
KEYWORD        :   23 ocorrências
IDENTIFIER     :   31 ocorrências
INT_LITERAL    :   15 ocorrências
STRING_LITERAL :    8 ocorrências
LBRACE         :    6 ocorrências
RBRACE         :    6 ocorrências
```

## 🤝 Contribuição

Este sistema foi desenvolvido para demonstrar a aplicação prática de:
- Teoria dos autômatos
- Análise léxica
- Compilação de expressões regulares
- Processamento de linguagens formais

Para contribuir, considere:
- Adicionar novos tipos de tokens
- Melhorar a detecção de erros
- Expandir os relatórios de análise
- Otimizar o desempenho dos autômatos

## 📚 Referências

- Repositório base: [github.com/Raul-Mozart/compiladores](https://github.com/Raul-Mozart/compiladores)
- Especificação da linguagem: Documentos `.md` do repositório
- Teoria dos autômatos: Implementação usando algoritmos clássicos (Thompson, subconjuntos)

---

**Sistema pronto! Execute `python main.py` para começar** 🚀

**Desenvolvido com ❤️ usando Python e teoria dos autômatos**