# from source.SyntaxAnalyzer.grammar import Grammar


class Parser1:
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

# # Example usage
# tokens = ['5', '+', '2', '+', '3', '*', '2']
# parser = Parser(tokens)
# result = parser.parse()
# print(result)  # Output: ('+', 5, ('*', 3, 2))

# t5

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



# import parser_sheesh as parse
# from source.LexicalAnalyzer.tokenclass import Token

# sample=[Token("sheesh", "sheesh", 1, 5), Token("(", "(" , 1, 6), Token(")", ")", 1, 9), Token("{", "{", 1, 4), Token("statement1", "text", 2, 1), Token("statement2", "text", 2, 2),  Token("}", "}", 3, 5)]             
# s=parse.Parser(sample)
# p=parse.SheeshDec(s)
# p.parse()
# print(p)  


""" 
algorithm for syntax checker:
def parse(tokens): #starts with program
while does not match, expand. if ends but no match, try other productions

def expand(token, rule): #expands the rule                                      

 """

class LL1Parser:
    def __init__(self, grammar):
        self.cfg = grammar
        self.first_sets ={}
        self.calculate_first_sets()
        self.follow_sets = {}
        self.calculate_follow_sets()

    def calculate_first_sets(self):
        first_sets = {}
        for non_terminal in self.cfg:
            first_sets[non_terminal] = self.calculate_first_set(non_terminal)
        return first_sets

    def calculate_first_set(self, non_terminal):
        first_set = set()
        for production in self.cfg[non_terminal]:
            first_set |= self.calculate_first(production)
        return first_set

    def calculate_first(self, production):
        first_set = []
        for symbol in production:
            
            if symbol is None:
                continue
            if symbol not in self.cfg:
                first_set.append(symbol)
                break
            first_set |= self.first_sets[symbol]
            if None not in self.first_sets[symbol]:
                break
        return first_set

    def calculate_follow_sets(self):
        follow_sets = {non_terminal: set() for non_terminal in self.cfg}
        follow_sets[next(iter(self.cfg))] = {'$'}
        changed = True
        while changed:
            changed = False
            for non_terminal in self.cfg:
                for production in self.cfg[non_terminal]:
                    follow_sets[non_terminal] |= self.calculate_follow(production, follow_sets)
            for non_terminal in self.cfg:
                old_follow_set = set(follow_sets[non_terminal])
                for production in self.cfg[non_terminal]:
                    follow_sets[non_terminal] |= self.calculate_follow(production, follow_sets)
                if old_follow_set != follow_sets[non_terminal]:
                    changed = True
        return follow_sets

    def calculate_follow(self, production, follow_sets):
        follow_set = set()
        for i, symbol in enumerate(production):
            if symbol is None:
                continue
            if symbol in self.cfg:
                follow_set |= self.calculate_first(production[i + 1:])
                if None in self.calculate_first(production[i + 1:]):
                    follow_set -= {None}
                    follow_set |= follow_sets[symbol]
        return follow_set

    def parse(self, tokens):
        self.tokens = tokens + ['$']
        self.current_token = 0
        self.stack = ['$', next(iter(self.cfg))]
        while self.stack:
            top = self.stack[-1]
            if top in self.cfg:
                production = self.get_production(top)
                if production:
                    self.stack.pop()
                    self.stack.extend(reversed(production))
                else:
                    raise SyntaxError(f"No production for non-terminal '{top}'")
            elif top == self.tokens[self.current_token]:
                self.stack.pop()
                self.current_token += 1
            elif top == '$':
                return "Valid program"
            else:
                raise SyntaxError(f"Mismatched token: expected '{top}', found '{self.tokens[self.current_token]}'")
        return "Invalid program"

    def get_production(self, non_terminal):
        for production in self.cfg[non_terminal]:
            if self.tokens[self.current_token] in self.calculate_first(production) or \
                    (None in self.calculate_first(production) and self.tokens[self.current_token] in self.follow_sets[non_terminal]):
                return production
        return None

from source.LexicalAnalyzer.tokenclass import Token
from source.SyntaxAnalyzer import parser2 as parser

sample=[Token("sheesh", "sheesh", 1, 5), Token("(", "(" , 1, 6), Token(")", ")", 1, 9), Token("{", "{", 1, 4), Token("statement1", "text", 2, 1), Token("statement2", "text", 2, 2),  Token("}", "}", 3, 5)]           
q=[Token("sheesh", "from", 1, 5), Token("(", "(" , 1, 6), Token(")", ")", 1, 9), Token("{", "{", 1, 4), Token("statement1", "text", 2, 1), Token("statement2", "text", 2, 2),  Token("}", "}", 3, 5)]           

sample2=[Token("sheesh", "use", 1, 1), Token("ewan", "Identifier" , 1, 1), Token(" from", "from", 1, 1), Token("{", "Identifier", 1, 1), Token("statement1", "#", 2, 1), Token("sheesh", "use", 1, 2), Token("ewan", "Identifier" , 1, 2), Token(" from", "from", 1, 2), Token("{", "Identifier", 1, 2), Token("statement1", "#", 2, 2),]           
sample3=[Token("sheesh", "sheesh", 1, 1), Token("(", "(", 2, 1), Token(")", ")", 3, 1), Token("{", "{", 4, 1), Token("whole", "whole", 1, 2), Token("y", "Identifier", 2, 2), Token("=", "=", 3, 2),   Token("5", "Dec", 4, 2), Token("#", "#", 5, 2), Token("}", "}", 1, 3),  ]

sample4=[ Token("whole", "whole", 1, 2), Token("y", "Identifier", 2, 2), Token("=", "=", 3, 2),   Token("5", "Dec", 4, 2), Token("#", "#", 5, 2),   ]
sample5=[]

# inp=input("Enter a string: ")
# inp="sheesh(){dec dec a=5# dec b=2, c=5# whole a=6#}"
# inp="up(\"I love ninjas\")# }"
inp=" whole x= z,y,k#"
# inp="sheesh(){ up(\"I love ninjas\")#}"
# inp="whole whole a=1, b=2, g=3# dec d=5#"
# inp="}"
from source.LexicalAnalyzer.lexerpy import Lexer
tokens,error=Lexer.tokenize(inp)
print(tokens)
tokens= [x for x in tokens if x.type!="Whitespace" and x.type!="Block Comment" and x.type!="Inline Comment"]
print(tokens)
pars=parser.SyntaxAnalyzer(tokens)
print(pars.var_or_seq_dec())
# print(pars.sheesh_declaration())
print(pars.buffer)
print(pars.syntax_errors)


# pars=parser.SyntaxAnalyzer(q)
# print(pars.match("from"))
# print(pars.tokens)