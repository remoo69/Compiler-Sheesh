
import sys
from typing import Self
sys.path.append( '.' )
from dataclasses import dataclass

import source.core.constants as const
from source.core.error_handler import SemanticError
from source.core.error_types import Semantic_Errors as se
from source.core.AST import AST
from source.core.error_handler import RuntimeError as RError
from source.CodeGeneration.Functionality.runner import FuncRunner as FR

""" 
Scope System:
    The scopes of the variables in the program will follow a scope system where the scope of the variable would be the id of the
    loop or the block.

Types:

Values:

Block IDs:
    Blocks such as loops, conditionals, and functions will all have their own block IDs. Each block id will be used to reference the 
    scope of the variables inside the id. 

    Block IDs will follow the format below:
        [Block Type][Unique Identifier]

        where block type refers to one of the block types in:
            Function, For-loop, Kung, Ehkung, Whilst, Bet, 

        the unique identifier would be either the function identifier if the block is a function, and a number that
        iterates per invocation. For example, the main sheesh function would have the Block id of FUNCTION sheesh.
        
        
        Another case for this would be an invocation of a conditional block. The block id would be KUNG1, KUNG2, etc.
        The block id functions as a unique identifier for that specific block. As such, all block ids should be unique.

*UPDATE::
    A new symbol table will now be created every block. The newly created block will inherit the previous block as its parent. When the block is finished, 
    the parent block should be reset as the current block. 
    **Create a stack to store scope calls and hierarchies. 
 
"""



@dataclass
class Token:

    #Refers to the token's value. Could be a keyword, identifier, etc. This does not refer to the token's numerical value
    value: str

    #Refers to the type of token. Should be in the list of valid tokens such as Keyword, Identifier, Dec, Whole, Symbol, Operator, Text, Charr, Sus, Whitespace
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
        # return f"Token(\"{self.value}\", {self.attribute}, {self.dtype}, {self.numerical_value})"
        return f"Tok(\"{self.value}\")"

class Value:
    def __init__(self) -> None:
        self.value=None
        self.dtype=None
        self.scope=None
        self.token=None
        
    def execute(self):
        raise NotImplementedError
    
    def evaluate(self):
        raise NotImplementedError
    


class Variable:
    """  
    This functions as the base class for other constructs in the program like constants and sequences.
    This class is used to perform operations on the variable such as assigning and getting the value.
    Other functionalities should be implemented as needed.
    """
    def __init__(self, id, type) -> None:
        # self.set_scope(scope=scope)
        self.id=id
        self.type=type
        self.value=None
        
    def assign(self, op, value):
        """ Value should be evaluated already. """
        print(type(value))
        print(const.types[self.type])
        if type(value)==const.types[self.type]:
            pass
        else:
            if  type(value)!=const.py_types[self.type] :
                if type(value) in [str, float] and value.isdigit() and value%1==0:
                    value=type(value)(value) #FIXME - breaks when div
                else:
                    raise ValueError(se.VAL_OPERAND_INVALID)
            if isinstance(value, const.types[self.type]):
                pass
        if op=="=":
            self.value=value
        else:
            if self.value!=None:
                if op=="+=":
                    self.value+=value
                elif op=="-=":
                    self.value-=value
                elif op=="*=":
                    self.value*=value
                elif op=="/=":
                    self.value/=value #FIXME - Probably the same div issue
                elif op=="%=":
                    self.value%=value
            else:
                raise ValueError(se.VAR_UNDEF)
    
    def _evaluate(self):
        """  
        1. Return self.value
        """
        

    # def set_scope(self, scope):
    #     self.scope=scope
    
    def get_val(self):
        """  
        This method is from the variable class. Use accordingly.
        """
        if self.value!=None:
            return self.value
        else:
            raise ValueError("VAR_UNDEF")

    def __repr__(self):
        return f"Variable({self.id}, {self.type}, {self.value})"
    

class Sequence(Variable):
    """  
    Class used to represent sequences (arrays). Rows and cols should be whole values before instantiating the sequence. 
    Make sure to evaluate expressions inside before creating a sequence.
    """
    def __init__(self, id, type, rows, cols) -> None:
        super().__init__(id, type,)
        self.array=[]
        self.rows=rows
        self.cols=cols
    def set(self, rows, cols, value):
        self.array[rows][cols]=value

    def initialize(self, values):
        """ This assumes that values is also a list. Interface accordingly. """
        if len(values)!=self.rows:
            raise ValueError(se.WRONG_NUM_VALUES)
        
        for i in range(self.rows):
            if len(values[i])!=self.cols:
                raise ValueError(se.WRONG_NUM_VALUES)
            for j in range(len(self.cols)):
                self.array[i][j]=values[i][j]

    def get(self, row, col):
        """  
        1. Get row and col
        2. If isinstanc(row, any(id_derivates)) 
        3. id.evaluate
        
        """
        if row>=self.rows or col>=self.cols:
            raise ValueError(se.OUT_OF_BOUNDS)
        if col==None:
            return self.array[row]
        else:
            return self.values[row][col]
    
    def __repr__(self):
        return f"Sequence({self.id}, {self.type}, {self.values})"
    

#NOTE- medj sus
class ConstantVar(Variable):
    """ A global variable """
    def __init__(self, id, type) -> None:
        super().__init__(id, type)

class ConstantSeq(Sequence):
    """ A global sequence """
    def __init__(self, id, type) -> None:
        super().__init__(id, type)
        # self.set_scope=const.GBL  

