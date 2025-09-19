"""
Compilador Principal - Função de Alto Nível

Orquestra todo o processo de compilação de regex para DFA,
integrando todos os módulos do pacote.
"""

from .estruturas import DFA, resetar_ids
from .tokenizer import tokenize_regex, add_concat_tokens
from .parser import to_postfix
from .thompson import postfix_to_nfa
from .subconjuntos import compile_nfa_to_dfa


def compile_regex_to_dfa(regex: str) -> DFA:
    """
    FUNÇÃO PRINCIPAL: Compila uma expressão regular em um DFA
    
    Passos:
    1. Tokeniza a regex (quebra em pedaços)
    2. Adiciona operadores de concatenação explícitos
    3. Converte para notação postfix (Shunting-yard)
    4. Constrói NFA usando algoritmo de Thompson
    5. Converte NFA para DFA usando construção de subconjuntos
    
    Args:
        regex: expressão regular como string
        
    Returns:
        Autômato finito determinístico que reconhece a regex
        
    Raises:
        ValueError: se a regex for malformada
        
    Exemplo:
        >>> dfa = compile_regex_to_dfa("ab*")
        >>> dfa.accepts("a")      # True
        >>> dfa.accepts("abb")    # True  
        >>> dfa.accepts("ba")     # False
    """
    # Reseta gerador de IDs para execuções limpas (útil para testes)
    resetar_ids()
    
    # Pipeline de compilação
    tokens = tokenize_regex(regex)
    tokens = add_concat_tokens(tokens)
    postfix = to_postfix(tokens)
    nfa = postfix_to_nfa(postfix)
    dfa = compile_nfa_to_dfa(nfa)
    
    return dfa