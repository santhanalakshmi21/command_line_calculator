import sys
import re

# Define the token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        text = self.text

        if self.pos >= len(text):
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            value = 0
            while self.pos < len(text) and text[self.pos].isdigit():
                value = value * 10 + int(text[self.pos])
                self.pos += 1

            return Token(INTEGER, value)

        if current_char == '+':
            self.pos += 1
            return Token(PLUS, '+')

        if current_char == '-':
            self.pos += 1
            return Token(MINUS, '-')

        if current_char == '*':
            self.pos += 1
            return Token(MULTIPLY, '*')

        if current_char == '/':
            self.pos += 1
            return Token(DIVIDE, '/')

        if current_char == '(':
            self.pos += 1
            return Token(LPAREN, '(')

        if current_char == ')':
            self.pos += 1
            return Token(RPAREN, ')')

        self.error()

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result = result * self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)
if __name__ == '__main__':
    main()

