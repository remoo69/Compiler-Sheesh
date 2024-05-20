
import re
import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
import source.core.constants as const
from source.core.AST import AST
from source.core.symbol_table import SymbolTable
from source.core.error_handler import RuntimeError
from source.core.error_types import Semantic_Errors as se


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
            matched=self.leaves

            vars=[]
            vars2=[]
            text=''
            val=[]
            type=None

            for match in reversed(matched):
                if match.type=="Identifier":
                    vars.append(self.codegen.current_scope.find_var(match.value, self.current_scope))
                    vars2.append(match)
                    type=match.dtype
                    print(type)
                elif match.type in const.literal_types and match.type!="Text":
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
                        RuntimeError(error=err_msg, token=self.node.children[0], expected=expected)
                        )
                elif len(vars)>len(format_specifiers):
                    expected=f"{len(vars)} format specifiers of type"
                    for var in vars:
                        if var.type=="Identifier":
                            expected+=f" {var.dtype},"
                        else:
                            expected+=f" {var.type},"
                    self.runtime_errors.append(
                        RuntimeError(error=err_msg, token=self.node.children[0], expected=expected)
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
                              RuntimeError(error=se.VAR_UNDEF, token=vars2[i], expected=se.expected["VAR_UNDEF"])
                         )
                         return
                    # print(type(var))
                    # if isinstance(var, const.types[type]):
                    #      print("yeah")
                    # if type(var)==str and str(var).isdigit():
                    #      raise NotImplementedError

                    if vars[i].type in ["whole", "dec"] and ((var >1 or var<-1) and var%1==0):
                            var=const.format_spec[format_specifier](var)
                    val.append(var)
                    # Check if the variable has the correct type
                    if not isinstance(var, const.format_spec[format_specifier]):
                        
                        err_msg=f"Variable {vars[i].value} does not match format specifier {format_specifier}"
                        expected=f"{self.own_specifiers[format_specifier]} for format specifier ${format_specifier}"
                        self.runtime_errors.append(
                    RuntimeError(error=err_msg, token=self.current_node.children[0], expected=expected)
                    )
                        # raise TypeError(f"Variable {var} does not match format specifier {format_specifier}")

                # Replace the format specifiers with {} for string formatting
                for format_specifier in format_specifiers:
                    text = text.replace(format_specifier, "{}")

                # Format the string with the variables
                formatted_text = text.format(*val)

                occurrence=0
                # Print the formatted string
                if formatted_text in self.output_stream.keys():
                    self.output_stream[formatted_text]+=1
                else:
                    occurence=1
                    self.output_stream[formatted_text]=occurence
                print(self.output_stream)