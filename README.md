# LAB 1 LFAF

### Course: Formal Languages & Finite Automata
### Author: Bardier Andrei

----

## Theory
Regular grammar and finite automata are two important concepts in computer science that are used to describe and recognize patterns in strings and languages.

A regular grammar is a set of rules for generating strings in a particular language. It consists of a set of terminals, which are the basic symbols used to build strings, and a set of non-terminals, which are used to describe the structure of the strings. The grammar also includes production rules, which specify how to transform non-terminals into terminals.

A finite automaton, on the other hand, is a mathematical model for recognizing strings in a language. It consists of a set of states, a set of input symbols, a transition function, a start state, and a set of accept states. The automaton processes a string by starting at the start state and following the transition function for each symbol in the string, until it reaches an accept state or a non-accept state.

Both regular grammar and finite automata can be implemented in programming languages for various purposes. For example, they can be used to validate the syntax of programming languages, to recognize patterns in data, or to parse text.

In programming, regular grammar can be implemented as a parser, which takes a string as input and uses the rules of the grammar to determine if it is a valid string in the language described by the grammar. If the string is valid, the parser can also produce a parse tree, which represents the structure of the string.

Finite automata can also be implemented in programming languages, typically as a finite state machine. A finite state machine is a program that takes inputs and changes its behavior based on the inputs and its current state. For example, a finite state machine can be used to implement a simple calculator that takes inputs of numbers and arithmetic operators and outputs the result.

In conclusion, regular grammar and finite automata are powerful concepts that can be used to describe and recognize patterns in strings and languages. They can be implemented in programming languages for various purposes, such as validating the syntax of programming languages, recognizing patterns in data, or parsing text.


## Objectives:
1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

    a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

    b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

    c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
    
    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;
    
## Implementation description

The given program is an implementation of a Deterministic Finite Automaton (DFA) for a given context-free grammar. A DFA is a finite state machine that can accept or reject a string based on the transitions between the states and the input symbols.

The program uses two classes, Grammar and FiniteAutomaton, to represent the context-free grammar and the DFA respectively. The Grammar class takes the non-terminal variables (Vn), terminal variables (Vt), production rules (P), and the start symbol (S) as inputs, and it generates strings based on the given context-free grammar using a recursive function "generate_string". The class also converts the context-free grammar into a DFA using the "to_finite_automaton" function.

The FiniteAutomaton class takes five inputs: the set of states (Q), the alphabet (Sigma), the transition function (delta), the initial state (q0), and the set of final states (F). The class has a function "string_belongs_to_language" to check if the given input string belongs to the language defined by the DFA.

The main function generates 5 random strings from the grammar, checks if the strings belong to the language defined by the DFA, and finally tests the validation of a fixed string.


* Code snippets from your files.

```
 Vn = ["S", "D", "R"]
 Vt = ["a", "b", "c", "d", "f"]
 
 # Productions
 P = {
        "S": ["aS", "bD", "fR"],
        "D": ["cD", "dR", "d"],
        "R": ["bR", "f"]
    }
    
S = "S"
```
Output example:
```
____________Transitions______________
('S', 'a') -> ['S']
('S', 'b') -> ['D']
('S', 'f') -> ['R']
('D', 'c') -> ['D']
('D', 'd') -> ['R', 'F']
('R', 'b') -> ['R']
('R', 'f') -> ['F']
__________Generated strings___________
S -> bD -> bcD -> bcdR -> bcdf
Validation: True

S -> fR -> ff
Validation: True

S -> aS -> aaS -> aaaS -> aaabD -> aaabdR -> aaabdf
Validation: True

S -> bD -> bcD -> bccD -> bccdR -> bccdbR -> bccdbbR -> bccdbbbR -> bccdbbbbR -> bccdbbbbbR -> bccdbbbbbf
Validation: True

S -> aS -> aaS -> aaaS -> aaabD -> aaabd
Validation: True

_________String validation___________
String: bdbbfd
Validation: False

Process finished with exit code 0

```




## Conclusions

In conclusion, regular grammars and finite automatons are important concepts in computer science that are used to describe and recognize patterns in strings and languages. They provide a set of rules for generating strings and a mathematical model for recognizing strings respectively. These concepts can be implemented in programming languages such as Python for various purposes such as syntax validation, pattern recognition, and text parsing.

In this lab, the students were tasked with implementing a type/class for their given grammar, generating 5 valid strings from the language expressed by their given grammar, converting an object of type Grammar to an object of type Finite Automaton, and checking if an input string can be obtained via the state transition from the finite automaton. This lab serves as the initial setup for the evolving project that the students will work on throughout the semester.

The implementation of regular grammars and finite automatons in Python highlights the versatility and power of these concepts in computer science. With the ability to perform various operations and tasks related to string manipulation, regular grammars and finite automatons are an indispensable tool for computer scientists and programmers alike.
![FA](https://user-images.githubusercontent.com/90408983/218338895-e56ed245-1552-4ba2-a473-db6b1cfc694f.png)


## References
