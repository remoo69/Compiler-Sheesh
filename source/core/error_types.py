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

        CONST_REDECL="Redeclaration of Constant"
        CONST_UNDECL="Undeclared Constant"
        CONST_REASSIGN="Redefinition of Constant"

        VAR_UNDECL="Undeclared Variable"
        VAR_UNDEF="Undefined Variable"
        VAR_REDECL_INSCOPE= "Redeclaration of Variable in Scope"
        VAR_SCOPE_INVALID="Variable Scope is Invalid"

        SEQ_UNDECL="Undeclared Sequence"
        
        WRONG_NUM_ARGS="Wrong Number of Arguments"
        
        FUNC_UNDECL="Undeclared Function"
        FUNC_UNDEF="Undefined Function"
        FUNC_REDECL_INSCOPE= "Redeclaration of Function Identifer"


        VAR_ARG_INVALID="Variable Argument Type is Invalid"
        VAL_ARG_INVALID= "Value Argument Type is Invalid"

        FUNC_RETURN_VAR="Returned Variable Type is Invalid"
        FUNC_RETURN_VAL="Returned Value Type is Invalid"


        VAR_OPERAND_INVALID="Variable Operand Type is Invalid"
        VAL_OPERAND_INVALID="Value Operand Type is Invalid"

        FUNC_OPERAND_INVALID="Function Operand Type is Invalid"


        ZERO_DIV="Division by Zero"
        OUT_OF_BOUNDS="Out of Bounds"

        WRONG_NUM_VALUES="Wrong Number of Values"
        WRONG_NUM_DIMENSIONS="Wrong Number of Dimensions"

        WRONG_INDEX_TYPE="Wrong Type of Index"

        PARAM_REDECL_INSCOPE="Redeclaration of Parameter Identifier in Scope"
        PARAM_UNDECL_INSCOPE="Undeclared Parameter Identifier in Scope"

        EMPTY_BODY="Empty Body"
        EWAN="Placeholder Error"


        expected={

        "CONST_REDECL": "Different Identifer",
        "CONST_UNDECL": "Declared Constant",

        "VAR_UNDECL": "Declared Variable",
        "VAR_UNDEF": "Defined Variable",
        "VAR_REDECL_INSCOPE":  "Different Identifier",
        "VAR_SCOPE_INVALID": "Valid Scope",

        "SEQ_UNDECL": "Declared Sequence",

        
        "WRONG_NUM_ARGS": "{} Arguments in Function Call",
        "FUNC_UNDECL": "Declared Function",
        "FUNC_UNDEF":"Defined Function",
        "FUNC_REDECL_INSCOPE":  "Different Identifier",


        "VAR_ARG_INVALID":"Argument of Type {}",
        "VAL_ARG_INVALID":  "Argument of Type {}",

        "FUNC_RETURN_VAR":"Return Variable of Type {}",
        "FUNC_RETURN_VAL":"Return Value of Type {}",


        "VAR_OPERAND_INVALID": "Variable Operand of Type {}",
        "VAL_OPERAND_INVALID":"Operand of Type {}",

        "FUNC_OPERAND_INVALID": "Function Operand of Type {}",


        "ZERO_DIV": "Value other than Zero",
        "OUT_OF_BOUNDS": "Variable in Bound",

        "WRONG_NUM_VALUES": "{} Values in Sequence",
        "WRONG_NUM_DIMENSIONS": "{} Dimensions in Sequence",

        "WRONG_INDEX_TYPE": "Index of Type whole",

        "PARAM_REDECL_INSCOPE": "Different Parameter Identifier",
        "PARAM_UNDECL_INSCOPE": "Declared Parameter in Scope {}",

        "EMPTY_BODY":"Meat in Body",
        }