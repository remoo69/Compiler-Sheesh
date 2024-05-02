import sys
sys.path.append( '.' )
from source.core.symbol_table import Token
from source.core.error_handler import SemanticError as SemError
from source.core.error_types import Semantic_Errors as se


GBL="Global"
LOCAL="Local"
VAR="Variable"
FUNC="Function"
MOD="Module"
SEQ="Sequence"
IMP="Imported"
PARAM="Parameter"


class SemanticAnalyzer:
    """  
    The semantic analyzer must work in parallel with the syntax analyzer. As such, using this module requires the syntax analyzer.
    The semantic analyzer will check the AST for any semantic errors.
    The SA must be used within the syntax analyzer.
    """
    
    def __init__(self, parse_tree) -> None:
        self.parse_tree=parse_tree
        self.semantic_errors: list[se]=[]

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
            
    
    
    # def find_type(self, Token):
        
    #region SEMANTIC CHECKS

    def semantic_error(self, error, token, expected):
        self.semantic_expected.append(expected)
        self.semantic_errors.append(SemError(error=error, line=token.line, toknum=token.position, value=token.value, expected=self.semantic_expected))
        
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

    def var_load_type(self, id:Token):
        self.req_type=id.dtype


    # def 
#endregion SEMANTIC CHECKS



