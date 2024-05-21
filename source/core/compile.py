import sys
sys.path.append('.')


from source.LexicalAnalyzer.Lexer import Lexer
from source.SyntaxAnalyzer.Parser import SyntaxAnalyzer
from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.CodeGeneration.cg2 import CodeGenerator

# from source.core.AST import AST
# from source.core.symbol_table import Identifiers
class Compiler:
    def __init__(self, code, debugMode=False) -> None:


        self.lexer=Lexer(code)
        self.parser=None
        self.semantic=None

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
        print("Tokenization Finished...")

        if self.lexer.errors ==[]:
            self.parser=SyntaxAnalyzer(
                Compiler.remove_whitespace_type(self.lexer.tokens), self.debug)
            self.parser.parse()
            print("Syntax Analysis Finished...")

            if self.parser.syntax_errors ==[]:

                self.codegen=CodeGenerator(parse_tree=self.parser.Tree, debugMode=self.debug, mode=1)
                self.codegen.generate_code()
                print("Code Generation Finished...")
                if self.codegen.runtime_errors:
                    self.runtime_errors=self.codegen.runtime_errors
                    return
                
                else:
                    self.output=self.codegen.output_stream
                    return
                
            else:
                self.syntax_errors=self.parser.syntax_errors
                return
            
        else:
            self.lex_errors=self.lexer.errors
            return

    def parse(self):
        print("Start Parsing...")
        if self.lex_analyze():
            self.parser=SyntaxAnalyzer(
                Compiler.remove_whitespace_type(self.lexer.tokens))
            self.parser.parse()
            if self.parser.syntax_errors:
                self.syntax_errors=self.parser.syntax_errors
                return False
            else:
                return True
    
    def lex_analyze(self):
        print("Start Lexical Analysis...")
        self.lexer.tokenize()
        if not self.lexer.errors:
            return True
        else:
            self.lex_errors=self.lexer.errors
            return False