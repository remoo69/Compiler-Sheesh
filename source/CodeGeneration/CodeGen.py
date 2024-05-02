import re
import sys
from tkinter import StringVar, Text
sys.path.append('.')
# from source.SyntaxAnalyzer.parser2 import SyntaxAnalyzer
from Lexer import Lexer 
import llvmlite as ir

class charr:
    def __init__(self, value):
        self.value=value
        self.type="char"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __add__(self, other):
        return charr(self.value+other.value)

    def __sub__(self, other):
        return charr(self.value-other.value)

    def __mul__(self, other):
        return charr(self.value*other.value)

    def __truediv__(self, other):
        return charr(self.value/other.value)

    def __mod__(self, other):
        return charr(self.value%other.value)

    def __eq__(self, other):
        return self.value==other.value

    def __ne__(self, other):
        return self.value!=other.value

    def __lt__(self, other):
        return self.value<other.value

    def __le__(self, other):
        return self.value<=other.value

    def __gt__(self, other):
        return self.value>other.value

    def __ge__(self, other):
        return self.value>=other.value

    def __and__(self, other):
        return self.value and other.value

    def __or__(self, other):
        return self.value or other.value

    def __xor__(self, other):
        return self.value ^ other.value

    def __lshift__(self, other):
        return self.value << other.value

    def __rshift__(self, other):
        return self.value >> other.value

    def __invert__(self):
        return ~self.value

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __round__(self, n):
        return round(self.value, n)

    def __floor__(self):
        return self.value.floor()

    def __ceil__(self):
        return self.value.ceil()

    def __trunc__(self):
        return self.value.trunc()

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return len(self.value)
    
class CodeGeneration:

    def __init__(self, syntax_analyzer):
        self.syntax=syntax_analyzer
        self.types={
            "whole":int,
            "decimal":float,
            "text":str,
            "suspect":bool,
            "char":charr
        }
        self.format_spec={
            "w":int,
            "d":float,
            "t":str,
            "s":bool,
            "c":charr
        }

    def eval_arithm(self, matched, id_list):
        eval=[]
        for match in reversed(matched):
            if match.type=="=":
                return self.evaluate(eval)
            elif match.type=="Identifier":
                eval.append(self.get_value(match, id_list))
            elif match.type in ["#", "Newline"]:
                pass
            else:
                eval.append(match)

    def get_value(self, id, id_list):
        for var in id_list:
            if var.value==id.value:
                return var
        else:
            raise Exception("Variable not found")
    

    def ID_assign(self, matched_list, id_list, value):
        found_equals = False
        id=None
        for token in reversed(matched_list):
            if token.type == "=":
                found_equals = True
            elif found_equals and token.type == "Identifier":
                id = token
                break
        
        for var in id_list:
            if var.value==id.value:
                var.numerical_value=value
                return var
        else:
            raise Exception("Variable not found")

    def evaluate(self, eval:list):
        precedence = {'+':1, '-':1, '*':2, '/':2, '%':2}
        operator_stack = []
        operand_stack = []

        for token in reversed(eval):
            if token.type == "Identifier":
                operand_stack.append(token.numerical_value)
            elif token.type not in ['+', '-', '*', '/', '^', '(', ')', "=", "%", "Newline"]:
                operand_stack.append(int(token.value))
            elif token.type == '(':
                operator_stack.append(token.value)
            elif token.type == ')':
                while operator_stack[-1].type != '(':
                    operator = operator_stack.pop().value
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    if operator == '+':
                        result = operand1 + operand2
                    elif operator == '-':
                        result = operand1 - operand2
                    elif operator == '*':
                        result = operand1 * operand2
                    elif operator == '/':
                        result = operand1 / operand2
                    elif operator=='%':
                        result = operand1 % operand2
                    operand_stack.append(result)
                operator_stack.pop()  # Remove the '(' from the stack
            else:
                while (operator_stack and operator_stack[-1].type != '(' and 
                    precedence[operator_stack[-1].type] >= precedence[token.type]):
                    operator = operator_stack.pop().value
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    if operator == '+':
                        result = operand1 + operand2
                    elif operator == '-':
                        result = operand1 - operand2
                    elif operator == '*':
                        result = operand1 * operand2
                    elif operator == '/':
                        result = operand1 / operand2
                    elif operator=='%':
                        result = operand1 % operand2
                    operand_stack.append(result)
                operator_stack.append(token)

        while operator_stack:
            operator = operator_stack.pop().value
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            if operator == '+':
                result = operand1 + operand2
            elif operator == '-':
                result = operand1 - operand2
            elif operator == '*':
                result = operand1 * operand2
            elif operator == '/':
                result = operand1 / operand2
            elif operator=='%':
                result = operand1 % operand2
            operand_stack.append(result)

        print(operand_stack[0])
        return operand_stack[0]



    def up(self, matched, output_stream, id_list):
        vars=[]
        text=''
        val=[]
        type=None
        for match in reversed(matched):
            if match.type=="Identifier":
                vars.append(self.get_value(match, id_list))
                type=match.dtype
                print(type)
            elif match.type in self.types:
                vars.append(self.types[match.type](match.value))
            elif match.type=="Text":
                text=match.value
                print(match.value)
            elif match.type=="(":
                break
 

        # Find all format specifiers in the text
        format_specifiers = re.findall(f"\$[{''.join(self.format_spec.keys())}]", text)
        # print(format_specifiers)
        # Check if the number of format specifiers matches the number of variables
        if len(format_specifiers) != len(vars):
            self.syntax.semantic_errors.append(f"Number of format specifiers does not match number of variables")
            
            # raise ValueError("Number of format specifiers does not match number of variables")

        # For each format specifier, check if the corresponding variable has the correct type
        for i in range(len(format_specifiers)):
            # Get the format specifier (remove the dollar sign)
            format_specifier = format_specifiers[i][1:]
            # Get the corresponding variable
            var = vars[i].numerical_value
            val.append(var)
            # Check if the variable has the correct type
            if not isinstance(var, self.format_spec[format_specifier]):
                self.syntax.semantic_errors.append(f"Variable {var} does not match format specifier {format_specifier}")
                # raise TypeError(f"Variable {var} does not match format specifier {format_specifier}")

        # Replace the format specifiers with {} for string formatting
        for format_specifier in format_specifiers:
            text = text.replace(format_specifier, "{}")

        # Format the string with the variables
        formatted_text = text.format(*val)

        # Print the formatted string
        output_stream.append(formatted_text)

    
    def pa_mine(self, matched, id_list,  terminal:StringVar):
        user_input = terminal.get()
        ev = CodeGeneration()
        result = ev.ID_assign(matched, id_list, user_input)
        print(result)
    
if __name__ == "__main__":
    # variables = {"a":1, "b":2, "c":3}
    code = "=1+2*(3%9)/3/4"
    # code,error=Lexer.tokenize(code)
    # print(code)
    ev=CodeGeneration()
    print(code)
    print(ev.eval_arithm(code))
    # cg=CodeGeneration(SyntaxAnalyzer(None))
    # cg.up("The speed of the fluid $t is: $w m/s ", 'hi',10, )