import re
import sys

sys.path.append('.')
# from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_handler import RuntimeError as RError
from source.core.error_handler import SemanticError as SError
from source.core.error_types import Semantic_Errors as se
import source.core.constants as const
# from source.core.symbol_table import  Context

# from source.CodeGeneration.Functionality.ControlFlow import ControlFlow
# from source.CodeGeneration.Functionality.Loops import Loops
# from source.CodeGeneration.Functionality.Declarations import Identifier
# from source.CodeGeneration.Functionality.Evaluators import Evaluators
# from source.CodeGeneration.Functionality.InOut import InOut
from source.core.AST import AST
from copy import deepcopy



"""  
TODO
1. Literal Limits
2. Choose-when-default
3. Func def,call, as expr, prototype #NOTE - partially done
4. Sequence def, init, call, as expr #NOTE  - started
5. Multiple init
6. Seq bounds checking
7. Seq size enforcement

8. Break when runtime or semantic error

"""

import sys
from typing import Self
sys.path.append( '.' )
from dataclasses import dataclass

import source.core.constants as const
from source.core.error_handler import SemanticError
from source.core.error_types import Semantic_Errors as se
from source.core.AST import AST
from source.core.error_handler import RuntimeError as RError
# from source.CodeGeneration.cg2 import CodeGenerator
# from source.CodeGeneration.Functionality.Evaluators import Evaluators
# from source.CodeGeneration.Functionality.runner import FuncRunner as FR

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
    

class Sequence:
    """  
    Class used to represent sequences (arrays). Rows and cols should be whole values before instantiating the sequence. 
    Make sure to evaluate expressions inside before creating a sequence.
    """
    def __init__(self, id, type, rows, cols) -> None:
        self.id=id
        self.type=type
        self.array=[]
        self.rows=rows
        self.cols=cols
        
    def __repr__(self) -> str:
        return f"Sequence({self.id}, {self.rows}, {self.cols})"
    def set(self, rows, cols, value):
        self.array[rows][cols]=value

    def initialize(self, values):
        """ This assumes that values is also a list. Interface accordingly. """
        if len(values)!=self.rows:
            raise ValueError("WRONG_NUM_VALUES")
        
        for i in range(self.rows):
            if self.cols==0:
                self.array.append(values[i])
            else:
                if len(values)!=self.cols:
                    raise ValueError("WRONG_NUM_VALUES")    
                for j in range(len(self.cols)):
                    self.array[i][j]=values[i][j]

    def get(self, row, col=0):
        """  
        1. Get row and col
        2. If isinstanc(row, any(id_derivates)) 
        3. id.evaluate
        
        """
        
        if row>=self.rows or col>self.cols:
            raise ValueError(se.OUT_OF_BOUNDS)
        if col==0:
            return self.array[row]
        else:
            return self.values[row][col]
    
    def __repr__(self):
        return f"Sequence({self.id}, {self.type}, {self.values})"
    

#NOTE- medj sus
class ConstantVar(Variable):
    """ A global variable """
    def __init__(self, id, type, value) -> None:
        super().__init__(id, type)
        super().assign(op="=", value=value)
        
    def assign(self, op, value):
        raise ValueError("CONST_REASSIGN")
    
    def initialize(self, values):
        raise ValueError("CONST_REASSIGN")

class ConstantSeq(Sequence):
    """ A global sequence """
    def __init__(self, id, type, rows, cols) -> None:
        super().__init__(id, type, rows, cols)
        
    def assign(self, op, value):
        raise ValueError("CONST_REASSIGN")
    
    def initialize(self, values):
        raise ValueError("CONST_REASSIGN")
        
        # self.set_scope=const.GBL  

class Parameter(Variable):
    def __init__(self, id, type, param_type, scope) -> None:
        super().__init__(id, type, scope)
        #regular var or sequence
        self.param_type=param_type
    
    def __repr__(self):
        return f"Parameter({super().__repr__()})"

class Function:
    def __init__(self, id:str, return_type:str, parameters:list[Parameter], body:AST) -> None:
        
        self.id=id
        self.return_type=return_type
        self.parameters=parameters
        #parameters should be a list of variables
        self.func_body:AST=body
        # self.ctx_name=f"FUNCTION {self.id}"


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
            # FR(func=self,arguments= args).run()
            cd=CodeGenerator(parse_tree=self.func_body,)
            
            for  i in len(args):
                cd.context.symbol_table.find(args[i].value).assign(op="=", value=Evaluators(expression=args[i],
                                                                    context=cd.context,
                                                                    runtime_errors=cd.runtime_errors))
                cd.generate_code() #NOTE -  added
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
    def sequence(self, id, type,rows, cols)->Sequence:
        if id not in self.symbols.keys():
            self.symbols[id]=Sequence(id=id, type=type, rows=rows, cols=cols)
            return self.symbols[id]
        else:
            raise KeyError("VAR_REDECL_INSCOPE")
        

    def function(self,*,id, return_type, parameters, body=None):
        if id not in self.symbols.keys():
            if body:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters, body=body)
                return self.symbols[id]
            else:
                self.symbols[id]=Function(id=id, return_type=return_type, parameters=parameters)
        else:
            raise KeyError("FUNC_REDECL_INSCOPE")
        

    def constant_var(self, id, type, value)->ConstantVar:
        if id not in self.symbols.keys():
            self.symbols[id]=ConstantVar(id=id, type=type, value=value)
            return self.symbols[id]
        else:
            raise KeyError("CONST_REDECL")
        

    def constant_seq(self, id, type, rows, cols):
        if id not in self.symbols.keys():
            self.symbols[id]=ConstantSeq(id=id, type=type, rows=rows, cols=cols)
            return self.symbols[id]
        else:
            raise KeyError("CONST_REDECL")
            # self.symbols[id]=Parameter(id=id, type=type, param_type=param_type, scope=scope)


    def find(self,id):
        if id in self.symbols.keys():
            return self.symbols[id]
        else:
            
            raise KeyError("VAR_UNDECL")
            # self.runtime_errors.append()
        

    def find_var(self, id)->Variable:
        if id in self.symbols.keys() and type(self.symbols[id])==Variable:
            return self.symbols[id]
        else:
            raise AttributeError("VAR_UNDECL")
        
    def find_seq(self, id, scope)->Sequence:
        if id in self.symbols.keys() and type(self.symbols[id])==Sequence :
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
        self.parent=parent
        self.symbol_table:SymbolTable=SymbolTable()
        self.runtime_errors=[]
        self.output_stream={}
        if parent != None:
            self.symbol_table.symbols.update(self.parent.symbol_table)
            # self.runtime_errors.extend(self.parent.runtime_errors)
            
            # self.output_stream.update(self.parent.output_stream)
  
    def __repr__(self) -> str:
        return f"Context({self.name})"
    
    def symbols(self):
        self.symbol_table=SymbolTable()
        self.symbol_table.extend(self.parent.symbol_table)
        return self.symbol_table

