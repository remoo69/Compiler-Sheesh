import grammar 
import source.core.constants as const
from source.LexicalAnalyzer.tokenclass import Token
from grammar import FirstFollowPredict

cfg=grammar.Grammar()
first = FirstFollowPredict().firstSet(grammar.Grammar.cfg, grammar.Grammar.cfg.keys())


class SyntaxAnalyzer:
    
    def __init__(self):
        self.parse_stack = []
        self.token_pointer = 0
        self.production_pointer = 0
        self.rule_pointer = 0
        self.production="program"
        self.current_production=cfg.cfg[self.production][self.production_pointer]
        self.is_error=False
        self.tokens=[]
        self.error_message=""
        self.error_line=0
        self.error_column=0
        self.error_token=""
        self.error_type=""
        self.error_expected=""
        self.error_found=""
        self.error_rule=""
        self.error_production=""
        self.error_stack=""
        self.error_stack_trace="" 

    def parse(self, tokenlist: list[Token]):
        tokens = [i for i in tokenlist if i.type != "Whitespace" and i.type != "Block Comment" and i.type != "Inline Comment"]
        

        # initialize token pointer
        token_pointer = 0
        production_pointer = 0
        rule_pointer = 0
        production="program"
        current_production=cfg.cfg[production][production_pointer]
        # from list of token objects, parse using ll1
        parse_stack = []
        # initialize parse stack
        parse_stack.append("$")
        is_error=False
        # Push the start symbol onto the parse stack
        parse_stack.append("program")

        # Push the first production of the start symbol onto the parse stack
        parse_stack.extend(reversed(cfg.cfg["program"][0]))

        # Iterate until the parse stack is empty or an error occurs
        while parse_stack:
            # Get the top of the parse stack
            top = parse_stack[-1]

            # Get the current token
            current_token = tokens[token_pointer]

        #     # If the top of the parse stack is a non-terminal
        #     if top in cfg.non_terminals:
        #     # Get the production rule for the current non-terminal and current token
        #     production_rule = cfg.get_production_rule(top, current_token.type)

        #     # If there is no production rule, raise an error
        #     if not production_rule:
        #         is_error = True
        #         error_message = f"Syntax error: Unexpected token '{current_token.value}' at line {current_token.line}, column {current_token.column}"
        #         break

        #     # Pop the top of the parse stack
        #     parse_stack.pop()

        #     # Push the production rule onto the parse stack in reverse order
        #     parse_stack.extend(reversed(production_rule))

        #     # If the top of the parse stack is a terminal
        #     elif top in cfg.terminals:
        #     # If the top of the parse stack matches the current token
        #     if top == current_token.type:
        #         # Pop the top of the parse stack and move to the next token
        #         parse_stack.pop()
        #         token_pointer += 1
        #     else:
        #         # Raise an error
        #         is_error = True
        #         error_message = f"Syntax error: Expected token '{top}' but found '{current_token.value}' at line {current_token.line}, column {current_token.column}"
        #         break

        # # If the parse stack is empty and there are no more tokens, the parsing is successful
        # if not parse_stack and token_pointer == len(tokens):
        #     print("Parsing successful")
        # else:
        #     print("Parsing failed")
class TreeNode:
    pass

class ParseTree:
    pass

