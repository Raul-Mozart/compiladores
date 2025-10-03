"""
afn_afd_builder.py
------------------
Construtor de AFN unificado a partir de múltiplos AFDs de tokens
+ determinização (subset construction) para um AFD único
+ minimização (Hopcroft)
+ utilitários de exportação.

Uso típico:
    from afn_afd_builder import TokenDFA, dfa_list_to_union_nfa, nfa_to_dfa, minimize_dfa, dfa_to_table
"""

import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, List, Iterable, Hashable, FrozenSet, Optional

@dataclass
class TokenDFA:
    name: str                             # e.g., "IDENT"
    states: Set[Hashable]
    alphabet: Set[Hashable]
    start: Hashable
    finals: Set[Hashable]
    delta: Dict[Tuple[Hashable, Hashable], Hashable]
    priority: int = 100                   # menor = maior prioridade

@dataclass
class NFA:
    states: Set[Hashable]
    alphabet: Set[Hashable]
    start: Hashable
    finals: Dict[Hashable, Dict[str, int]]  # estado -> {token_name: priority}
    delta: Dict[Tuple[Hashable, Hashable], Set[Hashable]] = field(default_factory=dict)
    eps: Dict[Hashable, Set[Hashable]] = field(default_factory=dict)  # transições epsilon

@dataclass
class DFA:
    states: Set[str]  # rotulamos subconjuntos como strings para legibilidade
    alphabet: Set[Hashable]
    start: str
    finals: Dict[str, Dict[str, int]]  # estado -> candidatos {token_name: priority}
    winner: Dict[str, str]             # estado -> token vencedor
    delta: Dict[Tuple[str, Hashable], str]  # transições determinísticas

# ---------- Helpers ----------

def _label_set(s: FrozenSet[Hashable]) -> str:
    # rótulo estável para estados-conjunto
    return "{" + ",".join(sorted(map(str, s))) + "}"

def _epsilon_closure(nfa: NFA, states: Iterable[Hashable]) -> FrozenSet[Hashable]:
    stack = list(states)
    visited: Set[Hashable] = set(stack)
    while stack:
        q = stack.pop()
        for r in nfa.eps.get(q, set()):
            if r not in visited:
                visited.add(r)
                stack.append(r)
    return frozenset(visited)

def _move(nfa: NFA, S: FrozenSet[Hashable], a: Hashable) -> FrozenSet[Hashable]:
    out: Set[Hashable] = set()
    for q in S:
        for r in nfa.delta.get((q, a), set()):
            out.add(r)
    return frozenset(out)

# ---------- 1) DFAs -> AFN unificado (ε-união) ----------

def dfa_list_to_union_nfa(dfas: List[TokenDFA], start_name: str = "S") -> NFA:
    states: Set[Hashable] = set()
    alphabet: Set[Hashable] = set()
    finals: Dict[Hashable, Dict[str, int]] = defaultdict(dict)
    delta: Dict[Tuple[Hashable, Hashable], Set[Hashable]] = defaultdict(set)
    eps: Dict[Hashable, Set[Hashable]] = defaultdict(set)

    global_start = start_name
    states.add(global_start)

    for dfa in dfas:
        prefix = f"{dfa.name}."
        # prefixa estados para evitar colisões
        p_states = {prefix + str(s) for s in dfa.states}
        states |= p_states
        alphabet |= dfa.alphabet

        p_start = prefix + str(dfa.start)
        eps[global_start].add(p_start)

        # transições
        for (s, a), t in dfa.delta.items():
            delta[(prefix + str(s), a)].add(prefix + str(t))

        # finais
        for f in dfa.finals:
            finals[prefix + str(f)][dfa.name] = dfa.priority

    return NFA(states=states, alphabet=alphabet, start=global_start, finals=finals, delta=delta, eps=eps)

# ---------- 2) AFN -> AFD (construção de subconjuntos) ----------

def nfa_to_dfa(nfa: NFA) -> DFA:
    start_set = _epsilon_closure(nfa, [nfa.start])
    start_label = _label_set(start_set)

    states: Set[str] = set([start_label])
    finals: Dict[str, Dict[str, int]] = {}
    winner: Dict[str, str] = {}
    delta: Dict[Tuple[str, Hashable], str] = {}

    # registra finais do estado inicial, se houver
    contenders = _collect_contenders(nfa, start_set)
    if contenders:
        finals[start_label] = contenders
        winner[start_label] = _choose_winner(contenders)

    queue = deque([start_set])
    seen: Set[FrozenSet[Hashable]] = {start_set}

    while queue:
        S = queue.popleft()
        S_label = _label_set(S)

        for a in nfa.alphabet:
            move_set = _move(nfa, S, a)
            if not move_set:
                continue
            T = _epsilon_closure(nfa, move_set)
            T_label = _label_set(T)

            delta[(S_label, a)] = T_label

            if T not in seen:
                seen.add(T)
                states.add(T_label)
                queue.append(T)
                contenders_T = _collect_contenders(nfa, T)
                if contenders_T:
                    finals[T_label] = contenders_T
                    winner[T_label] = _choose_winner(contenders_T)

    return DFA(states=states, alphabet=set(nfa.alphabet), start=start_label, finals=finals, winner=winner, delta=delta)