class Evaluators:
    """  
    This is a general helper class for evaluations. An evaluator can take either a value, variable, function call, or an expression.
    The evaluator will then evaluate the expression and return the result.
    The evaluator should be given an expression, and the symbol table. It then outputs the result of the expression.
    The expression should be a list of tokens.
    
    """
    def __init__(self, expression, runtime_errors, context) -> None:
        self.expression=expression
        # self.runtime_errors=runtime_errors
        self.context=context
        # self.context.name=scope
        # self.context.symbol_table:st.SymbolTable=symbol_table

    def build_expression(self, expression):
        """  
        This method extracts all possible values from the expression. It then returns a list of the values.
        This method should evaluate funcs, sequences, and variables first before evaluating the expression.
        """
        final_expression=""
        eq_found=False
        for i, expr in enumerate(expression):
 
                if expr.type not in const.keywords:
                    if expr.type=="Identifier":
                        try:
                            var= self.context.symbol_table.find(expr.value)
                            if isinstance(var, Sequence): 
                                
                                index=self.evaluate(expression[i+2:], type=const.dtypes.whole)
                                col=self.evaluate(expression[i+3:], type=const.dtypes.whole) # FIXME can' eval col because can't find second index.
                                # sequence=self.context.symbol_table.find(var.value, self.context.name)
                                final_expression+=var.get(row=index, col=col)
                                
                            elif isinstance(var, Variable):
                                if var.type in ["whole", "dec",]:
                                    final_expression+=str(var.value)
                                elif var.type in ["sus", "text", "charr"]:
                                    final_expression+=var.value 
                                    #NOTE - idk what to do here. ito muna lagay ko
                            elif isinstance(var, Function):
                                args=[]
                                
                                for j,expr in enumerate(expression[i:]):
                                    args[j]=""
                                    if expr.type==",":
                                        break
                                    else:
                                        if expr.type=="Identifier":
                                            var_arg=self.context.symbol_table.find(expr.value)
                                            if isinstance(var_arg, Sequence):
                                                index=self.evaluate(expression[i+2:], type=const.dtypes.whole)
                                                col=self.evaluate(expression[i+3:], type=const.dtypes.whole) # FIXME can' eval col because can't find second index.
                                                # sequence=self.context.symbol_table.find(var.value, self.context.name)
                                                final_expression+=var.get(row=index, col=col)
                                                
                                            if isinstance(var_arg, Function):
                                                var_arg.execute(self.build_expression(expression=expression[i:]))

                                        args[j]+=expr.value
                                func=var.execute(args)
                                final_expression+=func 
                            elif isinstance(var, Token):
                                if var.type in ["Whole", "Dec"]:
                                    final_expression+=var.numerical_value
                                else:
                                    self.context.runtime_errors.append(RError(se.EWAN, expr, "Invalid Expression"))
                        except KeyError as e:
                            e=str(e)[1:-1]
                            self.context.runtime_errors.append(RError(error=getattr(se, e), token=expr, expected=se.expected[e]))

                    elif expr.type in ["Whole", "Dec", ]:
                        final_expression+=expr.value
                    elif expr.type in ["Text", "Charr"]:
                        final_expression+=expr.value
                    elif expr.type in ["Sus"]:
                        if expr.value =="nocap":
                            final_expression+="True"
                        else:
                            final_expression+="False"
                    elif expr.type in const.aop:
                        final_expression+=expr.value
                    elif expr.type in ["#", "]"]:
                        break
                    else:
                        final_expression+=expr.value
                else:
                    pass
                
        return final_expression
    
    def evaluate(self, expr, type):
        expression=self.build_expression(expression=expr)
        return const.py_types[type]( self.general_evaluator(expression))
        
    # def evaluate(self, expr):
    #     new_expr=self.build_expression()
    #     if not any(op in new_expr for op in const.all_op):
    #         return new_expr
    #     else:
    #         return eval(new_expr)


    
    def general_evaluator(self, expr:str):
        """ TRIES to evaluate expressions using python's eval() """
        if expr!=None and expr!="":
            if not any(op in expr for op in const.all_op):
                return expr
            else:
                return eval(expr)
        else:
            return None
    
    def assign(self, id):
        """  
        This function should take the name of the id, and the symbol table. It should then assign the value to the id.

        """
        assign_ops=["=", "+=", "-=", "*=", "/=", "%="]
        op=None
        for index, vals in enumerate(self.expression):
            if vals.type in assign_ops:
                op=self.expression[index].type
                break
        
        value=None
        if id.value in self.context.symbol_table.keys():
            items=self.expression
            try:
                var=self.context.symbol_table.find(id.value, self.context.name)
                #FIXME - no type checking for var

                if var.type in ["dec", "whole"]:
                    temp=self.build_expression(self.expression)
                else:
                    temp=self.build_condition()
                
            
                value=self.general_evaluator(temp)

                id_ref=self.context.symbol_table.find_var(id.value, self.context.name)
                if id_ref.value==None:
                    id_ref.value=0 #NOTE -  medj sus; idk if oks lang bang ganto default
                if op != "=":
                    if op=="+=":
                        value+=id_ref.value
                    elif op=="-=":
                        value-=id_ref.value
                    elif op=="*=":
                        value*=id_ref.value
                    elif op=="/=":
                        value/=id_ref.value
                    elif op=="%=":
                        value%=id_ref.value
        
                
                if value != None:
                    print(type(value))
                    print(const.types[id_ref.type])
                    if type(value)==const.py_types[id_ref.type]:
                        if id_ref.type in ["whole", "dec"]:
                            self.context.symbol_table[id.value].assign(op=op, value=const.py_types[id_ref.type](value)[1:-1])
                        else:
                            self.context.symbol_table[id.value].assign(op=op, value=value)
                        return True
                    
                    elif type(value)==str:
                        value=const.py_types[id_ref.type](value)
                        self.context.symbol_table[id.value].assign(op=op, value=value)
                        return True
                    else:
                        if value%1==0 or value>0 or value<0:
                            value=self.semantic.data_types[id.dtype](value)
                            self.context.symbol_table[id.value].assign(op=op, value=value)
                            return True
                        else:
                            # self.semantic.semantic_error(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}")
                            self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}"))
                else:
                    # self.semantic.semantic_error(se.VAR_UNDEF, id, "Value pare")
                    self.runtime_errors.append(RuntimeError(error=se.VAR_UNDEF,token= id, expected="Value pare"))
            except KeyError as e:
                        e=str(e)[1:-1]
                        self.codegen.context.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
    
         
