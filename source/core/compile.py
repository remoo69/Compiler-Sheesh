import sys
sys.path.append('.')


from source.LexicalAnalyzer.Lexer import Lexer
from source.SyntaxAnalyzer.Parser import SyntaxAnalyzer
from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
# from source.CodeGeneration.CodeGen import CodeGenerator
from source.CodeGeneration.translator import Translator

# from source.core.AST import AST
# from source.core.symbol_table import Identifiers
class Compiler:
    def __init__(self, code, debugMode=False) -> None:


        self.lexer=Lexer(code)
        self.parser=None
        self.semantic=None
        self.translate=None

        self.codegen=None
        self.symbol_table=None
        
        self.output=[]

        self.lex_errors=[]
        self.syntax_errors=[]
        self.semantic_errors=[]
        self.runtime_errors=[]

        self.debug=debugMode

    @staticmethod
    def remove_whitespace_type(tokens):
        new_tokens = []
        for token in tokens:
            if token.type != "Whitespace" and token.type != "Block Comment" and token.type != "Inline Comment":
                new_tokens.append(token)
        return new_tokens

    def compile(self):
        print("Compiler Function...")
        self.lexer.tokenize()

        if not self.lexer.errors:
            self.parser=SyntaxAnalyzer(
                Compiler.remove_whitespace_type(self.lexer.tokens), self.debug)
            self.parser.parse()

            if not self.parser.syntax_errors:
                self.semantic=SemanticAnalyzer(self.parser.Tree, self.debug)
                self.semantic.analyze()
                if self.semantic.semantic_errors:
                    self.semantic_errors=self.semantic.semantic_errors
                    return
                else:
                    self.translate=Translator(self.parser.Tree, self.debug)
                    self.translate.generate()
                    if self.translate.errors:
                        self.runtime_errors=self.translate.errors
                        return
                    else:
                        self.output=self.translate.output
                        return
            else:
                self.syntax_errors=self.parser.syntax_errors
                return
            
        else:
            self.lex_errors=self.lexer.errors
            return

    def parse(self):
        print("Start Parsing...")
        self.lexer.tokenize()
        if not self.lexer.errors:
            self.parser=SyntaxAnalyzer(
                Compiler.remove_whitespace_type(self.lexer.tokens))
            self.parser.parse()
            if self.parser.syntax_errors:
                self.syntax_errors=self.parser.syntax_errors
        else:
            self.lex_errors=self.lexer.errors
    