import sys
sys.path.append( '.' )
from source.core.symbol_table import Token, SymbolTable
from source.core.error_handler import SemanticError as SemError
from source.core.error_types import Semantic_Errors as se
from source.core.AST import AST



GBL="Global"
LOCAL="Local"
VAR="Variable"
FUNC="Function"
MOD="Module"
SEQ="Sequence"
IMP="Imported"
PARAM="Parameter"

CONST="Constant"


class SemanticAnalyzer:
    """  
    The semantic analyzer traverses the parse tree.
    The semantic analyzer will check the AST for any semantic errors.
    The SA must also assign identifiers to the symbol table.
    The SA will check:
        - Variable Declaration
        - Variable Use
        - Function Declaration
        - Function Use
        - Function Return Type
        - Function Arguments
        - Function Calls
        - Variable Assignment
        - Sequence Size
        - Sequence Access
        - Sequence Assignment


    Things to check:
        - Identifiers
        - Parameters/ Arguments
        - Return Types
        - Sequence Size
        - Sequence Access
        - Sequence Assignment/ Init

    """
    
    def __init__(self, parse_tree:AST) -> None:
        self.parse_tree:AST=parse_tree
        # self.matched=matched
        self.semantic_errors: list[se]=[]
        self.semantic_expected=[]

        self.semantic_errors: list[SemError]=[]
        self.id_vars:SymbolTable=SymbolTable()
        self.id_funcs:SymbolTable=SymbolTable()

        self.req_type=None

        self.current_node:AST=self.parse_tree


        self.check=Check(self)
        self.create=Create(self)



        self.buffer=[]

        self.nearest_id=None
        
        self.routines={

#SECTION: ID TYPE ENFORCEMENT 

            "import_prog": self.import_prog,
            "import_tail": self.import_tail,
            "in_param": self.in_param,
            "allowed_in_loop": self.allowed_in_loop,
            "id_tail": self.id_tail,
            "var_or_seq_dec": self.var_or_seq_dec,
            "more_whl_var": self.more_whl_var,
            "more_dec_var": self.more_dec_var,
            "more_sus_var": self.more_sus_var, 
            "more_txt_var": self.more_txt_var, 
            "more_chr_var": self.more_chr_var, 
            "charr_value": self.charr_value, 
            "const_type": self.const_type, 
            "more_whl_const": self.more_whl_const, 
            "more_dec_const": self.more_dec_const, 
            "more_sus_const": self.more_sus_const, 
            "more_txt_const": self.more_txt_const,
            "more_chr_const": self.more_chr_const,
            "control_flow_statement": self.control_flow_statement,
            "looping_statement": self.looping_statement,
            "loop_body_statement": self.loop_body_statement,
            "func_def": self.func_def,
            "id_as_val": self.id_as_val,



            
            }
        
    def __repr__(self) -> str:
        return f"SemanticAnalyzer({self.parse_tree})"

    def analyze(self):
        while True:
            if self.current_node.root not in self.routines.keys():
                self.current_node = self.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.current_node = self.parse_tree.traverse(self.current_node)
            if self.current_node is None:
                break  # Exit the loop if the tree has been fully traversed


    def import_prog(self):
        raise NotImplementedError

    def import_tail(self):
        raise NotImplementedError

    def in_param(self):
        raise NotImplementedError


    def allowed_in_loop(self):
        try:
            if self.current_node.children[0].type=="Identifier":
                self.nearest_id=self.current_node.children[0]
            else: 
                # raise ValueError("No Identifier Found")
                pass
        except AttributeError:
            pass

    def id_tail(self):
        tail_map={
            "(": self.check.func,
            "one_dim": self.check.seq,
            "assign_op": self.check.var,
        }

        try:
            tail_map[self.current_node.children[0].root]()
        except AttributeError:
            tail_map[self.current_node.children[0].value]()

    def var_or_seq_dec(self):
        try:
            if self.current_node.children[1].type=="Identifier":
                self.nearest_id=self.current_node.children[1]
                self.create.new_id(scope=LOCAL, type=self.current_node.children[0].value, attribute=VAR)
            else:
                raise ValueError("No Identifier Found")
        except AttributeError:
            raise AttributeError("No Identifier Found")
    
    def more_whl_var(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=LOCAL, type="whole", attribute=VAR)
    def more_dec_var(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=LOCAL, type="dec", attribute=VAR)
    def more_sus_var(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=LOCAL, type="sus", attribute=VAR)
    def more_txt_var(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=LOCAL, type="text", attribute=VAR)
    def more_chr_var(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=LOCAL, type="charr", attribute=VAR)
    

    def charr_value(self):
        if self.current_node.children[0].type=="Identifier":
            self.nearest_id=self.current_node.children[0]
            self.check.var()
            self.check.var_value()
            # self.check.var_type() #TODO - Implement this function
            # self.check.scope() #TODO - Implement this function
    

    def const_type(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type=self.current_node.children[0], attribute=CONST)
    

    def more_whl_const(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type="whole", attribute=CONST)
    def more_dec_const(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type="dec", attribute=CONST)
    def more_sus_const(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type="sus", attribute=CONST)
    def more_txt_const(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type="text", attribute=CONST)
    def more_chr_const(self):
        if self.current_node.children[1].type=="Identifier":
            self.nearest_id=self.current_node.children[1]
            self.create.new_id(scope=GBL, type="charr", attribute=CONST)
    

    def control_flow_statement(self):
        if self.current_node.children[2].type=="Identifier" and self.current_node.children[0].value=="choose":
            self.nearest_id=self.current_node.children[2]
            self.check.var()
            self.check.var_value()
            # self.check.scope() #TODO - Implement this function

    def looping_statement(self):
        if self.current_node.children[2].type=="Identifier" and self.current_node.children[0].value=="for":
            self.nearest_id=self.current_node.children[2]
            self.check.var()
            # self.check.var_value()
            # self.check.scope() #TODO - Implement this function

    def loop_body_statement(self):
        if self.current_node.children[2].type=="Identifier" and self.current_node.children[0].value=="choose":
            self.nearest_id=self.current_node.children[2]
            self.check.var()
            self.check.var_value()
            # self.check.scope() #TODO - Implement this function

    def func_def(self):
        if self.current_node.children[2].type=="Identifier":
            self.nearest_id=self.current_node.children[2]
            self.create.new_func(scope=GBL, type=self.current_node.children[1].value)
        elif self.current_node.children[3].type=="Identifier":
            self.nearest_id=self.current_node.children[3]
            self.create.new_func(scope=LOCAL, type=self.current_node.children[1].value)
    

    def id_as_val(self):
        if self.current_node.children[0].type=="Identifier":
            self.nearest_id=self.current_node.children[0]
            self.check.var()
            self.check.var_value()
            # self.check.var_type() #TODO - Implement this function
            # self.check.scope() #TODO - Implement this function


