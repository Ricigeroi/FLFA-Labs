import random
from D_FiniteAutomaton import D_FiniteAutomaton


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
                # Generate string choosing random production
                if symbol in self.non_terminal_vars:
                    new_string += random.choice(self.production[symbol])
                    print(" -> ", end='')
                else:
                    new_string += symbol
            # while exit point
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

        for element in final_states:
            states.add(element)

        for non_terminal in self.non_terminal_vars:
            states.add(non_terminal)
            for production in self.production[non_terminal]:
                for symbol in production:
                    if symbol in self.terminal_vars:
                        # Case for multiple delta from certain state
                        if (non_terminal, symbol) in transition:
                            if production in self.terminal_vars:
                                transition[(non_terminal, symbol)].append('F')
                            else:
                                transition[(non_terminal, symbol)].append(production[1:])
                        # General case
                        elif production in self.terminal_vars:
                            transition[(non_terminal, symbol)] = ['F']
                        else:
                            transition[(non_terminal, symbol)] = [production[1:]]
        print("_______________States________________")
        print(states)
        print("____________Transitions______________")
        for item in transition:
            print(item, "->", transition[item])
        return D_FiniteAutomaton(states, alphabet, transition, initial_state, final_states)

    def chomsky(self):
        flag = [0, 0, 0, 0]
        for rule in self.production:
            for prod in self.production[rule]:
                if len(rule) == 1:
                    if count_case_changes(prod) <= 1 and not prod.istitle():
                        if sum(1 for c in prod if c in self.non_terminal_vars) <= 1:
                            flag[3] = 1
                        else:
                            flag[3] = 0
                    else:
                        flag[2] = 1
                else:
                    if '$' not in prod:
                        flag[1] = 1
                    else:
                        flag[0] = 1
        return "Type " + str(flag.index(1))

def count_case_changes(s):
    count = 0
    previous_case = None
    for char in s:
        current_case = char.isupper()
        if previous_case is not None and current_case != previous_case:
            count += 1
        previous_case = current_case
    return count