from dataclasses import dataclass
import sys
sys.path.append( '.' )
from source.core.symbol_table import Token
from source.core.error_handler import SemanticError as se


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
    semantic_errors: list[se]=[]

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
        
    

