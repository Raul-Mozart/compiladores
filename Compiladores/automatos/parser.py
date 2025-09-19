"""
Parser - Conversão para Notação Postfix

Converte tokens de regex em notação postfix (polonesa reversa)
usando o algoritmo Shunting-yard de Dijkstra.

Precedência dos operadores:
1. *, +, ? (unários, maior precedência)
2. . (concatenação, precedência média)  
3. | (união, menor precedência)
"""

from typing import List


def to_postfix(tokens: List[str]) -> List[str]:
    """
    Converte lista de tokens para notação postfix usando Shunting-yard
    
    Exemplos:
    - ['a', 'b'] → ['a', 'b', '.']  (concatenação)
    - ['a', '|', 'b'] → ['a', 'b', '|']  (união)
    - ['a', '*'] → ['a', '*']  (estrela)
    - ['(', 'a', '|', 'b', ')', '*'] → ['a', 'b', '|', '*']
    
    Args:
        tokens: lista de tokens da regex
        
    Returns:
        Lista de tokens em notação postfix
        
    Raises:
        ValueError: se parênteses estiverem desbalanceados
    """
    # Precedência: maior número = maior precedência
    prec = {
        '*': 5,  # unários (maior precedência)
        '+': 5,
        '?': 5,
        '.': 4,  # concatenação (precedência média)
        '|': 3   # união (menor precedência)
    }
    
    output = []
    stack = []
    
    for tok in tokens:
        if tok == '(':
            # Abre parênteses: empilha
            stack.append(tok)
            
        elif tok == ')':
            # Fecha parênteses: desempilha até encontrar '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Parênteses desbalanceados: ')' sem '(' correspondente")
            stack.pop()  # remove o '('
            
        elif tok in prec:
            # Operador: desempilha operadores de maior ou igual precedência
            while (stack and 
                   stack[-1] != '(' and 
                   prec.get(stack[-1], 0) >= prec[tok]):
                output.append(stack.pop())
            stack.append(tok)
            
        else:
            # Operando: vai direto para output
            output.append(tok)
    
    # Desempilha operadores restantes
    while stack:
        if stack[-1] in ('(', ')'):
            raise ValueError("Parênteses desbalanceados")
        output.append(stack.pop())
    
    return output