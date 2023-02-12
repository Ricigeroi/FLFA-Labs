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
                if len(next_states) > 1 and index == len(input_string) - 1:
                    current_state = next_states[1]
                else:
                    current_state = next_states[0]
            else:
                return False
        return current_state in self.F
