# LAB 5 Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Bardier Andrei

----
<details>
  <summary><h2>Theory</h2></summary>
    An Abstract Syntax Tree (AST) and a parser are two essential components in the field of computer science, 
    particularly in the domain of programming languages and compilers. They play crucial roles in the analysis and 
    interpretation of code.
    <br>
    <br>
    A parser is a software module that takes source code as input and verifies its syntactic correctness according to 
    a specified grammar or language rules. It breaks down the code into a structured format known as a parse tree, 
    representing the hierarchical relationship of the code elements. The parse tree encompasses all the grammatical 
    details of the code but may include redundant information.
    <br>
    <br>
    To address this, an AST is derived from the parse tree. The AST captures the essential semantic meaning 
    of the code while discarding extraneous details. It is a more compact representation that focuses on the 
    program's structure and logic. The AST forms a tree-like structure, with each node representing a specific construct, 
    such as a function declaration, an if statement, or an expression.
    <br>
    <br>
    The AST is commonly used in various stages of the compilation process, including optimization, code generation, 
    and static analysis. It serves as an intermediate representation that facilitates efficient analysis and 
    transformation of the code.
    <br>
    <br>
    In summary, the parser and AST are fundamental tools in language processing. While the parser verifies the syntax 
    of the code, the AST extracts the meaningful essence, enabling further analysis and manipulation of the code. 
    Together, they empower the development of sophisticated compilers, interpreters, and other language-related tools.
</details>
<details>
  <summary><h2>Objective</h2></summary>
  
  1. Get familiar with parsing, what it is and how it can be programmed [1].
  2. Get familiar with the concept of AST [2].
  3. In addition to what has been done in the 3rd lab work do the following:
     1. In case you didn't have a type that denotes the possible types of tokens you need to:
        1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
        2. Please use regular expressions to identify the type of the token.
     2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
     3. Implement a simple parser program that could extract the syntactic information from the input text.
</details>


## Implementation description
In order to accomplish this laboratory task, I added a Parser class to my project.  

1. Initialize the Parser object by receiving a lexer object, which is responsible for tokenizing the input. I set the lexer attribute and obtain the first token from the lexer using get_next_token() method, storing it in the current_token attribute.
  ```python
      def __init__(self, lexer):
          self.lexer = lexer
          self.current_token = self.lexer.get_next_token()
  ```

2. Parser raise an exception with the provided error message. This method is called when an unexpected token is encountered during parsing.
  ```python
      def error(self, message):
          raise Exception(message)
  ```
3. Parser consumes the current token if its type matches the expected token_type. If they match, I obtain the next token from the lexer and update the current_token attribute. If they don't match, I raise an exception with an error message indicating the unexpected token.
  ```python
      def eat(self, token_type):
          if self.current_token and self.current_token[0] == token_type:
              self.current_token = self.lexer.get_next_token()
          else:
              self.error(f'Unexpected token: {self.current_token[0]}')
  ```
4. I handle the lowest level of expression parsing, which includes numbers, variables, parentheses, and conditional expressions (if statements). I check the type of the current token and call the appropriate methods or consume the token accordingly. I return a dictionary representing the parsed factor.
```python
    def factor(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return {'type': 'NUMBER', 'value': token[1]}
        elif token[0] == 'VARIABLE':
            self.eat('VARIABLE')
            return {'type': 'VARIABLE', 'name': token[1]}
        elif token[0] == 'LEFT_BRACKET':
            self.eat('LEFT_BRACKET')
            expr = self.expr()
            self.eat('RIGHT_BRACKET')
            return expr
        elif token[0] == 'IF':
            self.eat('IF')
            condition = self.expr()
            self.eat('BEGIN')
            if_branch = self.statements()
            self.eat('END')
            else_branch = None
            if self.current_token and self.current_token[0] == 'ELSE':
                self.eat('ELSE')
                self.eat('BEGIN')
                else_branch = self.statements()
                self.eat('END')
            return {'type': 'IF', 'condition': condition, 'if_branch': if_branch, 'else_branch': else_branch}
        else:
            self.error(f'Unexpected token: {token[0]}')
```
4. I handle exponentiation operations in the expression parsing. I first call the factor() method to parse the base expression. If the current token is a power operator, I create a dictionary representing the power operation and recursively call factor() to parse the exponent expression. I update the expr variable and return the resulting dictionary.
```python
 def power(self):
        expr = self.factor()
        while self.current_token and self.current_token[0] == 'POWER':
            token = self.current_token
            self.eat('POWER')
            expr = {'type': 'POWER', 'left': expr, 'right': self.factor()}
        return expr
```
5. I handle multiplication, division, and modulo operations in the expression parsing. Similar to power(), I first call power() to parse the left operand. Then, while the current token is a multiplication, division, or modulo operator, I create a dictionary representing the respective operation and recursively call power() to parse the right operand. I update the expr variable and return the resulting dictionary.
```python
    def term(self):
        expr = self.power()
        while self.current_token and (self.current_token[0] == 'MULTIPLIER' or self.current_token[0] == 'DIVIDE' or self.current_token[0] == 'MODULO'):
            token = self.current_token
            if token[0] == 'MULTIPLIER':
                self.eat('MULTIPLIER')
            elif token[0] == 'DIVIDE':
                self.eat('DIVIDE')
            elif token[0] == 'MODULO':
                self.eat('MODULO')
            expr = {'type': token[0], 'left': expr, 'right': self.power()}
        return expr
```
6. I handle addition and subtraction operations in the expression parsing. Similar to term(), I first call term() to parse the left operand. Then, while the current token is a plus or minus operator, I create a dictionary representing the respective operation and recursively call term() to parse the right operand. I update the expr variable and return the resulting dictionary.
```python
    def expr(self):
        expr = self.term()
        while self.current_token and (self.current_token[0] == 'PLUS' or self.current_token[0] == 'MINUS'):
            token = self.current_token
            if token[0] == 'PLUS':
                self.eat('PLUS')
            elif token[0] == 'MINUS':
                self.eat('MINUS')
            expr = {'type': token[0], 'left': expr, 'right': self.term()}
        return expr
```
7. I initiate the parsing process by calling expr(). This method returns the parsed expression.
```python
    def parse(self):
        return self.expr()
```

