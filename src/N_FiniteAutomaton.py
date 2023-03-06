from D_FiniteAutomaton import D_FiniteAutomaton
from Grammar import Grammar
from graphviz import Digraph


class N_FiniteAutomaton:
    def __init__(self, Q, Sigma, q0, delta, F):
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.delta = delta
        self.F = F

    def string_belongs_to_language(self, string):
        current_state = self.q0

        for char in string:
            if (current_state, char) in self.delta:
                next_states = self.delta[(current_state, char)]
                if not next_states:
                    return False
                current_state = next_states[0]
            else:
                return False

        return current_state in self.F

    def to_grammar(self):
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
        is_deterministic = True

        # Check if there is more than one transition from a state with the same symbol
        for q in self.Q:
            transitions = {}
            for (state, symbol), next_states in self.delta.items():
                if state == q:
                    if symbol in transitions:
                        is_deterministic = False
                        break
                    else:
                        transitions[symbol] = next_states
        if is_deterministic:
            return "NFA"
        else:
            return "DFA"

    def nfa2dfa(self):
        dfa_F = []
        dfa_delta = {}
        dfa_Q = [[self.q0]]

        for states in dfa_Q:
            for s in self.Sigma:
                new_states = []
                for q in states:
                    if (q, s) in self.delta:
                        new_states += self.delta[(q, s)]
                new_states = list(set(new_states))

                if new_states:
                    dfa_delta[(tuple(states), s)] = new_states
                    if new_states not in dfa_Q:
                        dfa_Q.append(new_states)

        for states in dfa_Q:
            for q in states:
                if q in self.F:
                    dfa_F.append(states)
                    break

        return D_FiniteAutomaton(dfa_Q, self.Sigma, [self.q0], dfa_F, dfa_delta)

    def draw_graph(self):
        dot = Digraph()

        # add nodes
        for q in self.Q:
            dot.node(str(q))

        # add initial state
        dot.attr('node', shape='none')
        dot.edge('', str(self.q0), arrowhead='normal')

        # add final states
        dot.attr('node', shape='doublecircle')
        for q in self.F:
            dot.node(str(q))

        # add transitions
        dot.attr('node', shape='circle')
        dot.attr('edge', arrowhead='normal')
        for (q, a), qs in self.delta.items():
            for q_ in qs:
                dot.edge(str(q), str(q_), label=a)

        return dot