class CodeGenerator:
    """  
    *UPDATE: CODE GEN NOW INCLUDES SEMNATIC ANALYZER

    General Code Generator Logic: Traverse all nodes in the AST. Go to respective routines based on the node's root.
    Algorithm:
    * The Code Generator Functions like a Depth First Search Traversal.
    * The code gen executes routines based on the current node's leaf or root, depending on the implementation for that type.
    1. Traverse the tree
    2. If a root with a routine is found, execute routine.
    3. If success, go to the next node.
    4. If fail, raise runtime error.


    Update:
        A routine exists for each node where the node's first set is a terminal. This is to ensure that all possible outcomes in the code generator has an output.
        In some cases, however, multiple nodes are agreggated into one if their functions are similar. This is to reduce redundancy in the code generator.
    
    Functionalities will be direct calls to their respective modules. This is to ensure that the code generator is modular and can be easily updated.
    
    Code Generator Tasks:
    1. Each node in the ast is traversed during code generation + semantic analysis. 
    2. Variables are created and directly added to the symbol table.
    3. Functions such as up, pa_mine, and user defined function invocations function similarly. Arguments are assigned to parameters as variables in the function block.
        the body of the function is then executed using gen_code()<-might need some optimization/fixing
    4. Each method in this class represents a node in the ast and extracts necessary information for the execution of the node. 
    5. 
    
    """
    def __init__(self, parse_tree:AST, parent:Context=None, debugMode=False, mode=2) -> None:
        self.mode=mode
        
        self.debug=debugMode

        self.parse_tree=parse_tree
        self.current_node:AST = parse_tree
        self.previous_node:AST=None #Stores the previous node to handle loops?
        
        self.output_stream={}

        self.matched=self.parse_tree.leaves()
        
        self.req_type=None
        
        self.nearest_id=None

        self.semantic_errors:list[SError]=[]
        self.runtime_errors:list[RError] = []

        # self.scope_tree=self.symbol_table.scopetree
        self.ctx_dict={}
        if parent==None:
            self.context=Context("GLOBAL", None)
            self.ctx_dict[self.context.name]=self.context
            # self.ctx_dict[self.context.name]=deepcopy(self.context)
        else:
            self.context:Context=parent
        

        
        

        self.reverse_types={v:k for k, v in const.types.items()}

        self.block_counter=1
        self.print_ctr=1
        self.temp_id=None
        """  
        Routines act as the entry point for the functions in the program. As such, each routine should contain their respective
        functionalities. 
        """
        self.routines={

            # "sheesh_declaration": self.sheesh_declaration,
            "allowed_in_loop": self.allowed_in_loop,
            # "id_tail": self.id_tail, #handled in backend
            # "id_next_tail": self.id_next_tail,
            "reg_body": self.reg_body,
            "var_or_seq_dec": self.var_or_seq_dec,
            # "val_assign": self.val_assign, #handled in backend; var or seq dec
            # "all_value": self.all_value,
            # "seq_tail": self.seq_tail,
            # "seq_init": self.seq_init,
            # "var_seq_tail": self.var_seq_tail,
            # "txt_op": self.txt_op,
            "const_type": self.const_type,
            "in_loop_body":self.in_loop_body,
            # "loop_body":self.loop_body,
            # "const_dimtail1": self.const_dimtail1,
            # "const_dimtail2": self.const_dimtail2,
            # "const_var_tail": self.const_var_tail,
            # "const_tail": self.const_tail,
            # "control_flow_statement": self.control_flow_statement,
            # "ehkung_statement": self.ehkung_statement,
            # "cond_tail": self.cond_tail,
            # "when_statement": self.when_statement,
            # "statement_for_choose": self.statement_for_choose,
            # "choose_default": self.choose_default,
            "looping_statement": self.looping_statement,
            "func_def": self.func_def,
            "loop_body_statement": self.loop_body_statement,
            "control_flow_statement":self.control_flow_statement,
            # "yeet_statement": self.yeet_statement, 
            # "step_statement": self.step_statement,
            # "loop_body_statement": self.loop_body_statement,
            # "loop_ehkung": self.loop_ehkung,
            # "in_loop_condtail": self.in_loop_condtail,
            # "loop_when": self.loop_when,
            # "loop_default": self.loop_default,
            # "yeet_statement": self.yeet_statement,
            # "func_def": self.func_def,
            # "id_as_val": self.id_as_val,
            # "id_val_tail": self.id_val_tail,
            # "assign_value": self.assign_value,
            # "literal_or_expr": self.literal_or_expr,
            # "l_expr_withparen": self.l_expr_withparen,
            # "charr_op_tail": self.charr_op_tail,
            # "condition": self.condition,
            # "id_val_op": self.id_val_op,
            # "id_val_paren": self.id_val_paren,
            # "logic_value": self.logic_value,
            # "l_val_withparen": self.l_val_withparen,
            # "logic_not_expr": self.logic_not_expr,
            # "logic_expr": self.logic_expr,
            # "logic_id": self.logic_id,
            # "logic_id_tail": self.logic_id_tail,
            # "num_arithm": self.num_arithm,
            # "num_arithmparen": self.num_arithmparen,
            # "id_arithm": self.id_arithm,
            # "id_arithm_paren": self.id_arithm_paren,
            # "id_arithm_tail": self.id_arithm_tail,
            # "num_or_arithmexpr": self.num_or_arithmexpr,
            # "num_or_arithmparen": self.num_or_arithmparen,
            # "num_math_op": self.num_math_op,
            # "rel_expr": self.rel_expr,
            # "rel_val": self.rel_val


    
        }


    def new_context(self, context):
        prev_output=self.context.output_stream
        # prev_errors=self.context.runtime_errors
        self.context=Context(context, self.context)
        self.context.output_stream=prev_output
        # self.context.runtime_errors=prev_errors
        # cpy=deepcopy(self.context)
        self.ctx_dict[context]=self.context
        
    def end_context(self):
        
        if self.context.parent!=None:
            self.context.parent.runtime_errors.extend(self.context.runtime_errors)
            self.context.parent.output_stream.update(self.context.output_stream)
            # a={key + str(len(self.parent.output_stream)) if self.parent else key: value for key, value in self.output_stream.items()}
            
            # self.context.parent.output_stream.update(a)
        return self.context
    # def get_context(self, context):
        
    def reset(self):
        self.current_node=self.parse_tree
        self.previous_node=None
        
    def generate_code(self):

        print("Generating code...")
        while True:
            # if not isinstance(self.current_node, AST):
            #     if self.current_node.type=="}":
            #         self.end_context()
            #         self.current_node=self.parse_tree.traverse(self.current_node)
            #         pass
            if self.current_node == None:
                return
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                try:
                    
                    trav=self.parse_tree.traverse(self.current_node)
                    self.current_node = trav

                except AttributeError:
                    break
            if self.current_node == None:
                # print(self.scope_tree)
                print(f"Generate Code: {self.context}")
                if self.context.parent is not None:
                    self.context.parent.runtime_errors.extend(self.context.runtime_errors)
                    try:
                        a={key + len(self.context.parent.output_stream) if self.context.parent else key: value for key, value in self.output_stream.items()}
                        self.context.parent.output_stream.update(a)
                    except AttributeError:
                        pass
                    
                    self.output_stream=self.context.parent.output_stream
                    
                self.end_context()
                print(self.ctx_dict)
                self.reset()
                
                break  # Exit the loop if the tree has been fully traversed
            
        if self.context.parent is not None:
            self.context.parent.runtime_errors.extend(self.context.runtime_errors)
            a={key + len(self.context.parent.output_stream) if self.context.parent else key: value for key, value in self.output_stream.items()}
            self.context.parent.output_stream.update(a)
            # self.output_stream=self.context.parent.output_stream
            self.output_stream=self.context.output_stream
            print(self.output_stream)
            self.runtime_errors.extend(self.context.runtime_errors)
        else:
            
            self.output_stream=self.context.output_stream
            self.runtime_errors=self.context.runtime_errors
            
    # def gen_code(self, node):
    #     print("Generating code for node...")
    #     current_node=node
    #     previous_node=None
    #     while True:
    #         if current_node.root not in self.routines.keys():
    #             previous_node=current_node
    #             current_node = self.parse_tree.traverse(current_node)
    #         else:
    #             self.routines[current_node.root]()
    #             previous_node=current_node
    #             try:
    #                 current_node = self.parse_tree.traverse(current_node)
    #             except AttributeError:
    #                 break
    #         if current_node is None:
    #             # print(self.scope_tree)
    #             break  # Exit the loop if the tree has been fully traversed
            
    def advance(self):
        self.previous_node=self.current_node
        self.current_node = self.parse_tree.traverse(self.current_node)
        self.routines[self.current_node.root]()
        
    
    def allowed_in_loop(self):
        current=self.current_node
        if isinstance(self.current_node.children[0], AST):
            return
        if self.current_node.children[0].value=="up":
            print("Attempting Print...")
            up=InOut(self)
            up.up()
            # self.previous_node=self.current_node
            # self.current_node=None
            # self.runtime_errors+=up.runtime_errors
            
        elif self.current_node.children[0].type=="Identifier":
            # id=Identifier(node=current, 
            #            output_stream=self.output_stream, 
            #            symbol_table=self.symbol_table, 
            #            current_scope=self.current_scope, 
            #            runtime_errors=self.runtime_errors).id_tail()
            # self.runtime_errors+=id.runtime_errors
            if self.current_node.children[1].leaves()[0].type in const.asop:
                val=self.context.symbol_table.find(self.current_node.children[0].value)
                val.assign(op=self.current_node.children[1].leaves()[0].type,value=Evaluators(expression=self.current_node.children[1].leaves(), runtime_errors=self.context.runtime_errors, context=self.context).evaluate(expr=self.current_node.children[1].leaves()[1:], type=val.type) )
            else:
                raise NotImplementedError
        
        else: return

    
    def reg_body(self): #FIXME - IDK if it'll be an issue, but I'm not sure this resets to the previous block after the block ends. 
        if self.current_node.parent.root=="sheesh_declaration":
            # self.current_scope=self.scope_tree.add(self.current_scope, "FUNCTION sheesh")
            self.new_context("FUNCTION sheesh")
            gen=CodeGenerator(self.current_node.children[1], parent=self.context, debugMode=self.debug)
            gen.generate_code()
            self.context.output_stream.update(gen.output_stream)
            
            self.context.runtime_errors.extend(gen.runtime_errors)
            self.context.runtime_errors = list(set(self.context.runtime_errors))
            
            self.end_context()
            
            self.previous_node=self.current_node
            self.current_node=None
        else:
            if self.current_node.parent.parent.root=="func_def":
                # self.new_context(f"FUNCTION {self.current_node.parent.parent.children[2].value}")
                # self.gen_code(self.current_node.children[1])
                # self.end_context()
                pass
                
            else:
                # self.new_context(f"{self.current_node.parent.children[0].value} {self.block_counter}")
                # code=CodeGenerator(parse_tree=self.current_node)
                # self.block_counter+=1
                # self.end_context()
                pass

    def in_loop_body(self):
        if isinstance(self.current_node.parent.children[0], AST):
            # self.current_scope=self.scope_tree.add(context=self.current_scope, scope=f"{self.current_node.parent.children[0].children[0].value} {self.block_counter}")
            self.new_context(f"{self.current_node.parent.children[0].children[0].value} {self.block_counter}")
            code=CodeGenerator(self.current_node, parent=self.context, debugMode=self.debug)
            code.generate_code()
            self.block_counter+=1
        else:
            # self.current_scope=self.scope_tree.add(context=self.current_scope, scope=f"{self.current_node.parent.children[0].value} {self.block_counter}")
            self.new_context(f"{self.current_node.parent.children[0].value} {self.block_counter}")
            self.block_counter+=1
    
    def loop_body_statement(self):
        if isinstance(self.current_node.children[0], AST):
            # self.previous_node=self.current_node
            # self.current_node = self.parse_tree.traverse(self.current_node)
            return
        else:
            if self.current_node.children[0].type=="kung":
                ControlFlow(self).kung()
                
                # self.previous_node=self.current_node
                # self.current_node=self.current_node.parent.children[1]
                
            elif self.current_node.children[0].type=="choose":
                ControlFlow(self).choose_when_default()
            elif self.current_node.children[0].value=="felloff":
                Loops(self).felloff()
            elif self.current_node.children[0].value=="pass":
                Loops(self).pass_()
                
    # def loop_body(self):
    #     main=self.current_node.children[0]
    #     m=CodeGenerator(main, False)
    #     m.current_scope=self.current_scope
    #     m.symbol_table=self.symbol_table
    #     m.generate_code()
    #     if len(self.current_node.children)>1:
    #         next=self.current_node.children[1]
    #         n=CodeGenerator(next, False)
    #         n.current_scope=self.current_scope
    #         n.symbol_table=self.symbol_table
    #         n.generate_code()
        
    def var_or_seq_dec(self):
        type=self.current_node.children[0].value

        if type==const.dtypes.charr:
            id=self.current_node.children[2]
        else:
            id=self.current_node.children[1]

        if isinstance(self.current_node.children[-2], AST):
            if self.current_node.children[-2].children[0].root[2:]=="vardec_tail":
                items=self.current_node.children[-2].children[0].leaves()
                for i,item in enumerate(items):
                    if item.type==",":
                        pass
                    elif item.type=="=":
                        try:
                            self.context.symbol_table.variable(id=id.value,
                                                    type=type,
                                                    ).assign(op=item.type,
                                                            value=Evaluators(
                                                                expression=self.current_node.children[-2].children[0].children[0].children[1].leaves(),
                                                                runtime_errors=self.runtime_errors,
                                                                context=self.context,
                                                            ).evaluate(expr=self.current_node.children[-2].children[0].children[0].children[1].leaves(),
                                                                    type=type))
                        except KeyError as e:
                            e=str(e)[1:-1]
                            self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                    elif item.type=="Identifier":
                        if items[i+1].type=="=":
                            try:
                                op=items[i+1].type
                                value=[]
                                j=0
                                while items[i+j].type not in [const.asop, "," ]:
                                    value.append(items[i+j])#tokens
                                    j+=1
                                value=Evaluators(expression=value, 
                                                runtime_errors=self.runtime_errors, 
                                                scope=self.current_scope, 
                                                symbol_table=self.symbol_table).evaluate()
                                
                                self.context.symbol_table.variable(id=item.value, 
                                                        type=type, 
                                                        scope=self.current_scope).assign(op=op, value=value )
                            except KeyError as e:
                                e=str(e)[1:-1]
                                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                        else:
                            try:
                                self.context.symbol_table.variable(item.value, type, self.current_scope)
                            except KeyError as e:
                                e=str(e)[1:-1]
                                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                    elif item.type=="#":
                        break
                    else:
                        pass
            elif self.current_node.children[-2].children[0].root=="index":
                rows=0
                cols=0
                index=[]
                items=self.current_node.children[-2].children[0].leaves()
                k=0
                while items[k].type not in [const.asop]:
                    index.append(items[k])
                    
                    if items[k].type=="]":
                        break
                    k+=1
                    
                try:
                    rows=Evaluators(expression=index, 
                                    runtime_errors=self.runtime_errors, 
                                    context=self.context).evaluate(expr= index[1:-1], type=const.dtypes.whole)
                    if len(self.current_node.children[-2].children)>1:
                        items=self.current_node.children[-2].children[1].leaves()
                        if items[0].type=="[":
                            col=[]
                            k=0
                            while items[k].type not in [const.asop]:
                                col.append(items[k])
                                if items[k].type=="]":
                                    break
                                k+=1
                            cols=Evaluators(expression=index, 
                                            runtime_errors=self.runtime_errors, 
                                            context=self.context).evaluate(expr=col[1:-1], type=const.dtypes.whole)
                        elif items[0].type=="=":
                            init=[]
                            
                            for item in items:
                                if item.type in ["=", "{"]:
                                    pass
                                elif item.type==",":
                                    pass
                                elif item.type=="}":
                                    break
                                else:
                                    init.append(item)
                            try:
                                self.context.symbol_table.sequence(id=id.value, type=type, rows=rows, cols=cols).initialize(init)
                            except ValueError as e:
                                e=str(e)
                                self.context.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e].format(rows)))
                        else:
                              
                            try:    
                                self.context.symbol_table.sequence(id=id.value, type=type, rows=rows, cols=cols)
                            except KeyError as e:
                                e=str(e)[1:-1]
                                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e].format(rows)))
                    
                    if len(self.current_node.children[-2].children)==1:
                        if isinstance(self.current_node.children[-2].children[1].children[0], AST):
                            if self.current_node.children[-2].children[1].children[0].root=="index":
                                
                                items=self.current_node.children[-2].children[1].leaves()
                                for i,item in enumerate(items):
                                    if item.type==",":
                                        pass
                                    elif item.type=="Identifier":
                                        if items[i+1].type=="=":
                                            op=items[i+1].type
                                            value=[]
                                            j=0
                                            while items[i+j].type not in [const.asop, "," ]:
                                                value.append(items[i+j])
                except KeyError as e:
                    e=str(e)[1:-1]
                    self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                        
            else:
                try:    
                    self.context.symbol_table.sequence(id=id, type=type, rows=rows, cols=cols)
                except KeyError as e:
                    e=str(e)[1:-1]
                    self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
        else:
            try:
                self.context.symbol_table.variable(id=id, type=type)
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))

    def const_type(self):  
        type=self.current_node.children[0].value
        id=self.current_node.children[1]
        if self.current_node.children[-1].children[0].root=="index":
            index=[]
            items=self.current_node.children[-1].children[0].leaves()
            k=0
            while items[k].type not in [const.asop]:
                index.append(items[k])
                
                if items[k].type=="]":
                    break
                k+=1
                
            try:
                rows=Evaluators(expression=index, 
                                runtime_errors=self.runtime_errors, 
                                context=self.context).evaluate(expr= index[1:-1], type=type)
                if len(self.current_node.children[-1].children)>1:
                    items=self.current_node.children[-1].children[1].leaves()
                    if items[0].type=="[":
                        col=[]
                        k=0
                        while items[k].type not in [const.asop]:
                            col.append(items[k])
                            if items[k].type=="]":
                                break
                            k+=1
                        cols=Evaluators(expression=index, 
                                        runtime_errors=self.runtime_errors, 
                                        context=self.context).evaluate(expr=col[1:-1], type=type)
                        
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=items[k], expected=se.expected[e]))
                
            if len(self.current_node.children[-1].children)>1:
                if isinstance(self.current_node.children[-1].children[1].children[0], AST):
                    if self.current_node.children[-1].children[1].children[0].root=="index":
                        items=self.current_node.children[-1].children[1].leaves()
                        for i,item in enumerate(items):
                            if item.type==",":
                                pass
                            elif item.type=="Identifier":
                                if items[i+1].type=="=":
                                    op=items[i+1].type
                                    value=[]
                                    j=0
                                    while items[i+j].type not in [const.asop, "," ]:
                                        value.append(items[i+j])
                    
            else:
                try:
                    self.context.symbol_table.constant_seq(id=id, type=type, rows=rows, cols=cols)
                except KeyError as e:            
                    e=str(e)[1:-1]
                    self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
        else:
            try:
                            self.context.symbol_table.constant_var(id=id.value,
                                                    type=type,
                                                    value=Evaluators(
                                                                expression=self.current_node.children[-1].children[0].children[1].leaves(),
                                                                runtime_errors=self.runtime_errors,
                                                                context=self.context,
                                                            ).evaluate(expr=self.current_node.children[-1].children[0].children[1].leaves(),
                                                                    type=type))
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
    
    def control_flow_statement(self):
        if self.current_node.children[0].type=="kung":
            ControlFlow(codegen=self).kung()
                # node=self.current_node, 
                #         output_stream=self.output_stream, 
                #         symbol_table=self.symbol_table, 
                #         current_scope=self.current_scope, 
                #         runtime_errors=self.runtime_errors).kung()
            
        elif self.current_node.children[0].type=="choose":
            ControlFlow(node=self.current_node, 
                        output_stream=self.output_stream, 
                        symbol_table=self.symbol_table, 
                        current_scope=self.current_scope, 
                        runtime_errors=self.runtime_errors).choose_when_default()
        else:
            raise ValueError("ERROR??????????") #NOTE - huy alisin mo to

    
    def ehkung_statement(self):
        raise NotImplementedError
    
    def looping_statement(self):
        if self.current_node.children[0].type=="bet":
            Loops(self).bet_whilst()
            
            
        elif self.current_node.children[0].type=="for":
            try:
                self.context.symbol_table.variable(id=self.current_node.children[3].value,
                                        type=self.current_node.children[2].value,
                                        ).assign(op=self.current_node.children[4].type,
                                                value=Evaluators(expression=self.current_node.children[5],
                                                                                            runtime_errors=self.runtime_errors,
                                                                                            context=self.context).evaluate(expr=self.current_node.children[5].leaves(), type=self.current_node.children[2].value))
            except KeyError as e:
                e=str(e)[1:-1]
                return self.context.runtime_errors.append(RError(error=getattr(se, e), token=self.current_node.children[3], expected=se.expected[e]))                 
            
            Loops(codegen=self).for_()    
    
    # def yeet_statement(self): #NOTE idk dito
    #     return Evaluators(
    #         expression=self.current_node.children[1],
    #         runtime_errors=self.runtime_errors,
    #         scope=self.current_scope,
    #         symbol_table=self.symbol_table
    #     ).evaluate(expr=self.current_node.children[1].leaves(), type=self.)
    
    def func_def(self):
        """  
        To do:
        1. 
        2.  
        """
        dtype=self.current_node.children[1].leaves()[0].value
        id=self.current_node.children[2]
        pars=self.current_node.children[3]
        tail=self.current_node.children[-1]
        parameters=[]
        self.new_context(f"FUNCTION {id.value}")
        for i,param in enumerate(parameters.leaves()):
            if param.type in const.dtypes:
                type=param.type
                id=parameters[i].value
                self.context.symbol_table.variable(id=id.value, type=type)
        self.end_context()    
        try:
            self.context.symbol_table.function(id=id.value,
                                    return_type=dtype,
                                    parameters=parameters,
                                    body=tail,)
        except KeyError as e:
            e=str(e)[1:-1]
            self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))

        

    
