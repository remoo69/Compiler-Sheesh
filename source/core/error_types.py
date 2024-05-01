from enum import Enum
class ErrorTypes:

#ANCHOR - LEXICAL ERRORS
    Lex_Errors={
        # "":{},

    }
    
#ANCHOR - SYNTAX ERRORSS
    Syntax_Errors={}

#ANCHOR - SEMANTIC ERRORS
class Semantic_Errors:
        VAR_UNDECL="Undeclared Variable"
        VAR_UNDEF="Undefined Variable"
        VAR_REDECL_INSCOPE= "Redeclaration of Variable in Scope"
        
        FUNC_UNDECL="Undeclared Function"
        FUNC_UNDEF="Undefined Function"
        FUNC_REDECL_INSCOPE= "Redeclaration of Function"


        VAR_ARG_INVALID="Variable Argument Type is Invalid"
        VAL_ARG_INVALID= "Value Argument Type is Invalid"

        FUNC_RETURN_VAR="Returned Variable Type is Invalid"
        FUNC_RETURN_VAL="Returned Value Type is Invalid"


        VAR_OPERAND_INVALID="Variable Operand Type is Invalid"
        VAL_OPERAND_INVALID="Value Operand Type is Invalid"

        FUNC_OPERAND_INVALID="Function Operand Type is Invalid"
        WTYPE_RETURN_VAL="Returned Value Type is Invalid"
