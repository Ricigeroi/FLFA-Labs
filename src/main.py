from Grammar import Grammar

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
    Q = ['q0', 'q1', 'q2', 'q3', 'q4']
    alphabet = ['a', 'b']
    transition = {}
    initial_state = 'q0'
    final_states = 'q4'

    grammar = Grammar(Vn, Vt, P, S)

    print(grammar.to_finite_automaton())

    print()
