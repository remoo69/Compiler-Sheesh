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
        
        """ 
        Variables:
            Var Undeclared 
            Var Undefined
            Var Redeclaration in Scope

        Functions:
            Func Undeclared
            Func Undefined
            Func Redeclaration in Scope 

        Arguments:
            Var Argument Type Invalid
            Value Argument Type Invalid

        Return:
            Func Return Variable Type Invalid
            Func Return Value Type Invalid

        Operands:
            Var Operand Type Invalid
            Value Operand Type Invalid
            Func Operand Type Invalid

        Array:
            Wrong Number of Values
            Wrong Number of Dimensions
            Wrong Type of Values (Var)

        Array Index:
            Wrong type of index
            Out of Bounds

        Array Assignment:
            Wrong type of value
            Wrong type of index
            Out of Bounds

        Array Access:
            Wrong type of index
            Out of Bounds

        
          
        """
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


        ZERO_DIV="Division by Zero"
        OUT_OF_BOUNDS="Out of Bounds"
        WRONG_NUM_VALUES="Wrong Number of Values"
        WRONG_NUM_DIMENSIONS="Wrong Number of Dimensions"

        WRONG_INDEX_TYPE="Wrong Type of Index"
