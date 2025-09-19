"""
Estruturas de Dados para Autômatos

Define as classes principais para representar:
- EstadoNFA: Estado em autômato não-determinístico
- NFA: Autômato não-determinístico completo  
- DFA: Autômato determinístico completo
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Set, Dict, FrozenSet, Tuple, Optional, List

# ---------- Gerador de IDs únicos ----------
_proximo_id_estado = 0


def _novo_id_estado():
    """Gera um ID único para cada estado do autômato"""
    global _proximo_id_estado
    _proximo_id_estado += 1
    return _proximo_id_estado


def resetar_ids():
    """Reseta o contador de IDs (útil para testes)"""
    global _proximo_id_estado
    _proximo_id_estado = 0


# ---------- Classes de Estruturas ----------

@dataclass
class EstadoNFA:
    """
    Representa um estado no Autômato Não-Determinístico (NFA)
    
    Atributos:
    - id: identificador único do estado
    - eps: conjunto de estados alcançáveis por transições epsilon (vazias)
    - trans: dicionário de transições por caracteres
    """
    id: int
    eps: Set["EstadoNFA"]
    trans: Dict[FrozenSet[str], Set["EstadoNFA"]]

    def __init__(self):
        self.id = _novo_id_estado()
        self.eps = set()  # transições vazias (epsilon)
        self.trans = defaultdict(set)  # transições por caracteres

    def adicionar_eps(self, estado: "EstadoNFA"):
        """Adiciona uma transição epsilon (vazia) para outro estado"""
        self.eps.add(estado)

    def adicionar_transicao(self, conjunto_simbolos: FrozenSet[str], estado: "EstadoNFA"):
        """Adiciona uma transição que consome caracteres do conjunto_simbolos"""
        self.trans[conjunto_simbolos].add(estado)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, EstadoNFA) and self.id == other.id


@dataclass
class NFA:
    """
    Representa um Autômato Não-Determinístico completo
    
    Atributos:
    - start: estado inicial
    - accept: estado de aceitação (final)
    """
    start: EstadoNFA
    accept: EstadoNFA


@dataclass
class DFA:
    """
    Representa um Autômato Finito Determinístico completo
    
    Atributos:
    - start: índice do estado inicial
    - states: lista de conjuntos de IDs dos estados NFA correspondentes
    - accept_states: conjunto de índices dos estados de aceitação
    - trans: tabela de transições [estado][caractere] = próximo_estado
    """
    start: int
    states: List[FrozenSet[int]] = field(default_factory=list)
    accept_states: Set[int] = field(default_factory=set)
    trans: Dict[int, Dict[str, int]] = field(default_factory=dict)

    def accepts_str(self, s: str) -> bool:
        """Verifica se uma string é aceita pelo autômato"""
        return self.accepts_str_with_dead(s)[0]

    def accepts_str_with_dead(self, s: str) -> Tuple[bool, Optional[int]]:
        """
        Verifica se uma string é aceita e retorna o estado final
        
        Retorna:
            (aceita: bool, estado_final: int ou None)
        """
        cur = self.start
        for ch in s:
            if ch not in self.trans[cur]:
                return False, None
            cur = self.trans[cur][ch]
        return (cur in self.accept_states), cur

    def accepts(self, text: str) -> bool:
        """Alias para accepts_str (compatibilidade)"""
        return self.accepts_str(text)