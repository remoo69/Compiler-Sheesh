
import re
import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
import source.core.constants as const


class InOut:
    def __init__(self, functionality) -> None:
        # self.codegen=functionality.codegen
        # self.debug=functionality.debug
        pass


    def up(self):
            matched=self.codegen.current_node.leaves()
            id_dict=self.id_dict
            vars=[]
            text=''
            val=[]
            type=None

            for match in reversed(matched):
                if match.type=="Identifier":
                    vars.append(self.get_value(match, id_dict))
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
            format_specifiers = re.findall(f"\$[{''.join(self.format_spec.keys())}]", text)
            # print(format_specifiers)
            # Check if the number of format specifiers matches the number of variables
            if len(format_specifiers) != len(vars):
                err_msg="Number of format specifiers does not match number of variables"
                if len(vars)<len(format_specifiers):
                    expected=f"{len(format_specifiers)} variables of type"
                    for format in format_specifiers:
                            expected+=f" {self.own_specifiers[format[1:]]},"
                    self.runtime_errors.append(
                        RuntimeError(error=err_msg, token=self.current_node.children[0], expected=expected)
                        )
                elif len(vars)>len(format_specifiers):
                    expected=f"{len(vars)} format specifiers of type"
                    for var in vars:
                        if var.type=="Identifier":
                            expected+=f" {var.dtype},"
                        else:
                            expected+=f" {var.type},"
                    self.runtime_errors.append(
                        RuntimeError(error=err_msg, token=self.current_node.children[0], expected=expected)
                        )
            else:

            # For each format specifier, check if the corresponding variable has the correct type
                vars=list(reversed(vars))
                for i in range(len(format_specifiers)):
                    # Get the format specifier (remove the dollar sign)
                    format_specifier = format_specifiers[i][1:]
                    # Get the corresponding variable
                    var = vars[i].numerical_value
                    if (var >1 or var<-1) and var%1==0:
                            var=self.format_spec[format_specifier](var)
                    val.append(var)
                    # Check if the variable has the correct type
                    if not isinstance(var, self.format_spec[format_specifier]):
                        
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