# import sys
# sys.path.append(".")
# from source.CodeGeneration.cg2 import CodeGenerator
# from source.core.symbol_table import Function
# from source.core.AST import AST



class FuncRunner:
    def __init__(self, func:Function, arguments):
        self.func=func
        self.body=func.func_body
        # self.codegen=codegen
        self.arguments=arguments
        self.runtime_errors=[]
        self.debug=False
        
    def run(self):
        run=CodeGenerator(self.body, self.debug)
        run.current_scope=f"FUNCTION {self.func.id}"
        for i,arg in enumerate(self.arguments):
            run.symbol_table.variable(
                name=self.func.parameters[i].id, 
                dtype=self.func.parameters[i].type, 
                scope=run.current_scope
            ).assign("=", arg)
            
        return run.generate_code()



class Loops:
    """  
    Algorithm:
    1. Check the type of loop
    2. Get the loop body
    3. Traverse the loop body
    4. Execute the loop body
    5. When loop body has been executed, check condition
    6. If condition is met, go to loop_body node; re-execute loop body

    """
    def __init__(self, codegen) -> None:
        # self.node=node
        # self.leaves=self.node.leaves()
        # self.output_stream=output_stream
        # self.symbol_table:SymbolTable=symbol_table
        # self.current_scope=current_scope
        # self.runtime_errors=runtime_errors
        self.codegen=codegen
        self.debug=True

    def bet_whilst(self):
        condition=self.codegen.current_node.children[4].leaves()
        loop_body=self.codegen.current_node.children[1]
        while Evaluators(runtime_errors=self.codegen.runtime_errors, 
                         expression=condition, 
                         context=self.codegen.context).evaluate(expr=condition, type=const.dtypes.sus)==True:
            
            cd=CodeGenerator(parse_tree=loop_body, parent=self.codegen.context, )
            cd.generate_code()
            self.previous_node=self.codegen.current_node
            self.codegen.current_node = self.codegen.parse_tree.traverse(loop_body)
            
            # self.routines[self.node.root]()


    def for_(self):
            iterator=self.codegen.context.symbol_table.find_var(self.codegen.current_node.children[3].value)
            # iterator.assign(op="=",value= const.types[iterator.type](self.node.children[5].leaves()[0].numerical_value))
            # end=self.node.children[7].leaves()[0].numerical_value #idk if this'll work for seq and funcs
            end=Evaluators(expression=self.codegen.current_node.children[7].leaves(),
                                runtime_errors=self.codegen.runtime_errors,
                                context=self.codegen.context,
                                ).evaluate(type=const.dtypes.whole, expr=self.codegen.current_node.children[7].leaves())
            try:
                step=int(self.codegen.current_node.find_node("step_statement").leaves()[1].numerical_value)
                
            except AttributeError as e:
                step=1

            loop_body=self.codegen.current_node.children[-1]
            
            self.codegen.block_counter+=1
            output=None
            while True:
                
                if iterator.value ==end:
                    break
                
                code=CodeGenerator(parse_tree=loop_body.children[1], parent=self.codegen.context ,debugMode=self.debug) 
                
                code.new_context(f"for {self.codegen.block_counter}");
                code.current_node=loop_body.children[1]
                code.generate_code()
                output=code.output_stream
                

                iterator.assign("+=",step)
                print("Iterator: ", iterator.value, "End: ", end, "Step: ", step)
                
            
            self.codegen.output_stream=output
            # code.end_context()
            if self.debug:
                print(f"For Loop: \n\tIterator: {iterator}\n\t End: {end}\n\t Step: {step}")
            print(output)
            self.codegen.current_node=self.codegen.current_node.parent.parent.parent.parent.children[0] #FIXME - idk
            

    # def to(self):
    #     raise NotImplementedError
    
    def felloff(self):
        #statement that should break loops
        self.codegen.previous_node=self.codegen.current_node
        self.codegen.current_node = self.codegen.current_node.parent.children[1]
        self.codegen.routines[self.codegen.current_node.root]()
    

    # def step(self):
    #     raise NotImplementedError
    
    def pass_(self):
        if self.codegen.current_node.root=="loop_body_statement":
            self.codegen.previous_node=self.codegen.current_node
            self.codegen.current_node = self.codegen.current_node.parent.children[1]



