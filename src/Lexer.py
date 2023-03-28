import re

# Define token types
TOKEN_TYPES = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLIER', r'\*'),
    ('DIVIDE', r'/'),
    ('LEFT_BRACKET', r'\('),
    ('RIGHT_BRACKET', r'\)'),
    ('VARIABLE', r'[a-zA-Z_]\w*'),
    ('EQUAL', r'=')
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

        # If no match, raise an exception
        raise Exception(f'Invalid character: {self.current_char}')
