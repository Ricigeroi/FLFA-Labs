from Grammar import Grammar

if __name__ == "__main__":
    Vn = ["S", "D", "R"]
    Vt = ["a", "b", "c", "d", "f"]
    P = {
        "S": ["aS", "bD", "fR"],
        "D": ["cD", "dR", "d"],
        "R": ["bR", "f"]
    }

    S = "S"
    grammar = Grammar(Vn, Vt, P, S)
    finite_automaton = grammar.to_finite_automaton()

    print("__________Generated strings___________")
    for i in range(5):
        string = grammar.generate_string()
        print("Parsing:", finite_automaton.string_belongs_to_language(string))
    print("=================================================")
    print(finite_automaton.string_belongs_to_language("bccccdf"))
