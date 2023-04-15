from Grammar import Grammar
from Lexer import Lexer
from N_FiniteAutomaton import N_FiniteAutomaton


# Lab 1 and lab 2 code
def lab_1_2():
    # Lab 1 data
    Vn = ["S", "D", "R"]
    Vt = ["a", "b", "c", "d", "f"]
    P = {
        "S": ["aS", "bD", "fR"],
        "D": ["cD", "dR", "d"],
        "R": ["bR", "f"]
    }
    S = "S"

    grammar = Grammar(Vn, Vt, P, S)
    print(grammar.to_finite_automaton())
    # Lab 2 #
    ################################################################
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
    print('Delta =')
    for tran in dfa.delta:
        print(tran, '=', dfa.delta[tran])
    print('q0 =', dfa.q0)
    print('F =', dfa.F)
    print('___________________________________')

    # Graphical representation of the NFA
    # automaton.draw_graph().view()
# Lab 3 code
def lab_3():
    input_string = str(input("Enter string: "))
    # Create a lexer instance with some sample input
    lexer = Lexer(input_string)

    # Get tokens until end of input
    token = lexer.get_next_token()
    while token is not None:
        print(token)
        token = lexer.get_next_token()


if __name__ == "__main__":
    # Call lab 1 and 2 functions
    # lab_1_2()
    # Call lab 3 functions
    # lab_3()
    #############################
    # LAB 4 #

    Vn = ["S", "A", "B", "C", "E"]
    Vt = ["a", "d"]
    P = {
        "S": ["dB", "A"],
        "A": ["d", "dS", "aAdAB"],
        "B": ["aC", "aS", "AC"],
        "C": [""],
        "E": ["AS"]
    }
    S = "S"

    grammar = Grammar(Vn, Vt, P, S)





