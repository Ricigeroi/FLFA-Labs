import re

# Define the different token types along with their regex patterns
TOKEN_TYPES = [
    ('NUMBER', r'\d+(\.\d+)?'),  # Matches integers and float numbers
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLIER', r'\*'),
    ('DIVIDE', r'/'),
    ('POWER', r'\^'),
    ('LEFT_BRACKET', r'\('),
    ('RIGHT_BRACKET', r'\)'),
    ('VARIABLE', r'[a-zA-Z_]\w*'),  # Matches valid variable names
    ('EQUAL', r'='),
    ('COMMA', r','),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('MODULO', r'%'),
    ('LESS_THAN', r'<'),
    ('GREATER_THAN', r'>'),
    ('NOT_EQUAL', r'!='),
    ('AND', r'&&'),
    ('OR', r'\|\|'),
    ('NOT', r'!'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('WHILE', r'while'),
    ('FOR', r'for'),
    ('FUNCTION', r'function'),
    ('RETURN', r'return'),
    ('BEGIN', r'{'),
    ('END', r'}'),
]


class Lexer:
    # Initialize the lexer with the input text
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    # Advance the position and update the current character
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    # Skip whitespace characters
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Get the next token from the input text
    def get_next_token(self):
        # Skip any whitespace
        self.skip_whitespace()

        # Return None if end of input
        if self.current_char is None:
            return None

        # Check if the current character matches any of the token types
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(self.text[self.pos:])
            if match:
                # If matched, create a token of that type with the matched value
                value = match.group(0)
                token = (token_type, value)
                # Advance the position by the length of the matched value
                for _ in range(len(value)):
                    self.advance()
                # Return the token
                return token

        # If no match, print an error message and return None
        print(f'Invalid character: {self.current_char}')
        self.advance()
        return None

