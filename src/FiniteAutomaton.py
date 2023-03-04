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
        # Initialize the lists of non-terminal and terminal variables
        non_terminal_vars = list(self.Q)
        terminal_vars = list(self.Sigma)

        # Initialize the production rules dictionary
        production = {}

        # Add the start symbol
        start_symbol = self.q0

        # Iterate over all the transitions in the FA
        for transition, next_states in self.delta.items():
            # Extract the source state, symbol and destination state from the transition tuple
            src_state, symbol = transition

            # If the destination state is an accepting state, add a production rule to generate the empty string
            if next_states[0] in self.F:
                if src_state not in production:
                    production[src_state] = []
                production[src_state].append('')

            # Add a production rule for the current transition
            if src_state not in production:
                production[src_state] = []
            dest_state = next_states[0]
            production[src_state].append(symbol + dest_state)

            # If there are multiple next states, add epsilon productions for each of them
            for state in next_states[1:]:
                if src_state not in production:
                    production[src_state] = []
                production[src_state].append(symbol + state)

        # Return the non-terminal variables, terminal variables, production rules and start symbol as a tuple
        return (non_terminal_vars, terminal_vars, production, start_symbol)



