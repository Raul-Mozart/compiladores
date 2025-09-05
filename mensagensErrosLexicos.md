# Padrões de Tokens e Análise Léxica

## TOKEN_PATTERNS

### 1) Identificadores e Palavras-chave
```regex
'IDENTIFIER': '^[a-z]+(?:[A-Z][a-z0-9]*)*$'
```

### 2) Palavras-chave
```regex
\b(if|else|for|while|function|string|int|float|bool|list|var|in|class|return|and|or|not)\b
```

### 3) Operadores
```regex
(\+|\-|\*{1,2}|\/|%|==|=|<=|>=|<|>)
```

### 4) Delimitadores e Símbolos
```regex
(\{|\}|\[|\]|\(|\)|;|:|,|\\|\.|\n)
```

### 5) Números
- **Inteiros**: `^[0-9]+$`
- **Float**: `^[0-9]+\.[0-9]+$`

### 6) Strings
```regex
"(.*?)"|'(.*?)'
```

### 7) Comentários (se aplicável futuramente)
```regex
//.*$|/\*[\s\S]*?\*/
```

---

## Tipos Comuns de Ambiguidade

### Ambiguidade Identificador vs. Palavra-chave
**Problema**: A string "function" deve ser reconhecida como identificador ou palavra-chave?

**Solução**: A solução padrão é dar precedência às palavras-chave, mas isso significa que "function" não pode ser usado como nome de variável.

**Resposta**: Seguiremos com a forma padrão mencionada acima.

### Ambiguidade de Operadores
**Problema**: A sequência "++" pode ser o operador de incremento, ou dois operadores de soma consecutivos? O princípio do maior match resolve esta ambiguidade naturalmente.

**Resposta**: Está definida em TOKEN_PATTERNS.

### Ambiguidade Numérica
**Problema**: A string "3.14e+2" é claramente um número, mas e "3.14e"? E "3."? E ".5"? Cada caso requer decisão explícita na especificação.

**Resposta**: No nosso caso, será válido apenas com número antes e depois do ponto, por exemplo: `3.57`.

---

## 🔍 Estratégias de Resolução

### Princípio do Maior Match
Sempre escolha o token mais longo possível. Se "123" e "123abc" são ambos reconhecíveis por padrões diferentes, escolha o match mais longo.

### Ordem de Precedência
Quando dois padrões reconhecem a mesma string, use uma ordem predefinida. Palavras-chave têm precedência sobre identificadores.

### Contexto Léxico
Em alguns casos, o contexto pode ajudar a resolver ambiguidades, embora isso deva ser usado com moderação para manter a simplicidade do analisador léxico.

# Mensagens de erro para usuários

### Caractere inválido
```txt
LEX001 [L8:12] Caractere inválido: '@'.
x = 10 @ 20
       ^
Erro: '@' não pertence ao alfabeto (Σ) nem a nenhuma ER de token definida.
```

---

### String não terminada
```txt
LEX002 [L3:5] String não terminada.
nome = "Maria
        ^
Erro: feche o delimitador para reconhecer a cadeia na linguagem de strings (ER).
```

---

### Número malformado
```txt
LEX003 [L5:9] Número malformado: '12.3.4'.
num = 12.3.4
          ^
Erro: a expressão regular do número permite no máximo um ponto decimal.
```

### Comentário de bloco não fechado
```txt
LEX004 [L7:1] Comentário de bloco não terminado.
/* este é um comentário
^
Erro: feche o comentário com '*/' para pertencer à linguagem de comentários de bloco.
```
