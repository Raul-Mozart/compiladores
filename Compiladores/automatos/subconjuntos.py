"""
Construção de Subconjuntos - Conversão NFA → DFA

Implementa o algoritmo de construção de subconjuntos para converter
autômatos não-determinísticos (NFA) em determinísticos (DFA).

O algoritmo funciona agrupando estados do NFA que podem ser
alcançados simultaneamente em um único estado do DFA.
"""

from collections import deque
from typing import Set, Dict, FrozenSet, List
from .estruturas import NFA, DFA, EstadoNFA
from .constantes import CARACTERES_PERMITIDOS


def epsilon_closure(states: Set[EstadoNFA]) -> Set[EstadoNFA]:
    """
    Calcula o fechamento epsilon: todos os estados alcançáveis por transições vazias
    
    Isso significa: a partir de um conjunto de estados, quais outros estados
    posso alcançar sem consumir nenhum caractere de entrada?
    
    Args:
        states: conjunto inicial de estados
        
    Returns:
        Conjunto expandido incluindo todos os estados alcançáveis por epsilon
    """
    stack = list(states)
    closure = set(states)
    
    while stack:
        st = stack.pop()
        for e in st.eps:  # Para cada transição epsilon
            if e not in closure:
                closure.add(e)
                stack.append(e)
                
    return closure


def nfa_states_ids(nfa_states: Set[EstadoNFA]) -> FrozenSet[int]:
    """
    Converte conjunto de estados NFA em conjunto de IDs (para usar como chave)
    
    Args:
        nfa_states: conjunto de estados do NFA
        
    Returns:
        Conjunto imutável (frozenset) de IDs dos estados
    """
    return frozenset(sorted(s.id for s in nfa_states))


def compile_nfa_to_dfa(nfa: NFA) -> DFA:
    """
    Converte NFA em DFA usando algoritmo de construção de subconjuntos
    
    Processo:
    1. Estado inicial do DFA = fechamento epsilon do estado inicial do NFA
    2. Para cada estado do DFA e cada caractere:
       - Calcula quais estados do NFA são alcançáveis
       - Agrupa esses estados em um novo estado do DFA
    3. Repete até não haver mais estados novos
    
    Args:
        nfa: autômato não-determinístico
        
    Returns:
        Autômato determinístico equivalente
    """
    # Estado inicial: fechamento epsilon do estado inicial do NFA
    start_closure = epsilon_closure({nfa.start})
    start_ids = nfa_states_ids(start_closure)
    
    # Estruturas do DFA
    states_list: List[FrozenSet[int]] = [start_ids]
    state_map: Dict[FrozenSet[int], int] = {start_ids: 0}
    accept_states: Set[int] = set()
    trans: Dict[int, Dict[str, int]] = {}
    
    # Se o estado inicial contém o estado de aceitação do NFA, é estado final
    if nfa.accept.id in start_ids:
        accept_states.add(0)
    
    # Fila para processar novos estados (BFS)
    queue = deque([start_closure])
    
    # Cria mapeamento id→estado para facilitar busca
    all_states_by_id = {}
    stack = [nfa.start]
    while stack:
        st = stack.pop()
        if st.id in all_states_by_id:
            continue
        all_states_by_id[st.id] = st
        for symset, dests in st.trans.items():
            for d in dests:
                stack.append(d)
        for e in st.eps:
            stack.append(e)

    # Para facilitar o cálculo de movimentos, criamos lista de todos os caracteres possíveis (ASCII)
    alphabet = CARACTERES_PERMITIDOS

    # Mapeia conjuntos de IDs para objetos de estado (para facilitar cálculos)
    visited_closure_objects: Dict[FrozenSet[int], Set[EstadoNFA]] = {start_ids: start_closure}

    while queue:
        cur_closure = queue.popleft()
        cur_ids = nfa_states_ids(cur_closure)
        cur_state_idx = state_map[cur_ids]
        trans[cur_state_idx] = {}
        
        # Para cada caractere possível, calcula movimento
        for ch in alphabet:
            move_set: Set[EstadoNFA] = set()
            
            for st in cur_closure:
                # Para cada transição do estado atual
                for symset, dests in st.trans.items():
                    # Se o caractere está no conjunto de símbolos da transição
                    if ch in symset:
                        for d in dests:
                            move_set.add(d)
            
            if not move_set:
                # Sem transição para este caractere
                continue
            
            # Calcula fechamento epsilon do conjunto destino
            closure2 = epsilon_closure(move_set)
            ids2 = nfa_states_ids(closure2)
            
            if ids2 not in state_map:
                # Novo estado do DFA
                idx = len(states_list)
                state_map[ids2] = idx
                states_list.append(ids2)
                visited_closure_objects[ids2] = closure2
                
                # Verifica se é estado de aceitação
                if nfa.accept.id in ids2:
                    accept_states.add(idx)
                    
                queue.append(closure2)
            
            # Adiciona transição
            trans[cur_state_idx][ch] = state_map[ids2]
    
    return DFA(
        start=0,
        states=states_list, 
        accept_states=accept_states, 
        trans=trans
    )