# import sys
# sys.path.append(".")
# # from source.CodeGeneration.Functionality.Functionality import Functionality
# from source.CodeGeneration.Functionality.Evaluators import Evaluators
# import source.core.constants   as const


class ControlFlow:
    """  
    Algorithm:
    1. Check Statement Type
    2. Get condition
    4. Get main bodyp
    5. Get sub-bodies
    6. Evaluate condition, if success, go to main_body node; execute main body
    7. If condition is not met, go to fail node; execute fail node
    8. If fail node is not present, pass
    
    For choose:
    1. Get Check Value
    2. Get bodies5
    3. Evaluate check value == body value
    4. If success, execute node; else, check other bodies.
    5. If no body matches, go to default node; execute default node

    """
    def __init__(self, codegen) -> None:
        self.codegen=codegen
        # self.debug=functionality.debug
        # self.node=node
        # self.output_stream=output_stream
        
    def kung(self):
        #initializers
        condition=self.codegen.current_node.children[2].leaves()
        success=self.codegen.current_node.children[4]
        if len(self.codegen.current_node.children)==5:
            # fail=self.codegen.current_node.parent.children[0]
            fail=None
            
        else:
            fail=self.codegen.current_node.children[-1] 

        eval=Evaluators(expression=condition, runtime_errors=self.codegen.runtime_errors, context=self.codegen.context).evaluate(type=const.dtypes.sus,expr=condition)
        if eval==True:
            print("Kung Succeeded")
            code=CodeGenerator(parse_tree=success, parent=self.codegen.context, debugMode=self.codegen.debug)
            
            code.generate_code()
            self.codegen.previous_node=self.codegen.current_node
            self.codegen.current_node=self.codegen.current_node.parent.children[1]
            return
            # self.codegen.current_node=self.codegen.current_node.parent.parent.parent.parent.parent.parent.parent.children[1]
            # self.codegen.current_node = self.codegen.parse_tree.traverse(success)
            # # try:
            # self.codegen.routines[self.codegen.current_node.root]()
            # except KeyError:
            #     self.codegen.advance()

        else:
            if fail==None:
                try:
                    print("Kung Statement Failed")
                    # fail=self.codegen.current_node.parent.children[1]
                    # self.codegen.previous_node=self.codegen.current_node
                    # self.codegen.current_node=fail
                    self.codegen.previous_node=self.codegen.current_node
                    self.codegen.current_node=self.codegen.current_node.parent.children[1]
                    return
                    # self.codegen.current_node.children[-2].children[0].children[1].leaves(),
                except IndexError:
                    self.codegen.current_node=self.codegen.current_node.parent.parent.children[1]
                    return
                # self.codegen.current_node = self.codegen.parse_tree.traverse(fail)
                # self.codegen.routines[self.codegen.current_node.root]()
                
            else:
                while True:
                    try:
                        # self.codegen.current_node = self.codegen.semantic.parse_tree.traverse(fail)
                        # self.codegen.routines[self.codegen.current_node.root]()
                        self.codegen.gen_code(fail)
                        break  # if the above lines don't raise an exception, break the loop
                    except KeyError:
                        while self.codegen.current_node.root!="statement":
                            print(self.codegen.current_node.root)
                            self.codegen.current_node = self.codegen.previous_node
                            self.codegen.previous_node=self.codegen.previous_node.parent
                        fail= self.codegen.current_node=self.codegen.current_node.children[1].children[0].children[0]


    def ehkung(self):
        """ 
        Expects call from ehkung statement.
        """
        condition=self.codegen.current_node.children[2]
        body=self.codegen.current_node.children[-1]

        if Evaluators(expression=condition,runtime_errors= self.codegen.runtime_errors, context=self.codegen.context):
            self.codegen.current_node = self.codegen.semantic.parse_tree.traverse(body)
            self.previous_node=self.codegen.current_node
            self.codegen.routines[self.codegen.current_node.root]()
        else:
            return

    
    def deins(self):
        """ Expects call from a condtail node """
        body=self.codegen.current_node.children[1]
        self.codegen.current_node = self.codegen.semantic.parse_tree.traverse(body)
        self.previous_node=self.codegen.current_node
        self.codegen.routines[self.codegen.current_node.root]()
    
    def choose_when_default(self):
        """
        """
        checker=None
        body=None
        conditions=None
    
    # def when(self):
    #     raise NotImplementedError
    
    # def default(self):
    #     raise NotImplementedError
       
