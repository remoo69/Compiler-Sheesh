
import sys
sys.path.append( '.' )
from dataclasses import dataclass

@dataclass
class Token:

    #Refers to the token's value. Could be a keyword, identifier, etc. This does not refer to the token's numerical value
    value: str

    #Refers to the type of token. Should be in the list of 
    #valid tokens such as Keyword, Identifier, Dec, Whole, Symbol, Operator, Text, Charr, Sus, Whitespace
    type: str 


    #Refers to the attribute of the token. Could be func, var, seq, etc
    attribute: str= None

    #Refers to the scope of the token. Could be Global or Local
    scope: str=None
    
    #Refers to the data type of the token. Could be int, float, string, etc.
    dtype:str=None


    line: int=0
    position: int= 0

    numerical_value:float=None


    idnum=1
    tok_num=1
    line_num=1
    in_comment=False
    block_comment_buffer=''
    block_start_line=0

    def __repr__(self) -> str:
        return f"Token(\"{self.value}\", {self.attribute}, {self.dtype}, {self.numerical_value})"

class SymbolTable:

    """ 
    This Symbol Table is only for Identifiers. 
    It is a simple dictionary that stores the identifiers as keys and their corresponding Token objects as values. 
      
    """
    def __init__(self):
        self.symbols = {}

    def keys(self):
        return self.symbols.keys()
    

    def add(self, value:Token):
        key=value.value
        self.symbols[key] = value

    def __setitem__(self, value:Token):
        key=value.value
        self.symbols[key] = value

    def __getitem__(self, key):
        return self.symbols[key]

    def __contains__(self, key):
        return key in self.symbols

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

    def __str__(self):
        return f"{self.symbols}"
    

class Identifiers:
    def __init__(self) -> None:
        self.vars=SymbolTable()
        self.funcs=SymbolTable()
        self.params=SymbolTable()

    def __repr__(self):
        return f"Identifiers({self.vars}, {self.funcs}, {self.params})"
    