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

    # method to eliminate the e-transition (just in my particular case)
    def eliminate_e(self):
        print(' ' * 48, "Eliminating e-transitions:")
        production = self.production.copy()
        Ne = []
        for prod in production:
            if '' in production[prod]:
                Ne.append(prod)

                # eliminate e-transition from P
                production[prod].remove('')

        # delete empty transitions
        to_delete = []
        for i in production.keys():
            if not production[i]:
                to_delete.append(i)
        for item in to_delete:
            production.pop(item)
            self.non_terminal_vars.remove(item)

        # simplify productions (ex: [A -> aB, B -> epsilon] ==> [A -> a])
        for item in Ne:
            print(item, '->', 'epsilon')
            for prod in production:
                for i in range(len(production[prod])):
                    production[prod][i] = production[prod][i].replace(item, '')
        self.production = production
        print("\nP' =", self.production)
        print('=' * 128)

    # method to eliminate renaming
    def eliminate_rename(self):
        print(' ' * 50, "Eliminating renaming:")
        for prod in self.production:
            for rule in self.production[prod]:
                if rule in self.non_terminal_vars:
                    print(prod, '->', rule)
                    self.production[prod].remove(rule)
                    self.production[prod].extend(self.production[rule])
        print("\nP\" =", self.production)
        print('=' * 128)

    # method to eliminate inaccessible symbols
    def eliminate_unreachable(self):
        print(' ' * 50, "Unreachable symbols:")
        reached = set()
        for var in self.non_terminal_vars:
            for prod in self.production:
                for rule in self.production[prod]:
                    if var in rule:
                        reached.add(var)

        unreached = []
        for item in list(self.production.keys()):
            if item not in reached:
                unreached.append(item)

        for item in unreached:
            self.production.pop(item)
            self.non_terminal_vars.remove(item)

        print('Inaccessible symbols =', unreached)
        print("\nP\"\" =", self.production)
        print('=' * 128)

    # method to eliminate nonproductive symbols
    def eliminate_nonproductive(self):
        """
            There is no need to implement this method since my case doesn't have any
            nonproductive symbols to eliminate

            P.S.: Thank God for this!
        """
        pass

    def convert_to_normal_form(self):
        """
        Method to convert a grammar to Chomsky normal form.
        A -> BC
        D -> i
        """
        # START: Eliminate the start symbol from right-hand sides
        print(' ' * 50, "Chomsky normal form:")
        self.non_terminal_vars.append('S0')
        dict = {'S0': ['S']}
        self.production = {**dict, **self.production}

        # TERM: Eliminate rules with nonsolitary terminals
        new_production = {}
        dict = {}
        counter = 0
        for prod in self.production:
            for rule in self.production[prod]:
                if len(rule) > 1:
                    for char in rule:
                        if char in self.terminal_vars and char not in new_production.values():
                            new_production[chr(70 + counter)] = char
                            dict[char] = chr(70 + counter)
                            counter += 1

        # Replacing terminals symbols with their new non-terminal symbol (ex: [S -> dB] ==> [F -> d] and [S -> FB])
        for item in dict.keys():
            for prod in self.production:
                for i in range(len(self.production[prod])):
                    if len(self.production[prod][i]) > 1:
                        self.production[prod][i] = self.production[prod][i].replace(item, dict[item])

        # BIN: Eliminate right-hand sides with more than 2 nonterminals
        print("New productions:\n", new_production, sep='')
        self.production = {**self.production, **new_production}
        counter = 1
        new_production = {}
        for prod in self.production:
            for rule in self.production[prod]:
                if len(rule) > 2:
                    print(prod, '->', 'X1X2')
                    new_production[prod] = 'X1X2'

        prod = list(self.production.keys())[1]
        for rule in self.production[prod]:
            if len(rule) > 2:
                while len(rule) > 2:
                    new_production[('X' + str(counter))] = rule[:2]
                    print(('X' + str(counter)), '->', rule[:2])
                    counter += 1
                    if len(rule[2:]) > 2:
                        new_production[('X' + str(counter))] = ('X' + str(counter + 1)) + rule[-1]
                        print(('X' + str(counter)), '->', ('X' + str(counter + 1)) + rule[-1])
                        counter += 1
                    rule = rule[2:]

        for prod in self.production:
            for rule in self.production[prod]:
                if len(rule) > 2:
                    self.production[prod].remove(rule)

        for prod in new_production:
            if prod in self.production:
                self.production[prod].append(new_production[prod])
            else:
                self.production[prod] = new_production[prod]

        print("\nP normal =", self.production)
        print('=' * 128)


def count_case_changes(s):
    count = 0
    previous_case = None
    for char in s:
        current_case = char.isupper()
        if previous_case is not None and current_case != previous_case:
            count += 1
        previous_case = current_case
    return count
