class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

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

    def to_grammar(self):
        non_terminal_vars = list(self.Q)
        terminal_vars = list(self.Sigma)
        production = None
        start_symbol = self.q0

        keys = []
        values = []

        for key in self.delta:
            keys.append(key[0])
            values.append(key[1] + self.delta[key][0])

        production = dict.fromkeys(keys, list())

        for i in range(len(keys)):
            if len(production[keys[i]]) == 0:
                production[keys[i]] = [values[i]]
            else:
                production[keys[i]].append(values[i])

        return non_terminal_vars, terminal_vars, production, start_symbol