## Examples of input and output
Input:
```
2 + (2 + 3)
```
Output:
```json
"C:/Users/andre/OneDrive/Рабочий стол/FLFA-Labs/src/main.py"
{
  "type": "PLUS", 
  "left": 
  {
      "type": "NUMBER", 
      "value": "2"
  }, 
  "right": 
  {
    "type": "PLUS", 
    "left": 
    {
      "type": 
      "NUMBER", 
      "value": "2"
    }, 
    "right": 
    {
      "type": "NUMBER", 
      "value": "3"
    }
  }
}
```

Input:
```
(2 + 2) * 2 / 3 - 4
```
Output:
```json
"C:/Users/andre/OneDrive/Рабочий стол/FLFA-Labs/src/main.py"
{
  "type": "PLUS", 
  "left": 
  {
    "type": "NUMBER", 
    "value": "2"
  }, 
  "right": 
  {
    "type": "PLUS", 
      "left": 
      {
        "type": "NUMBER", 
        "value": "2"
      }, 
      "right": 
      {
        "type": "NUMBER", 
        "value": "3"
      }
  }
}
```
Input:
```
if (a > b)
{
    a = 1;
}
```
Output:
```json
{
  "type": "IF",
    "condition": {
        "type": "operation",
        "operator": "GREATER_THAN",
        "left": {
            "type": "VARIABLE",
            "value": "a"
        },
        "right": {
            "type": "VARIALBE",
            "value": "b"
        }
    },
    "body": {
        "type": "assign",
        "variable": "a",
        "value": 1
    },
}
```
Input:
```
3 * (a / b) + 2 * c"
```
Output:
```
"C:/Users/andre/OneDrive/Рабочий стол/FLFA-Labs/src/main.py"
{
  "type": "PLUS", 
  "left": 
  {
    "type": "MULTIPLIER", 
    "left": 
    {
      "type": "NUMBER", 
      "value": "3"
    }, 
    "right": 
    {
      "type": "DIVIDE", 
      "left": 
      {
        "type": "VARIABLE", 
        "name": "a"
      }, 
      "right": 
      {
        "type": "VARIABLE",
        "name": "b"
      }
    }
  }, 
  "right":
  {
    "type": "MULTIPLIER", 
    "left": 
    {
      "type": "NUMBER", 
      "value": "2"
    }, 
    "right": 
    {
      "type": "VARIABLE", 
      "name": "c"
    }
  }
}
```

## Conclusions / Screenshots / Results

In conclusion, the implementation of an Abstract Syntax Tree (AST) and parser plays a crucial role in the field of programming language processing and interpretation. The AST serves as an intermediary representation of source code, capturing its structure and semantics in a hierarchical form. It enables easier manipulation, analysis, and transformation of the code.
<br><br>
The parser, working in conjunction with a lexer, takes a stream of tokens and constructs the AST according to a specified grammar. It enforces syntactic rules and resolves ambiguities, ensuring that the code is well-formed and conforms to the language's syntax.
<br><br>
By using an AST, developers can perform a wide range of tasks, such as code generation, static analysis, optimization, and interpretation. The AST provides a structured representation that facilitates traversing and manipulating the code, making it easier to implement various language features and optimizations.
<br><br>
Mоreover, the separation between lexical analysis and syntactic analysis achieved thrоugh the cоmbinatiоn of lexer and parser prоmоtes mоdularity and cоde reuse. Changes in the grammar or lexical rules can be lоcalized tо the respective cоmpоnents, minimizing the impact оn the оverall system.
<br><br>
Overall, AST and parser implementations are fоundatiоnal techniques in language prоcessing, enabling the develоpment оf cоmpilers, interpreters, and оther language-related tооls. They empower develоpers tо create pоwerful and efficient systems fоr wоrking with prоgramming languages, facilitating cоde understanding, transformatiоn, and executiоn.

