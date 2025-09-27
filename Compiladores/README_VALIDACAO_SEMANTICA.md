# 🔬 Sistema de Análise Léxica e Semântica

## ✨ Novas Funcionalidades Implementadas

Este sistema agora inclui **validação semântica básica** além da análise léxica, especificamente para verificar **compatibilidade de tipos** em declarações de variáveis.

### 🎯 Objetivo Principal

Detectar erros semânticos como:
- `var int idade as b;` ❌ **ERRO**: `b` é um identificador, não um literal inteiro
- `var float altura as nome;` ❌ **ERRO**: `nome` é identificador, não literal float
- `var string texto as 123;` ❌ **ERRO**: `123` é inteiro, não string

Enquanto aceita declarações válidas:
- `var int idade as 25;` ✅ **VÁLIDO**: literal inteiro para tipo int
- `var float altura as 1.75;` ✅ **VÁLIDO**: literal float para tipo float
- `var string nome as "João";` ✅ **VÁLIDO**: literal string para tipo string

## 🏗️ Arquitetura da Solução

### 1. Classe `ValidadorSemantico`
- **Responsabilidade**: Verificar compatibilidade entre tipos declarados e valores atribuídos
- **Métodos principais**:
  - `eh_literal_valido_para_tipo()`: Verifica se um token é compatível com um tipo
  - `validar_declaracao_variavel()`: Valida declarações seguindo a gramática: `var Type identificador as valor`
  - `validar_tokens()`: Processa lista completa de tokens

### 2. Classe `AnalisadorLexico` (Atualizada)
- **Nova funcionalidade**: Integração com validador semântico
- **Método novo**: `processar_codigo_completo()` - faz análise léxica + semântica
- **Token atualizado**: Adicionado 'as' como palavra-chave

### 3. Tipos de Erro Detectados

#### Erros Léxicos (já existiam):
- Caracteres inválidos
- Strings não terminadas
- Números malformados

#### Erros Semânticos (NOVO):
- **TIPO_INCOMPATIVEL**: Valor não compatível com tipo declarado
- **DECLARACAO_INCOMPLETA**: Declaração de variável malformada

## 📋 Gramática Seguida

Baseado em `gramatica_formal.md`:
```
VariableDeclaration → var Type literal as identifier
Type → int | float | string | bool | list
```

## 🧪 Como Testar

### Opção 1: Menu Interativo
```bash
python teste_analise_lexica.py
```
Escolha a opção **5** para testar declarações específicas.

### Opção 2: Arquivo de Demonstração
Use o arquivo `demo_validacao_semantica.py` que inclui mocks para testar sem dependências.

### Opção 3: Arquivo de Teste
Analise o arquivo `teste_semantico_exemplo.txt` que contém casos válidos e inválidos.

## 🔍 Casos de Teste Implementados

### ✅ Casos Válidos:
```javascript
var int idade as 25;
var float altura as 1.75;
var string nome as "João Silva";
var bool ativo as true;
var float numero as 42;  // int promovido para float
```

### ❌ Casos que Geram Erro Semântico:
```javascript
var int idade as b;          // identificador em vez de literal int
var float altura as nome;    // identificador em vez de literal float
var string texto as 123;     // literal int em vez de string
var bool flag as "false";    // string em vez de bool literal
var int valor as 3.14;       // float em vez de int
```

## 📊 Formato de Saída

O relatório agora inclui:
- ✅ Status da análise (OK/ERROS ENCONTRADOS)
- 🚫 Erros léxicos (se houver)
- ⚠️ Erros semânticos (se houver)
- 📈 Estatísticas de tokens
- 🔍 Lista detalhada de tokens (apenas se análise OK)

### Exemplo de Erro Semântico:
```
⚠️  ERROS SEMÂNTICOS ENCONTRADOS:
--------------------------------------------------
  1. [1:20] TIPO_INCOMPATIVEL
     Tipo incompatível: variável 'idade' declarada como 'int' mas recebeu identificador 'b' (esperado literal int)
     Contexto: var int idade as b
```

## 🚀 Próximos Passos Possíveis

1. **Validação de escopo**: Verificar se identificadores foram declarados
2. **Validação de funções**: Verificar tipos de parâmetros e retorno
3. **Validação de expressões**: Verificar compatibilidade em operações aritméticas
4. **Validação de arrays**: Verificar tipos dos elementos em listas

## 📝 Arquivos Modificados/Criados

- ✏️ **Modificado**: `teste_analise_lexica.py` - Adicionada validação semântica
- 🆕 **Criado**: `demo_validacao_semantica.py` - Script de demonstração
- 🆕 **Criado**: `teste_semantico_exemplo.txt` - Arquivo com casos de teste
- 🆕 **Criado**: `README_VALIDACAO_SEMANTICA.md` - Este arquivo

---

## 💡 Implementação Baseada na Gramática Formal

A implementação segue rigorosamente a gramática especificada em `gramatica_formal.md`, especificamente:

- **Terminais verificados**: `var`, tipos (`int`, `float`, `string`, `bool`), `as`
- **Produção implementada**: `VariableDeclaration → var Type literal as identifier`
- **Validação semântica**: Garantir que `literal` é compatível com `Type`

Esta é uma implementação de **análise semântica básica**, focada em **verificação de tipos** para declarações de variáveis, seguindo os princípios da teoria de compiladores.