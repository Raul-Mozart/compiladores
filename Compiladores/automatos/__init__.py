"""
Pacote de Autômatos - Compilador de Expressões Regulares

Este pacote contém todos os módulos necessários para compilar
expressões regulares em autômatos finitos determinísticos.

Módulos:
- constantes: Definições de caracteres e tokens
- estruturas: Classes para NFA e DFA  
- tokenizer: Análise léxica de regex
- parser: Conversão para notação postfix
- thompson: Construção de NFA
- subconjuntos: Conversão NFA → DFA
- compilador: Função principal

Uso:
    from automatos import compile_regex_to_dfa
    dfa = compile_regex_to_dfa("ab*")
    resultado = dfa.accepts("abb")  # True
"""

from .compilador import compile_regex_to_dfa
from .estruturas import DFA, NFA, EstadoNFA

__all__ = ['compile_regex_to_dfa', 'DFA', 'NFA', 'EstadoNFA']
__version__ = '1.0.0'