#SECTION - ID CHECKERS

    



   
            
    
    
    # def find_type(self, Token):
        
    #region SEMANTIC CHECKS

    def semantic_error(self, error, token, expected):
        self.semantic_expected.append(expected)
        self.semantic_errors.append(SemError(error=error, line=token.line, toknum=token.position, value=token.value, expected=expected))
        
    

   


#endregion SEMANTIC CHECKS



class Check:
        
        def __init__(self, semantic: SemanticAnalyzer) -> None:
            self.semantic=semantic


        def func(self):
            id=self.semantic.nearest_id
            if id not in self.semantic.id_funcs.keys():
                exp=f"Declared Function {id.value}"
                err=se.FUNC_UNDECL
                self.semantic.semantic_error(err, id, exp)
                return
            
        def seq(self):
            id=self.semantic.nearest_id
            if id not in self.semantic.id_vars.keys():
                exp=f"Declared Sequence {id.value}"
                err=se.SEQ_UNDECL
                self.semantic.semantic_error(err, id, exp)
                return
            
        def var(self):
            id=self.semantic.nearest_id
            if id.value not in self.semantic.id_vars.keys():
                exp=f"Declared Variable {id.value}"
                err=se.VAR_UNDECL
                self.semantic.semantic_error(err, id, exp)
                return
        

        def var_value(self):
            id=self.semantic.nearest_id
            if id.numerical_value==None:
                exp=f"Value for Variable {id.value}"
                err=se.VAR_UNDEF
                self.semantic.semantic_error(err, id, exp)
                return


        def declared(self, id:Token):
            if any(id.value == token.value for token in self.id_vars) or any(id.value == token.value for token in self.id_funcs):            return True
            else: return False


        def check_var_declared(self):
            if self.matched[-1].type == "Identifier":
                id=self.matched[-1]
            else: id=self.matched[-2]
            if not self.declared(id):
                exp=f"Declared {id.value}"
                err=se.VAR_UNDECL
                self.semantic_error(err, id, exp)
                return
            else: return True
    
        def check_func_declared(self):
            id=self.matched[-2]
            if id in self.id_funcs:
                exp=f"Declared {id.value}"
                err=se.FUNC_UNDECL
                self.semantic_error(err, id, exp)
        
        def check_var_operand(self, id:Token):
            if self.declared(id):
                self.semantic_expected.append(self.req_type)
                self.semantic_errors.append(SemError(error=se.VAR_OPERAND_INVALID, line=id.line, toknum=id.position, value=id.value, expected=self.semantic_expected))

        def check_req_type(self, id:Token):
            if self.declared(id) and id.dtype != self.req_type:
                self.semantic_expected.append(f"Variable of Type {self.req_type}")
                self.semantic_errors.append(SemError(error=se.VAR_OPERAND_INVALID, line=id.line, toknum=id.position, value=id.value, expected=self.semantic_expected))

        @staticmethod
        def find_id(identifier:str, tokens:list[Token])->Token:
            """ 
            After syntax analysis, finds the identifier token in the program.
            From first to last index, could be implemented in a function that pops previously scanned tokens.
            """
            for i,token in enumerate(tokens):
                if token.type == "Identifier" and token.value==identifier :
                    return token

        @staticmethod
        def find_func(identifier:str, tokens:list[Token])->Token:
            for token in tokens:
                if token.type=="Identifier" and token.value==identifier and token.attribute=="Function":
                    return token
        

