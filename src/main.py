from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


if __name__ == "__main__":
    # Lab 1 data
    Vn = ["S", "D", "R"]
    Vt = ["a", "b", "c", "d", "f"]
    P = {
        "S": ["aS", "bD", "fR"],
        "D": ["cD", "dR", "d"],
        "R": ["bR", "f"]
    }
    S = "S"

    # Lab 2 data
    Q = ('q0', 'q1', 'q2', 'q3', 'q4')
    alphabet = ['a', 'b']
    transition = {
        ('q0', 'a'): ['q1'],
        ('q1', 'b'): ['q1'],
        ('q1', 'a'): ['q2'],
        ('q2', 'b'): ['q2'],
        ('q2', 'b'): ['q3'],
        ('q3', 'a'): ['q1'],
        ('q3', 'b'): ['q4'],
    }
    initial_state = 'q0'
    final_states = ['q4']

    grammar = Grammar(Vn, Vt, P, S)

    print(grammar.to_finite_automaton())

    automaton = FiniteAutomaton(Q, alphabet, transition, initial_state, final_states)
    print(automaton.to_grammar())