def _collect_contenders(nfa: NFA, subset: FrozenSet[Hashable]) -> Dict[str, int]:
    contenders: Dict[str, int] = {}
    for q in subset:
        if q in nfa.finals:
            for tok, prio in nfa.finals[q].items():
                if tok not in contenders or prio < contenders[tok]:
                    contenders[tok] = prio
    return contenders

def _choose_winner(contenders: Dict[str, int]) -> str:
    # menor prioridade vence; empate quebra por nome do token
    best_prio = min(contenders.values())
    best_tokens = [t for t, p in contenders.items() if p == best_prio]
    return sorted(best_tokens)[0]

# ---------- 3) Minimização (Hopcroft) ----------

def minimize_dfa(dfa: DFA) -> DFA:
    # particiona finais por token vencedor; não-finais em um bloco à parte
    finals_by_token: Dict[str, Set[str]] = defaultdict(set)
    for s, tok in dfa.winner.items():
        finals_by_token[tok].add(s)
    nonfinals = set(dfa.states) - set(dfa.winner.keys())

    P: List[Set[str]] = [nonfinals] if nonfinals else []
    P.extend(s for s in finals_by_token.values() if s)
    P = [b for b in P if b]

    W: deque[Set[str]] = deque(P)

    while W:
        A = W.popleft()
        for a in dfa.alphabet:
            X = {s for (s, sym), t in dfa.delta.items() if sym == a and t in A}
            newP = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    newP.extend([inter, diff])
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        W.append(inter if len(inter) <= len(diff) else diff)
                else:
                    newP.append(Y)
            P = newP

    # mapeia estado antigo -> representante do bloco
    block_id: Dict[str, str] = {}
    for block in P:
        rep = sorted(block)[0]
        for s in block:
            block_id[s] = rep

    new_states = set(block_id.values())
    new_start = block_id[dfa.start]

    new_delta: Dict[Tuple[str, Hashable], str] = {}
    for (s, a), t in dfa.delta.items():
        new_delta[(block_id[s], a)] = block_id[t]

    new_finals: Dict[str, Dict[str, int]] = {}
    new_winner: Dict[str, str] = {}
    for old_state, contenders in dfa.finals.items():
        rep = block_id[old_state]
        if rep not in new_finals:
            new_finals[rep] = dict(contenders)
        else:
            for tok, pr in contenders.items():
                if tok not in new_finals[rep] or pr < new_finals[rep][tok]:
                    new_finals[rep][tok] = pr

    for rep, contenders in new_finals.items():
        new_winner[rep] = _choose_winner(contenders)

    return DFA(states=new_states, alphabet=set(dfa.alphabet), start=new_start,
               finals=new_finals, winner=new_winner, delta=new_delta)

# ---------- Export / utilitário ----------

def dfa_to_table(dfa: DFA) -> Dict:
    return {
        "states": sorted(dfa.states),
        "alphabet": sorted(map(str, dfa.alphabet)),
        "start": dfa.start,
        "finals": {s: {"winner": dfa.winner.get(s), "contenders": dfa.finals.get(s, {})}
                   for s in sorted(dfa.states) if (s in dfa.winner or s in dfa.finals)},
        "delta": {"%s|%s" % (s, str(a)): t for (s, a), t in dfa.delta.items()},
    }

# ---------- Exemplo executável ----------

def _toy_example() -> Tuple[DFA, DFA]:
    # PLUS: reconhece "+"
    plus = TokenDFA(
        name="PLUS",
        states={"q0", "q1"},
        alphabet={"+", "g", "1"},
        start="q0",
        finals={"q1"},
        delta={("q0", "+"): "q1"},
        priority=10
    )

    # IDENT: "g" (uma ou mais) -- brinquedo
    ident = TokenDFA(
        name="IDENT",
        states={"s", "f"},
        alphabet={"+", "g", "1"},
        start="s",
        finals={"f"},
        delta={("s", "g"): "f", ("f", "g"): "f"},
        priority=20
    )

    # DIGIT1: "1" exato
    digit1 = TokenDFA(
        name="DIGIT1",
        states={"a", "b"},
        alphabet={"+", "g", "1"},
        start="a",
        finals={"b"},
        delta={("a", "1"): "b"},
        priority=15
    )

    nfa = dfa_list_to_union_nfa([plus, ident, digit1])
    dfa = nfa_to_dfa(nfa)
    dfa_min = minimize_dfa(dfa)
    return dfa, dfa_min

if __name__ == "__main__":
    dfa, dfa_min = _toy_example()
    with open("dfa_union.json", "w", encoding="utf-8") as f:
        json.dump(dfa_to_table(dfa), f, ensure_ascii=False, indent=2)
    with open("dfa_union_min.json", "w", encoding="utf-8") as f:
        json.dump(dfa_to_table(dfa_min), f, ensure_ascii=False, indent=2)
    print("Gerado dfa_union.json e dfa_union_min.json")
