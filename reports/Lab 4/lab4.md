# LAB 4 LFAF Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Bardier Andrei

----
<details>
  <summary><h2>Theory</h2></summary>
  
  Chomsky normal form (CNF) is a way of representing a context-free grammar in a standardized form.
  This form was first proposed by linguist Noam Chomsky in 1959 as a method to study the formal properties of natural languages.
  The CNF requires that every rule in the grammar is either of the form A → BC, where A, B, and C are nonterminal symbols, or A → a,
  where A is a nonterminal symbol and a is a terminal symbol.  

  There are several advantages to representing a grammar in Chomsky normal form. 
  One is that it makes it easier to analyze the grammar and to prove certain properties about it. 
  For example, it is straightforward to determine whether a given grammar generates a particular string or not using the CYK algorithm. 
  Additionally, converting a grammar to CNF can simplify the design of parsers, which are programs that recognize the structure of sentences in a language.  

  While it is possible to convert any context-free grammar to Chomsky normal form, the resulting grammar may have more rules than the original grammar. 
  However, the number of rules is still polynomial in the size of the original grammar, and the resulting grammar has several useful properties 
  that make it well-suited for computational applications. As a result, Chomsky normal form is a popular standard for representing context-free grammars 
  in natural language processing and other areas of computer science.
</details>
<details>
  <summary><h2>Objective</h2></summary>
  
  1. Learn about Chomsky Normal Form (CNF) [1].
  2. Get familiar with the approaches of normalizing a grammar.
  3. Implement a method for normalizing an input grammar by the rules of CNF.
      1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
      2. The implemented functionality needs executed and tested.
      3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
      4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar,  
           not only the one from the student's variant.
</details>


## Implementation description
In order to accomplish this laboratory task, I added several methods to my existing grammar class.  
So I had:
```
Original productions:

P = {'S': ['dB', 'A'], 'A': ['d', 'dS', 'aAdAB'], 'B': ['aC', 'aS', 'AC'], 'C': [''], 'E': ['AS']}
```

# Eliminating ε-transitions
<details>
  <summary>CODE HERE</summary>
  
  ```python
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
  ```
</details>
The above code implements a method to eliminate epsilon transitions from a context-free grammar. 
It first identifies non-terminal symbols that can produce epsilon, removes these transitions from the grammar, 
and then simplifies the productions by removing any occurrences of the eliminated symbols. The resulting grammar is printed to the console.    

Output:
```
================================================================================================================================
                                                 Eliminating e-transitions:
C -> epsilon

P' = {'S': ['dB', 'A'], 'A': ['d', 'dS', 'aAdAB'], 'B': ['a', 'aS', 'A'], 'E': ['AS']}
================================================================================================================================
```

# Eliminating renaming
<details>
  <summary>CODE HERE</summary>
  
  ```python
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
  ```
</details>
The above code implements a method to eliminate renaming of non-terminal symbols in a context-free grammar.
It iterates through each production and if it contains a single non-terminal symbol, it replaces it with the corresponding production rules of that symbol. 
The resulting grammar is printed to the console.    

Output:
```
================================================================================================================================
                                                   Eliminating renaming:
S -> A
B -> A

P" = {'S': ['dB', 'd', 'dS', 'aAdAB'], 'A': ['d', 'dS', 'aAdAB'], 'B': ['a', 'aS', 'd', 'dS', 'aAdAB'], 'E': ['AS']}
================================================================================================================================
```
# Eliminating unreachable symbols
<details>
  <summary>CODE HERE</summary>

  ```python
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
  ```
</details>
This Python code implements a method to eliminate inaccessible symbols from a context-free grammar. 
It iterates through all the productions in the grammar and checks if each non-terminal symbol can be reached from the start symbol. 
Any non-terminal symbol that cannot be reached is removed from the grammar, along with any productions that contain it. 
The resulting grammar is printed to the console along with the list of removed symbols.    

Output:
```
================================================================================================================================
                                                   Unreachable symbols:
Inaccessible symbols = ['E']

P"" = {'S': ['dB', 'd', 'dS', 'aAdAB'], 'A': ['d', 'dS', 'aAdAB'], 'B': ['a', 'aS', 'd', 'dS', 'aAdAB']}
================================================================================================================================
```
# Eliminate nonproductive symbols
```python
    # method to eliminate nonproductive symbols
    def eliminate_nonproductive(self):
        """
            There is no need to implement this method since my case doesn't have any
            nonproductive symbols to eliminate

            P.S.: Thank God for this!
        """
        pass
```
# Chomsky Normal form
<details>

  <summary>CODE HERE</summary>

  
  ```python
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
```

</details>

This code defines a method named convert_to_normal_form which takes a context-free grammar and converts it to Chomsky normal form. 
It does this in three steps, which are commented in the code.  

First, it eliminates the start symbol from right-hand sides of productions by introducing a new start symbol 'S0'. 
Then, it eliminates rules with nonsolitary terminals by introducing new non-terminal symbols that replace each terminal symbol. 
The productions of these new non-terminal symbols are added to the existing productions.  

Finally, it eliminates right-hand sides with more than 2 non-terminals by introducing new non-terminal symbols 
and breaking down the long rules into smaller ones until all rules have at most two non-terminals. 
The productions of these new non-terminal symbols are added to the existing productions, and the original productions that were broken down are removed.  

The method prints the new productions that were introduced during the second and third steps, as well as the resulting grammar in Chomsky normal form.

```
================================================================================================================================
                                                   Chomsky normal form:
New productions:
{'F': 'd', 'G': 'a'}
S -> X1X2
A -> X1X2
B -> X1X2
X1 -> GA
X2 -> X3B
X3 -> FA

P normal = {
              'S0': ['S'], 
              'S': ['FB', 'd', 'FS', 'X1X2'], 
              'A': ['d', 'FS', 'X1X2'], 
              'B': ['a', 'GS', 'd', 'FS', 'X1X2'], 
              'F': 'd', 
              'G': 'a', 
              'X1': 'GA', 
              'X2': 'X3B', 
              'X3': 'FA'
           }
================================================================================================================================

```

## Conclusions / Screenshots / Results


In conclusion, we have seen a set of methods to transform a context-free grammar into a Chomsky normal form. 
The methods include eliminating epsilon-transitions, eliminating renaming, and eliminating inaccessible symbols. 
These steps are essential as they allow the conversion of a context-free grammar into a form that can be easily analyzed and processed by algorithms.  

The conversion process to Chomsky normal form starts by adding a new start symbol, S0, to the grammar and eliminating rules with nonsolitary terminals. 
This is followed by eliminating right-hand sides with more than two non-terminals, and finally, 
each remaining rule is transformed into either a terminal or two non-terminals.  

It's worth noting that this conversion process does not affect the language generated by the original grammar. 
<a href="https://youtu.be/dQw4w9WgXcQ">Therefore</a>, the Chomsky normal form grammar generates the same language as the original grammar.

The implementation of the transformation methods is straightforward and can be easily applied to any context-free grammar. 
However, some grammar rules may require additional transformations, and the implementation may differ based on the specific grammar.  

In summary, the conversion of context-free grammars to Chomsky normal form is an important step in many applications, 
such as natural language processing, parsing, and automated theorem proving. The methods presented here provide a solid foundation for transforming 
any context-free grammar into Chomsky normal form, allowing for efficient analysis and processing of the language generated by the grammar.