class InOut:
    """  
    This class contains the input and output functions.
    It takes a node, and an output stream as input.
    Algorithm:
    1. Determine statement type
    2. Get variables
    3. If up, get format specifiers, perform type checking, and format the string
    4. If pa_mine, get format specifier. get input as format specifier type. If type is not correct, raise error. If correct, assign to var

    """
    def __init__(self, codegen) -> None:
        self.codegen=codegen
        # self.node=node
        # self.leaves=self.node.leaves()
        # self.output_stream=output_stream
        # self.symbol_table:SymbolTable=symbol_table
        # self.current_scope=current_scope
        # self.runtime_errors:list=runtime_errors

    def pa_mine(self):
         """  
         pa_mine can only be used in expressions (?)

         Algorithm:
         1. Get format specifier and type
         2. Enable input
         3. Get Input
         4. Check if input matches type
         5. If match, return input as format specifier type
         6. If not, raise error
         7. Assign input to variable
         
         """
         raise NotImplementedError
    
    def up(self):
            matched=self.codegen.current_node.leaves()

            vars=[]
            vars2=[]
            text=''
            val=[]
            # type=None

            for i,match in enumerate(reversed(matched)):
                if match.type=="Identifier":
                    try:
                        value=self.codegen.context.symbol_table.find(match.value)
                        if isinstance(value, Sequence):
                            print(isinstance(value, Sequence))
                            try:
                                value=value.get(int(matched[i+1].numerical_value))
                            except ValueError as e:
                                e=str(e)
                                self.codegen.context.runtime_errors.append(RError(error=getattr(se, e), token=matched[i+1], expected=se.expected[e]))
                        elif isinstance(value, Function):
                            value.execute([m for m in matched[i+2:] if m.type!=")"])
                        elif isinstance(value, Variable):
                            print(isinstance(value, Variable))
                            value=value
                        vars.append(value)
                        vars2.append(value)
                        # type=value.type
                        # print(type)
                    except KeyError as e:
                        e=str(e)[1:-1]
                        self.codegen.context.runtime_errors.append(RError(error=getattr(se, e), token=match, expected=se.expected[e]))
                        
                elif match.type in const.literal_types and match.type!="Text" and matched[i+2].type not in ["]", "["]:
                    print(matched[i+2].type)
                    vars.append(match)
                elif match.type=="Text":
                    text=match.value
                    print(text)
                elif match.type=="(":
                    break
    

            # Find all format specifiers in the text
            format_specifiers = re.findall(f"\$[{''.join(const.format_spec.keys())}]", text)
            # print(format_specifiers)
            # Check if the number of format specifiers matches the number of variables
            if len(format_specifiers) != len(vars):
                err_msg="Number of format specifiers does not match number of variables"
                if len(vars)<len(format_specifiers):
                    expected=f"{len(format_specifiers)} variables of type"
                    for format in format_specifiers:
                            expected+=f" {self.own_specifiers[format[1:]]},"
                            
                    self.runtime_errors.append(
                        RError(error=err_msg, token=self.node.children[0], expected=expected)
                        )
                elif len(vars)>len(format_specifiers):
                    expected=f"{len(vars)} format specifiers of type"
                    for var in vars:
                        if var.type=="Identifier":
                            expected+=f" {var.dtype},"
                        else:
                            expected+=f" {var.type},"
                    self.codegen.context.runtime_errors.append(
                        RError(error=err_msg, token=self.codegen.current_node.children[0], expected=expected)
                        )
            else:

            # For each format specifier, check if the corresponding variable has the correct type
                vars=list(reversed(vars))
                for i in range(len(format_specifiers)):
                    # Get the format specifier (remove the dollar sign)
                    format_specifier = format_specifiers[i][1:]
                    # Get the corresponding variable
                    # var = const.py_types[vars[i].type](vars[i].value)
                    var = vars[i].value
                    if var==None:
                         self.runtime_errors.append(
                              RError(error=se.VAR_UNDEF, token=vars2[i], expected=se.expected["VAR_UNDEF"])
                         )
                         return
                    # print(type(var))
                    # if isinstance(var, const.types[type]):
                    #      print("yeah")
                    # if type(var)==str and str(var).isdigit():
                    #      raise NotImplementedError

                    if vars[i].type in ["Whole", "Dec"] and ((float(var) >1 or float(var)<-1) and float(var)%1==0):
                            var=const.format_spec[format_specifier](var)
                    val.append(var)
                    # Check if the variable has the correct type
                    if type(var) != const.format_spec[format_specifier]:
                        
                        err_msg=f"Variable {vars[i].value} does not match format specifier {format_specifier}"
                        expected=f"{const.own_specifiers[format_specifier]} for format specifier ${format_specifier}"
                        self.codegen.runtime_errors.append(
                    RError(error=err_msg, token=self.codegen.current_node.children[0], expected=expected)
                    )
                        # raise TypeError(f"Variable {var} does not match format specifier {format_specifier}")

                # Replace the format specifiers with {} for string formatting
                for format_specifier in format_specifiers:
                    text = text.replace(format_specifier, "{}")

                # Format the string with the variables
                formatted_text = text.format(*val)

                # Print the formatted string
                if formatted_text :
                    
                    self.codegen.context.output_stream[self.codegen.print_ctr]=formatted_text
                    self.codegen.print_ctr+=1
                # else:
                #     occurence=1
                #     self.output_stream[formatted_text]=occurence
                print(self.codegen.output_stream)

    