class Function:
    def __init__(self, id:str, return_type:str, parameters:AST, body:AST) -> None:
        
        self.id=id
        self.return_type=return_type
        self.parameters:AST=parameters
        #parameters should be a list of variables
        self.func_body:AST=None
        self.ctx_name=f"FUNCTION {self.id}"


    def execute(self, args:list)->bool:
        """  
        *Args are a list of values. Evaluate args first before executing.
        
        This method should execute the statements in the function. Idk how to do that yet tho.
        
        Algorithm:
        1. Get block node
        2. Set args (series of var inits)
        Init new block
        Append var initialization

        3. Execute code until end.

        """
        if len(args)!=len(self.parameters):
            raise ValueError("WRONG_NUM_ARGS")
        else:
            FR(func=self,arguments= args).run()
        
        # while True:
        #     if self.current_node.root not in self.routines.keys():
        #         self.previous_node=self.current_node
        #         self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        #     else:
        #         self.routines[self.current_node.root]()
        #         self.previous_node=self.current_node
        #         try:
        #             self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        #         except AttributeError:
        #             break
        #     if self.current_node is None:
        #         break  # Exit the loop if the tree has been fully traversed
        return self.func_body #FIXME - di pa ayos to
    
class Parameter(Variable):
    def __init__(self, id, type, param_type, scope) -> None:
        super().__init__(id, type, scope)
        #regular var or sequence
        self.param_type=param_type
    
    def __repr__(self):
        return f"Parameter({super().__repr__()})"

class ScopeTree:
    def __init__(self, root, children) -> None:
        self.root=root
        self.children:list=children
    def __repr__(self) -> str:
        return "Scope()" #FIXME - ayusin mo to

class SymbolTable:

    """ 
    This Symbol Table is only for Identifiers. 
    It is a simple dictionary that stores the identifiers as keys and their corresponding Token objects as values. 
    """

    def __init__(self):
        self.symbols = {}
        # self.scopetree=ScopeTree(const.GBL)
        # self.runtime_errors=[]

    def keys(self):
        return self.symbols.keys()

    def variable(self, id, type)->Variable:
        if id not in self.symbols.keys():
            self.symbols[id]=Variable(id=id,type=type)

            return self.symbols[id]
        else:
            
            raise KeyError("VAR_REDECL_INSCOPE")


#FIXME - IDK WHAT TO DO WITH THIS
    def sequence(self, id, type, scope, rows, cols):
        if id not in self.symbols.keys():
            self.symbols[id]=Sequence(id=id, type=type, scope=scope, rows=rows, cols=cols)
        else:
            raise KeyError("VAR_REDECL_INSCOPE")
        

    def function(self,*,id, return_type, parameters, body=None):
        if id not in self.symbols.keys():
            if body:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters).body(body)
            else:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters)
        else:
            raise KeyError("FUNC_REDECL_INSCOPE")
        

    def constant_var(self, id, type):
        if id not in self.symbols.keys():
            self.symbols[id]=ConstantVar(id=id, type=type)
        else:
            raise KeyError("CONST_REDECL")
        

    def constant_seq(self, id, type):
        if id not in self.symbols.keys():
            self.symbols[id]=ConstantSeq(id=id, type=type)
        else:
            raise KeyError("CONST_REDECL")
            # self.symbols[id]=Parameter(id=id, type=type, param_type=param_type, scope=scope)


    def find(self,id):
        if id in self.symbols.keys():
            return self.symbols[id]
        else:
            
            raise KeyError("VAR_UNDECL")
            # self.runtime_errors.append()
        

    def find_var(self, id, scope)->Variable:
        if id in self.symbols.keys() and type(self.symbols[id])==Variable and self.symbols[id].scope==scope:
            return self.symbols[id]
        else:
            raise AttributeError("VAR_UNDECL")
        
    def find_seq(self, id, scope)->Sequence:
        if id in self.symbols.keys() and type(self.symbols[id])==Sequence  and self.symbols[id].scope==scope:
            return self.symbols[id]
        else:
            raise AttributeError("SEQ_UNDECL")
        
    def find_const_var(self, id)->ConstantVar:
        if id in self.symbols.keys() and type(self.symbols[id])==ConstantVar:
            return self.symbols[id]
        else:
            raise AttributeError("CONST_UNDECL")
        

    def find_const_seq(self, id)->ConstantSeq:
        if id in self.symbols.keys() and type(self.symbols[id])==ConstantSeq:
            return self.symbols[id]
        else:
            raise AttributeError("CONST_UNDECL")
        

    def find_func(self, id)->Function:
        if id in self.symbols.keys() and type(self.symbols[id])==Function:
            return self.symbols[id]
        else:
            raise AttributeError("FUNC_UNDECL")
        

    # def find_param(self, id, scope)->Parameter:
    #     if id in self.symbols.keys() and type(self.symbols[id])==Parameter and self.symbols[id].scope==scope:
    #         return self.symbols[id]
    #     else:
    #         raise AttributeError("PARAM_UNDECL_INSCOPE")


        
    def get_all(self, type):
        return [sym for sym in self.symbols.values() if isinstance(sym, type)]
    
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


class Context:
    def __init__(self, name, parent) -> None:
        self.name=name
        self.symbol_table:SymbolTable=None
        self.parent=parent
        
    
    def symbols(self):
        self.symbol_table=SymbolTable()
        self.symbol_table.extend(self.parent.symbol_table)
        return self.symbol_table
    
    
