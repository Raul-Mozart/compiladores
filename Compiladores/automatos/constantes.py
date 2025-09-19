"""
Constantes do Compilador de Regex

Contém definições de caracteres permitidos e tokens comuns
para análise léxica de linguagens de programação.
"""

# Caracteres ASCII imprimíveis (espaço até ~) + tab/quebra de linha
CARACTERES_PERMITIDOS = [chr(c) for c in (list(range(32, 127)) + [9, 10, 13])]

# ---------- Exemplos de tokens comuns para análise léxica ----------
TOKENS_COMUNS = {
    # IDENTIFICADOR: letra ou underscore seguido de letras/dígitos/underscore
    "IDENT": r"[A-Za-z_][A-Za-z0-9_]*",
    # INTEIRO: sequência de dígitos
    "INT": r"\d+",
    # FLOAT: número decimal simples (dígitos.dígitos)
    "FLOAT": r"\d+\.\d+",
    # STRING: aspas duplas, permite escapes simples
    "STRING": r'\"(\\.|[^"])*\"',
    # OPERADORES: operadores comuns de linguagens de programação
    "OP": r"==|!=|<=|>=|\+|-|\*|/|=|<|>|\(|\)|\{|\}|;|,",
    # ESPAÇOS EM BRANCO
    "WS": r"[ \t\n\r]+",
}