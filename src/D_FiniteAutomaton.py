class D_FiniteAutomaton:
    def __init__(self, Q, Sigma, q0, F, delta):
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.F = F
        self.delta = delta

    # Lab 1 function
    def string_belongs_to_language(self, input_string):
        current_state = self.q0
        for index in range(0, len(input_string)):
            if (current_state, input_string[index]) in self.delta:
                next_states = self.delta[(current_state, input_string[index])]
                # Case for last symbol in string (trying to find final state in last transition)
                if len(next_states) > 1 and index == len(input_string) - 1:
                    current_state = next_states[next_states.index('F')]
                else:
                    current_state = next_states[0]
            else:
                return False
        return current_state in self.F

    # Lab 2 function
    def to_grammar(self):
        from Grammar import Grammar
        production = {}

        for t in self.delta.keys():
            if t[0] not in production.keys():
                production[t[0]] = []

        for t in self.delta.keys():
            for s in self.delta[t]:
                if t[1] + s not in production[t[0]]:
                    production[t[0]].append(t[1] + s)

        return Grammar(self.Q, self.Sigma, production, self.q0)

    def type_automaton(self):
        for item in self.delta:
            if len(item) > 1:
                return 'NFA'
        return 'DFA'
