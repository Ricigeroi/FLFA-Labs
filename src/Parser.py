class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(message)

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Unexpected token: {self.current_token[0]}')

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

    def power(self):
        expr = self.factor()
        while self.current_token and self.current_token[0] == 'POWER':
            token = self.current_token
            self.eat('POWER')
            expr = {'type': 'POWER', 'left': expr, 'right': self.factor()}
        return expr

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

    def parse(self):
        return self.expr()
