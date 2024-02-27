class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def parse(self):
        return self.expr()

    def expr(self):
        left = self.term()

        while self.current_token and self.current_token in ['+', '-']:
            operator = self.current_token
            self.advance()
            right = self.term()
            left = (operator, left, right)

        return left

    def term(self):
        left = self.factor()

        while self.current_token and self.current_token in ['*', '/']:
            operator = self.current_token
            self.advance()
            right = self.factor()
            left = (operator, left, right)

        return left

    def factor(self):
        if self.current_token == '(':
            self.advance()
            result = self.expr()
            if self.current_token != ')':
                raise SyntaxError('Expected closing parenthesis')
            self.advance()
            return result
        elif self.current_token.isdigit():
            result = int(self.current_token)
            self.advance()
            return result
        else:
            raise SyntaxError('Invalid token')

# Example usage
tokens = ['5', '+', '2', '+', '3', '*', '2']
parser = Parser(tokens)
result = parser.parse()
print(result)  # Output: ('+', 5, ('*', 3, 2))

#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.current_token = None
#         self.index = -1
#         self.advance()

#     def advance(self):
#         self.index += 1
#         if self.index < len(self.tokens):
#             self.current_token = self.tokens[self.index]
#         else:
#             self.current_token = None

#     def parse(self):
#         return self.expr()

#     def expr(self):
#         result = self.term()

#         while self.current_token and self.current_token in ['+', '-']:
#             if self.current_token == '+':
#                 self.advance()
#                 result += self.term()
#             elif self.current_token == '-':
#                 self.advance()
#                 result -= self.term()

#         return result

#     def term(self):
#         result = self.factor()

#         while self.current_token and self.current_token in ['*', '/']:
#             if self.current_token == '*':
#                 self.advance()
#                 result *= self.factor()
#             elif self.current_token == '/':
#                 self.advance()
#                 result /= self.factor()

#         return result

#     def factor(self):
#         if self.current_token == '(':
#             self.advance()
#             result = self.expr()
#             if self.current_token != ')':
#                 raise SyntaxError('Expected closing parenthesis')
#             self.advance()
#             return result
#         elif self.current_token.isdigit():
#             result = int(self.current_token)
#             self.advance()
#             return result
#         else:
#             raise SyntaxError('Invalid token')

# # Example usage
# # tokens = ['(', '5', '+', '3', ')', '*', '2']
# tokens = ['5', '+', '(','3', '*', '2']
# parser = Parser(tokens)
# result = parser.parse()
# print(result)  # Output: 16