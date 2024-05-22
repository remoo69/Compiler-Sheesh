
import sys
sys.path.append( '.' )
from dataclasses import dataclass

import source.core.constants as const
from source.core.error_handler import SemanticError
from source.core.error_types import Semantic_Errors as se
# from source.core.AST import AST
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
        Another case for this would be the first invocation of a conditional like the kung statement. 
        The block if for it would be KUNG 1.
 
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
        return f"Token(\"{self.value}\", {self.type}, {self.dtype}, {self.numerical_value})"

class Variable:
    def __init__(self, id, type) -> None:
        self.id=id
        self.type=type
        self.value=None
        
    def assign(self, op, value):
        print(type(value))
        print(const.types[self.type])
        if type(value)==const.types[self.type]:
            pass
        else:
            if  type(value)!=const.py_types[self.type] :
                if type(value) in [str, float] and value.isdigit() and value%1==0:
                    value=type(value)(value)
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
                    self.value/=value
                elif op=="%=":
                    self.value%=value
            else:
                raise ValueError(se.VAR_UNDEF)


    # def set_scope(self, scope):
    #     self.scope=scope
    
    def get_val(self):
        if self.value!=None:
            return self.value
        else:
            raise ValueError("VAR_UNDEF")

    def __repr__(self):
        return f"Variable({self.id}, {self.type}, {self.value})"
    

class Sequence(Variable):
    def __init__(self, id, type, rows, cols) -> None:
        super().__init__(id, type, )
        # self.array=[[None]*cols for _ in range(int(rows))]
        self.array=[]
        self.rows=rows
        self.cols=cols

    def set(self, rows, cols, value):
        if rows>self.rows or cols>self.cols:
            raise ValueError("OUT_OF_BOUNDS")
        else:
            
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
        if row>=self.rows or col>=self.cols:
            raise ValueError(se.OUT_OF_BOUNDS)
        if col==None:
            return self.array[row]
        else:
            return self.values[row][col]
    
    def __repr__(self):
        return f"Sequence({self.id}, {self.type}, {self.array})"
    

#NOTE- medj sus
class Constant(Variable):
    def __init__(self, id, type) -> None:
        super().__init__(id, type)
        # self.set_scope=const.GBL

class Constant(Sequence):
    def __init__(self, id, type) -> None:
        super().__init__(id, type)
        # self.set_scope=const.GBL

class Function:
    def __init__(self, id, return_type, parameters) -> None:
        self.id=id
        self.return_type=return_type
        self.parameters:list[Parameter]=parameters
        self.func_body=None

    def __repr__(self) -> str:
        return f"Function({self.id}, {self.return_type}, {self.parameters}, {self.func_body})"

    # def new_statement(self, statement):
    #     self.statements.append(statement)

    def body(self, statements):
        self.func_body=statements

    def execute(self):
        """  
        This method should execute the statements in the function. Idk how to do that yet tho.
        
        Algorithm:
        1. Get block node
        2. Set args (series of var inits)
        3. Execute code until end.

        """
        print("Generating code...")
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
    def __init__(self, id, type, param_type,) -> None:
        super().__init__(id, type)
        #regular var or sequence
        self.param_type=param_type
    
    def __repr__(self):
        return f"Parameter({super().__repr__()})"

# class ScopeTree:
#     def __init__(self, root, children) -> None:
#         self.root=root
#         self.children:list=children
#     def __repr__(self) -> str:
#         return "Scope()" #FIXME - ayusin mo to

class SymbolTable:

    """ 
    This Symbol Table is only for Identifiers. 
    It is a simple dictionary that stores the identifiers as keys and their corresponding Token objects as values. 
      
    """
    def __init__(self):
        self.symbols = {}
        # self.scope_tree=ScopeTree()

    def keys(self):
        return self.symbols.keys()

    def variable(self, id, type):
        if id not in self.symbols.keys():
            self.symbols[id]=Variable(id=id,type=type)
        else:
            raise KeyError("VAR_REDECL_INSCOPE")


#FIXME - IDK WHAT TO DO WITH THIS
    def sequence(self, id, type, rows, cols):
        if id not in self.symbols.keys():
            self.symbols[id]=Sequence(id=id, type=type, rows=rows, cols=cols)
        else:
            raise KeyError("SEQ_REDECL_INSCOPE")
        

    def function(self,*,id, return_type, parameters, body=None):
        if id not in self.symbols.keys():
            if body:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters)
                self.symbols[id].body(body)
                print(self.symbols)
            else:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters)
        else:
            raise KeyError("FUNC_REDECL_INSCOPE")
        

    def constant(self, id, type):
        if id not in self.symbols.keys():
            self.symbols[id]=Constant(id=id, type=type)
        else:
            raise KeyError("CONST_REDECL")
        

    def parameter(self, id, type, param_type, ):
        if id in self.symbols.keys() and isinstance(self.symbols[id], Parameter):
            raise KeyError("PARAM_REDECL_INSCOPE")
        else:
            self.symbols[id]=Parameter(id=id, type=type, param_type=param_type)


    def find(self,id):
        if id in self.symbols.keys():
            return self.symbols[id]
        else:
            raise KeyError("VAR_UNDECL")
        

    def find_var(self, id)->Variable:
        if id in self.symbols.keys() and type(self.symbols[id])==Variable :
            return self.symbols[id]
        else:
            raise AttributeError("VAR_UNDECL")
        
    def find_seq(self, id)->Sequence:
        if id in self.symbols.keys() and type(self.symbols[id])==Sequence :
            return self.symbols[id]
        else:
            raise AttributeError("SEQ_UNDECL")
        
    def find_const(self, id)->Constant:
        if id in self.symbols.keys() and type(self.symbols[id])==Constant:
            return self.symbols[id]
        else:
            raise AttributeError("CONST_UNDECL")
        
    def find_func(self, id)->Function:
        if id in self.symbols.keys() and type(self.symbols[id])==Function:
            return self.symbols[id]
        else:
            raise AttributeError("FUNC_UNDECL")
        
    def find_param(self, id)->Parameter:
        if id in self.symbols.keys() and type(self.symbols[id])==Parameter :
            return self.symbols[id]
        else:
            raise AttributeError("PARAM_UNDECL_INSCOPE")

#FIXME - UNIMPLEMENTED
    # def  get_var_inscope(self, scope)->dict:
    #     vars={}
    #     raise NotImplementedError
    #     for key in self.symbols.keys():
    #         if self.symbols[key].scope==scope:
    #             vars.update(self.symbols[key])
    #         elif self.symbols[3]:pass
            

        
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
    





    

# class Identifiers:
#     def __init__(self) -> None:
#         self.vars=SymbolTable()
#         self.funcs=SymbolTable()
#         self.params=SymbolTable()

#     def __repr__(self):
#         return f"Identifiers({self.vars}, {self.funcs}, {self.params})"


#     def accessible_ids(self):
#         temp=SymbolTable()
#         temp.symbols.update(self.vars.symbols) 
#         temp.symbols.update(self.funcs.symbols) 

#         return temp