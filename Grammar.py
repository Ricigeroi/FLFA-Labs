import random
from FiniteAutomaton import FiniteAutomaton


class Grammar:
    def __init__(self, non_terminal_vars, terminal_vars, production, start_symbol):
        self.non_terminal_vars = non_terminal_vars
        self.terminal_vars = terminal_vars
        self.production = production
        self.start_symbol = start_symbol

    def generate_string(self):
        actual_string = self.start_symbol
        while True:
            print(actual_string, end='')
            new_string = ""
            for symbol in actual_string:
                if symbol in self.non_terminal_vars:
                    new_string += random.choice(self.production[symbol])
                    print(" -> ", end='')
                else:
                    new_string += symbol
            if new_string == actual_string:
                break
            actual_string = new_string
        print()
        return actual_string

    def to_finite_automaton(self):
        states = set()
        alphabet = self.terminal_vars
        transition = {}
        initial_state = self.start_symbol
        final_states = ['F']

        for non_terminal in self.non_terminal_vars:
            states.add(non_terminal)
            for production in self.production[non_terminal]:
                for symbol in production:
                    if symbol in self.terminal_vars:
                        if (non_terminal, symbol) in transition:
                            transition[(non_terminal, symbol)].append('F')
                        elif production.islower():
                            transition[(non_terminal, symbol)] = ['F']
                        else:
                            transition[(non_terminal, symbol)] = [production[1:]]
        print("____________Transitions______________")
        for item in transition:
            print(item, "->", transition[item])
        return FiniteAutomaton(states, alphabet, transition, initial_state, final_states)
