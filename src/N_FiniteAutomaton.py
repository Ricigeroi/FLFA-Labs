from D_FiniteAutomaton import D_FiniteAutomaton
from Grammar import Grammar
import networkx as nx
import matplotlib.pyplot as plt


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
        for item in self.delta.values():
            if len(item) > 1:
                return 'NFA'
        return 'DFA'

    def nfa2dfa(self):
        dfa_F = []
        dfa_delta = {}
        dfa_Q = [[self.q0]]

        for states in dfa_Q:
            for s in states:
                new_states = []
                T_states = []
                for c in self.Sigma:
                    if (s, c) in self.delta.keys():
                        new_states.append(self.delta[(s, c)])
                        T_states.append(c)
                for ns in new_states:
                    if ns and ns not in dfa_Q:
                        dfa_Q.append(ns)
                for i in range(len(new_states)):
                    if new_states[i]:
                        dfa_delta[(tuple(states), T_states[i])] = new_states[i]

        return D_FiniteAutomaton(dfa_Q, self.Sigma, self.q0, dfa_F, dfa_delta)

    def show_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.Q)

        for t in self.delta:
            for s in self.delta[t]:
                graph.add_edge(t[0], s, label=t[1])

        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edge_labels(graph, pos)

        plt.show()
