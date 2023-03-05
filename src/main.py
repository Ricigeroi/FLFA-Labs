from Grammar import Grammar
from N_FiniteAutomaton import N_FiniteAutomaton


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
        ('q2', 'b'): ['q2', 'q3'],
        ('q3', 'a'): ['q1'],
        ('q3', 'b'): ['q4'],
    }
    initial_state = 'q0'
    final_states = ['q4']

    print()
    print()

    # Lab 1
    grammar = Grammar(Vn, Vt, P, S)
    # print(grammar.to_finite_automaton())
    ####################################################################################################################
    # LAB 2 STARTS HERE
    #
    #
    # Grammar classification
    print("Grammar classification by Chomsky:", grammar.chomsky())
    print()

    # Creating of the new NFA
    automaton = N_FiniteAutomaton(Q, alphabet, initial_state, transition, final_states)

    # Convert NFA to grammar
    new_grammar = automaton.to_grammar()

    print('________Automata to grammar________')
    print("Type of the automaton is", automaton.type_automaton())
    print('Vn =', new_grammar.non_terminal_vars)
    print('Vt =', new_grammar.terminal_vars)
    print('P =', new_grammar.production)
    print('S =', new_grammar.start_symbol)

    # NFA to DFA conversion
    dfa = automaton.nfa2dfa()
    print('________NFA to DFA conversion________')
    print("Type of the automaton is", dfa.type_automaton())
    print('Q =', dfa.Q)
    print('Sigma =', dfa.Sigma)
    print('Delta =', dfa.delta)
    print('q0 =', dfa.q0)
    print('___________________________________')



