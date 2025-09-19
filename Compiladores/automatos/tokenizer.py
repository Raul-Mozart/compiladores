"""
Tokenizer - Análise Léxica de Expressões Regulares

Responsável por quebrar uma string de regex em tokens individuais,
tratando escapes, classes de caracteres e operadores especiais.
"""

from typing import Set, List


def escape_to_char(c: str) -> Set[str]:
    r"""
    Converte escape em conjunto de caracteres
    
    Exemplos:
    - 'd' → {'0', '1', '2', ..., '9'}  
    - 'w' → {'a', 'b', ..., 'z', 'A', ..., 'Z', '0', ..., '9', '_'}
    - 's' → {' ', '\t', '\n', '\r'}
    - 'n' → {'\n'}
    """
    if c == "d":
        return set(chr(i) for i in range(ord('0'), ord('9') + 1))
    if c == "w":
        s = set(chr(i) for i in range(ord('a'), ord('z') + 1))
        s |= set(chr(i) for i in range(ord('A'), ord('Z') + 1))
        s |= set(chr(i) for i in range(ord('0'), ord('9') + 1))
        s.add('_')
        return s
    if c == "s":
        return set([' ', '\t', '\n', '\r'])
    if c == "n":
        return set(['\n'])
    if c == "t":
        return set(['\t'])
    if c == "r":
        return set(['\r'])
    # escape literal (ex: \+, \*, \[)
    return set([c])


def tokenize_regex(regex: str) -> List[str]:
    r"""
    Tokeniza uma expressão regular em lista de tokens
    
    Trata:
    - Escapes: \\d, \\w, \\s, \\n, \\+, etc.
    - Classes: [abc], [a-z], [^abc] (negação)
    - Operadores: |, *, +, ?, (, )
    - Literais: a, b, 1, etc.
    
    Args:
        regex: expressão regular como string
        
    Returns:
        Lista de tokens
        
    Raises:
        ValueError: se regex for malformada
    """
    i = 0
    tokens = []
    L = len(regex)
    
    while i < L:
        c = regex[i]
        
        if c == "\\":
            # Escape: \d, \n, \+, etc.
            i += 1
            if i >= L:
                raise ValueError("Escape pendente no final da regex")
            tokens.append("\\" + regex[i])
            i += 1
            
        elif c == "[":
            # Classe de caracteres: [abc], [a-z], [^abc]
            j = i + 1
            negate = False
            
            # Verifica negação
            if j < L and regex[j] == '^':
                negate = True
                j += 1
                
            chars = []
            while j < L and regex[j] != "]":
                if regex[j] == "\\":
                    # Escape dentro da classe
                    j += 1
                    if j >= L:
                        raise ValueError("Escape malformado na classe de caracteres")
                    chars.append("\\" + regex[j])
                    j += 1
                elif j + 2 < L and regex[j+1] == '-' and regex[j+2] != ']':
                    # Range: a-z
                    start = regex[j]
                    end = regex[j+2]
                    for code in range(ord(start), ord(end)+1):
                        chars.append(chr(code))
                    j += 3
                else:
                    # Caractere literal
                    chars.append(regex[j])
                    j += 1
                    
            if j >= L or regex[j] != "]":
                raise ValueError("Classe de caracteres não fechada")
                
            # Monta token da classe
            prefix = "[^" if negate else "["
            tokens.append(prefix + "".join(chars) + "]")
            i = j + 1
            
        else:
            # Caractere literal ou operador
            tokens.append(c)
            i += 1
            
    return tokens


def add_concat_tokens(tokens: List[str]) -> List[str]:
    """
    Insere operadores de concatenação explícitos '.' onde necessário
    
    Regras:
    - Entre operandos: ab → a.b
    - Após operadores unários: a*b → a*.b  
    - Não antes de operadores: a|b (mantém a|b)
    - Não após operadores binários: a|b (mantém a|b)
    
    Args:
        tokens: lista de tokens
        
    Returns:
        Lista de tokens com concatenações explícitas
    """
    result = []
    i = 0
    
    while i < len(tokens):
        t = tokens[i]
        result.append(t)
        
        # Se há próximo token, verifica se deve inserir concatenação
        if i + 1 < len(tokens):
            left = t
            right = tokens[i+1]
            
            # Token atual pode ser operando esquerdo?
            left_can_end = (left not in ['|', '('])
            
            # Próximo token pode ser operando direito?  
            right_can_start = (right not in ['|', ')', '*', '+', '?'])
            
            if left_can_end and right_can_start:
                result.append(".")
                
        i += 1
        
    return result