class Create:

    def __init__(self, semantic:SemanticAnalyzer) -> None:
        self.semantic=semantic

    def var_load_type(self, id:Token):
        self.req_type=id.dtype


    def new_id(self, type, scope=LOCAL,  attribute=None):
        id=self.semantic.nearest_id #NOTE - idk if this is the right way to do this
        if id.value not in self.semantic.id_vars.keys():
            id.dtype=type
            id.attribute=attribute
            id.scope=scope

            self.semantic.id_vars.add(id)
        else:
            self.semantic.semantic_error(se.VAR_REDECL, id, f"Variable {id.value}")


    def new_func(self, scope, type, attribute=FUNC):
        id=self.semantic.nearest_id
        if id.value not in self.semantic.id_funcs.keys():
            id.dtype=type
            id.attribute=attribute
            id.scope=scope

            self.semantic.id_funcs.add(id)
        else:
            self.semantic.semantic_error(se.FUNC_REDECL_INSCOPE, id, f"Function {id.value}")


    #region Semantic Rules
#!SECTION: ID TYPE ENFORCEMENT 
    @staticmethod
    def id_import(token:Token)->Token:
        token.attribute=IMP
        token.scope=GBL
        return token
    
    @staticmethod
    def id_module(token:Token)->Token:
        token.attribute=MOD
        token.scope=GBL
        return token

    @staticmethod
    def id_decl(token:Token, dtype:str, scope=LOCAL)->Token:
        if scope in [GBL, LOCAL]:
            token.attribute=VAR
            token.dtype=dtype
            token.scope=scope
            return token
        else: raise ValueError("Wrong Scope Val")


    @staticmethod
    def id_decl_param(token:Token, type:str)->Token:
        token.attribute=PARAM
        token.dtype=type
        token.scope=LOCAL
        return token

    @staticmethod
    def id_as_sequence(token:Token)->Token:
        token.attribute=SEQ
        return token

    @staticmethod
    def id_func_invoc(token:Token)->Token:
        token.attribute=FUNC
        return token

    @staticmethod
    def id_funcdef(token:Token, type:str)->Token:
        token.attribute=FUNC
        token.scope=GBL
        token.dtype=type
        return token
    
    @staticmethod
    def id_assign(token:Token)->Token:
        token.attribute=VAR

        return token
    
#endregion
