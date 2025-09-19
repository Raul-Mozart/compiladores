"""
Construção de Thompson - Conversão Postfix → NFA

Implementa o algoritmo de Thompson para construir autômatos
não-determinísticos a partir de expressões em notação postfix.

O algoritmo trabalha com uma pilha de NFAs e combina-os usando
as regras de Thompson para cada operador.
"""

from typing import List, Set
from .estruturas import NFA, EstadoNFA
from .tokenizer import escape_to_char
from .constantes import CARACTERES_PERMITIDOS


def atom_to_nfa(atom: str) -> NFA:
    r"""
    Converte um átomo básico em um NFA
    
    Um átomo pode ser:
    - caractere simples: 'a'
    - escape: '\d' (dígitos), '\n' (nova linha), etc.
    - classe: '[abc]' ou '[^abc]' (negação)
    - ponto: '.' (qualquer caractere)
    
    Args:
        atom: token representando um átomo
        
    Returns:
        NFA que reconhece o átomo
        
    Raises:
        ValueError: se o átomo for malformado
    """
    s = EstadoNFA()  # estado inicial
    e = EstadoNFA()  # estado final
    
    if atom.startswith('\\'):
        # Escape: \d, \w, \s, \n, etc.
        set_chars = escape_to_char(atom[1:])
        
    elif atom.startswith('['):
        # Classe de caracteres: [abc] ou [^abc]
        content = atom[1:-1]  # remove [ e ]
        negate = content.startswith('^')
        
        if negate:
            charset = content[1:]
        else:
            charset = content
            
        # Expande escapes dentro da classe
        expanded = set()
        i = 0
        while i < len(charset):
            if charset[i] == "\\":
                i += 1
                if i >= len(charset):
                    raise ValueError("Escape malformado na classe")
                expanded |= escape_to_char(charset[i])
                i += 1
            else:
                expanded.add(charset[i])
                i += 1
        
        if negate:
            # Classe negada: todos os caracteres EXCETO os especificados
            allowed = set(CARACTERES_PERMITIDOS) - expanded
        else:
            # Classe normal: apenas os caracteres especificados
            allowed = expanded
            
        set_chars = allowed
        
    elif atom == '.':
        # Ponto: qualquer caractere
        set_chars = set(CARACTERES_PERMITIDOS)
        
    else:
        # Caractere literal
        set_chars = set([atom])
    
    # Adiciona a transição: estado inicial --[caracteres]--> estado final
    key = frozenset(set_chars)
    s.adicionar_transicao(key, e)
    return NFA(s, e)


def postfix_to_nfa(postfix: List[str]) -> NFA:
    """
    Converte expressão em notação postfix para NFA usando Construção de Thompson
    
    Operadores suportados:
    - '.': concatenação (ab)
    - '|': união (a|b)  
    - '*': estrela (a* = zero ou mais)
    - '+': plus (a+ = um ou mais)
    - '?': opcional (a? = zero ou um)
    
    Args:
        postfix: expressão em notação postfix
        
    Returns:
        NFA que reconhece a expressão
        
    Raises:
        ValueError: se a expressão for inválida
    """
    stack: List[NFA] = []
    
    for tok in postfix:
        if tok == '.':  # Concatenação: ab
            if len(stack) < 2:
                raise ValueError("Operador de concatenação precisa de 2 operandos")
            n2 = stack.pop()
            n1 = stack.pop()
            # Conecta final de n1 ao início de n2 com transição epsilon
            n1.accept.adicionar_eps(n2.start)
            stack.append(NFA(n1.start, n2.accept))
            
        elif tok == '|':  # União: a|b  
            if len(stack) < 2:
                raise ValueError("Operador de união precisa de 2 operandos")
            n2 = stack.pop()
            n1 = stack.pop()
            s = EstadoNFA()  # novo estado inicial
            e = EstadoNFA()  # novo estado final
            # Novo início se conecta aos dois caminhos
            s.adicionar_eps(n1.start)
            s.adicionar_eps(n2.start)
            # Os dois finais se conectam ao novo final
            n1.accept.adicionar_eps(e)
            n2.accept.adicionar_eps(e)
            stack.append(NFA(s, e))
            
        elif tok == '*':  # Estrela: a* (zero ou mais)
            if len(stack) < 1:
                raise ValueError("Operador estrela precisa de 1 operando")
            n = stack.pop()
            s = EstadoNFA()
            e = EstadoNFA()
            # Pode pular direto (zero ocorrências)
            s.adicionar_eps(n.start)
            s.adicionar_eps(e)
            # Pode repetir (loop)
            n.accept.adicionar_eps(n.start)
            n.accept.adicionar_eps(e)
            stack.append(NFA(s, e))
            
        elif tok == '+':  # Plus: a+ (um ou mais)
            if len(stack) < 1:
                raise ValueError("Operador plus precisa de 1 operando")
            n = stack.pop()
            s = EstadoNFA()
            e = EstadoNFA()
            # Deve executar pelo menos uma vez
            s.adicionar_eps(n.start)
            # Pode repetir
            n.accept.adicionar_eps(n.start)
            n.accept.adicionar_eps(e)
            stack.append(NFA(s, e))
            
        elif tok == '?':  # Opcional: a? (zero ou um)
            if len(stack) < 1:
                raise ValueError("Operador opcional precisa de 1 operando")
            n = stack.pop()
            s = EstadoNFA()
            e = EstadoNFA()
            # Pode executar
            s.adicionar_eps(n.start)
            # Pode pular
            s.adicionar_eps(e)
            n.accept.adicionar_eps(e)
            stack.append(NFA(s, e))
            
        else:
            # Operando (átomo)
            stack.append(atom_to_nfa(tok))
    
    if len(stack) != 1:
        raise ValueError("Regex inválida: sobrou elementos na pilha")
        
    return stack[0]