import re
import sys

sys.path.append('.')
from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_handler import RuntimeError
from source.core.error_types import Semantic_Errors as se
 


debug=True

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
    
class CodeGenerator:
    def __init__(self, semantic:SemanticAnalyzer) -> None:

        self.semantic=semantic
        self.output_stream={

        }
        self.id_list=self.semantic.parse_tree.symbol_table

        self.id_dict=self.semantic.parse_tree.symbol_table.accessible_ids()
        self.matched=self.semantic.parse_tree.leaves()

        self.current_node = self.semantic.parse_tree

        self.runtime_errors = []

        self.previous_node = None
        self.types={
            "whole":int,
            "decimal":float,
            "text":str,
            "sus":bool,
            "charr":charr
        }
        self.literal_types={
            "Whole":int,
            "Decimal":float,
            "Text":str,
            "Sus":bool,
            "Charr":charr
        }

        self.format_spec={
            "w":int,
            "d":float,
            "t":str,
            "s":bool,
            "c":charr
        }

        self.own_specifiers={
            "w":"whole",
            "d":"dec",
            "t":"text",
            "s":"sus",
            "c":"charr"


        }

        self.routines={
            "allowed_in_loop":self.allowed_in_loop,
            "pa_mine":self.pa_mine,
            "var_or_seq_dec":self.var_or_seq_dec,
            "looping_statement":self.looping_statement,
            "loop_body_statement":self.loop_body_statement,
            "in_loop_body":self.in_loop_body,
            "loop_body":self.loop_body,
            "more_loop_body":self.more_loop_body,
            "control_flow_statement":self.control_flow_statement,

        }

        self.functionality={

            "yeet":self.yeet,
            "def":self.def_,
            "based":self.based,
            "up":self.up,
            "pa_mine":self.pa_mine,
            
            
            "kung":self.kung,
            
            "pass":self.pass_,
            "kung":self.kung,
            "ehkung":self.ehkung,
            "deins":self.deins,
            "choose":self.choose,
            "when":self.when,
            "default":self.default,
            
            "bet":self.bet,
            "whilst":self.whilst,
            "for":self.for_loop,
            # "to":self.to_loop,
            "felloff":self.felloff,
            # "step":self.step,
            "pass":self.pass_,




        }


    def generate_code(self):
        print("Generating code...")
        while True:
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            if self.current_node is None:
                break  # Exit the loop if the tree has been fully traversed

    def get_value(self, id, id_dict):
        if id.value in id_dict.keys():
            return id_dict[id.value]
        else:
            raise Exception("Variable not found")
    

    def loop_body_statement(self):

        # try:
        #     self.functionality[self.current_node.root]()
        #     self.previous_node=self.current_node
        #     self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        # except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines[self.current_node.root]()
            try:
                if self.previous_node.parent.children[-1].root=="more_loop_body":
                    self.previous=self.current_node
                    self.current_node=self.previous_node.parent.children[-1]
                    self.routines["more_loop_body"]()
            except AttributeError:
                pass
            

    def looping_statement(self):
        if self.current_node.children[0].value=="for":
            self.functionality["for"]()

        elif self.current_node.children[0].value=="bet":
            self.functionality["bet"]()

    def var_or_seq_dec(self):
        # try:
            if self.current_node.children[-1].value=="#":
                pass
                # self.eval_arithm()
    def more_loop_body(self):
        try:
            if self.current_node.children[0].root in  self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
                self.routines[self.current_node.children[0].root]()
            else:
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            print("nag key error par")
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body_statement"]()

    def allowed_in_loop(self):

        try:
            if self.current_node.children[0].value in self.functionality.keys():
                self.functionality[self.current_node.children[0].value]()
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            elif self.current_node.children[0].type=="Identifier":

                self.assign(self.current_node.children[0])

            else:
                # raise Exception("Routine not found")
                print(f'Functionality {self.current_node.children[0].value} not found')
                pass
        except AttributeError as e:
            # print(e)
            # print(f"No Functionality for {self.current_node.children[0].root} in {self.current_node.root}")
            
            pass

    def in_loop_body(self):
        try:
            self.functionality[self.current_node.root]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body"]()
            

    def loop_body(self):
        try:
            self.functionality[self.current_node.root]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body_statement"]()  
            
    def control_flow_statement(self):
        if self.current_node.children[0].value in ["choose", "kung"]:
            self.functionality[self.current_node.children[0].value]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)

#region Functionality
#SECTION - FUNCTIONALITY


    def for_loop(self):
        
        children=self.current_node.children

        iterator=None
        end=None
        step=1
        loop_body=self.current_node.children[-1].children[1]

        if children[3].type=="Identifier":
            iterator=children[3]

        if children[7].root=="whl_value":
            end=children[7].leaves()[0]
            print(end)

        try:
            if children[8].root=="step_statement":
                step=children[8].leaves()[1]
                print(step)
        except AttributeError as e:
            print(e)
            print("No step statement")

        
        while iterator.numerical_value != end.numerical_value:
            self.current_node = self.semantic.parse_tree.traverse(loop_body)
            # self.previous_node=self.current_node
            self.routines[self.current_node.root]()
        
            # self.routines["in_loop_body"]()
            iterator.numerical_value+=step
            print("Iterator: ", iterator.numerical_value, "End: ", end.numerical_value, "Step: ", step)

        if debug:
            print(f"For Loop: \n\tIterator: {iterator}\n\t End: {end}\n\t Step: {step}")
        
    def kung(self):

        condition=self.current_node.children[2].leaves()
        reg_body=self.current_node.children[4]
        # cond_tail=


    def yeet(self):
        raise NotImplementedError
    
    def based(self):
        raise NotImplementedError
    
    def def_(self):
        raise NotImplementedError
    
    def ehkung(self):
        raise NotImplementedError
    
    def deins(self):
        raise NotImplementedError
    
    def when(self):
        raise NotImplementedError
    
    def default(self):
        raise NotImplementedError
    
    def whilst(self):
        raise NotImplementedError

    def bet(self):
        raise NotImplementedError

    def choose(self):
        raise NotImplementedError
    
    def felloff(self):
        raise NotImplementedError
    
    def pass_(self):
        raise NotImplementedError

    def up(self):
        matched=self.current_node.leaves()
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
            elif match.type in self.literal_types and match.type!="Text":
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
            for i in range(len(format_specifiers)):
                # Get the format specifier (remove the dollar sign)
                format_specifier = format_specifiers[i][1:]
                # Get the corresponding variable
                var = vars[i].numerical_value
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


    def assign(self, id):
        assign_ops=["=", "+=", "-=", "*=", "/=", "%="]
        op=None
        for index, vals in enumerate(self.current_node.leaves()):
            if vals.type in assign_ops:
                op=self.current_node.leaves()[index].value
                break
        
        expr=[]
        value=None
        if id.value in self.semantic.id.accessible_ids().keys():
            items=self.current_node.parent.leaves()
            temp=self.current_node.parent.values()
            
            eq_index=temp.index(op)
            for children in items[eq_index+1:]:
                # try:
                    if children.type not in ["#", ",", "Newline", "whole", "dec", "sus", "text", "charr", "for" ]:
                        if children.type=="Identifier":
                                expr.append(self.semantic.id.accessible_ids()[children.value])
                        elif children.type=="to":
                            break
                        else: expr.append(children)
                    
                # except AttributeError:
                #     raise AttributeError("No Identifier Found")
            
        
            value=self.eval_arithm(expr)

            id_ref=self.semantic.id.accessible_ids()[id.value]
            if id_ref.numerical_value==None:
                id_ref.numerical_value=0
            if op != "=":
                if op=="+=":
                    value+=id_ref.numerical_value
                elif op=="-=":
                    value-=id_ref.numerical_value
                elif op=="*=":
                    value*=id_ref.numerical_value
                elif op=="/=":
                    value/=id_ref.numerical_value
                elif op=="%=":
                    value%=id_ref.numerical_value
    
            
            if value != None:
                if type(value)==self.semantic.data_types[id.dtype]:
                    self.semantic.id.accessible_ids()[id.value].numerical_value=value
                    return True
                else:
                
                    if value%1==0:
                        value=self.semantic.data_types[id.dtype](value)
                        self.semantic.id.accessible_ids()[id.value].numerical_value=value
                        return True
                    else:
                        # self.semantic.semantic_error(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}")
                        self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}"))
            else:
                # self.semantic.semantic_error(se.VAR_UNDEF, id, "Value pare")
                self.runtime_errors.append(RuntimeError(se.VAR_UNDEF, id, "Value pare"))

    def evaluate(self, eval:list):
        precedence = {'+':1, '-':1, '*':2, '/':2, '%':2}
        operator_stack = []
        operand_stack = []

        for token in reversed(eval):
            if token.type == "Identifier":
                operand_stack.append(token.numerical_value)
            elif token.type not in ['+', '-', '*', '/', '^', '(', ')', "=", "%", "Newline"]:
                try:
                    operand_stack.append(float(token.numerical_value))
                except ValueError:
                    operand_stack.append(float(token.numerical_value[1:-1]))
            elif token.type == '(':
                operator_stack.append(token)
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

        print(operand_stack[0]) if debug else None
        return operand_stack[0]
    
    def eval_arithm(self, expr):

        eval=[]
        for match in reversed(expr):
            if match.type in ["#", "Newline"]:
                pass
            else:
                eval.append(match)

        return self.evaluate(eval)
    
    def eval_logic(self, expr):
        eval=[]
        for match in reversed(expr):
            if match.type in ["#", "Newline"]:
                pass
            else:
                eval.append(match)
        return self.evaluate_logic(eval)
    
    def evaluate_logic(self, eval):
        precedence = {'&':1, '|':1, '!':2}
        operator_stack = []
        operand_stack = []

        for token in reversed(eval):
            if token.type == "Identifier":
                operand_stack.append(token.numerical_value)
            elif token.type not in ['&', '|', '!', '(', ')', "=", "Newline"]:
                try:
                    operand_stack.append(float(token.numerical_value))
                except ValueError:
                    operand_stack.append(float(token.numerical_value[1:-1]))
            elif token.type == '(':
                operator_stack.append(token)
            elif token.type == ')':
                while operator_stack[-1].type != '(':
                    operator = operator_stack.pop().value
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    if operator == '&':
                        result = operand1 and operand2
                    elif operator == '|':
                        result = operand1 or operand2
                    operand_stack.append(result)
                operator_stack.pop()

    def evaluate_relational(self, eval):
        precedence = {'<':1, '>':1, '<=':1, '>=':1, '==':2, '!=':2}
        operator_stack = []
        operand_stack = []

        for token in reversed(eval):
            if token.type == "Identifier":
                operand_stack.append(token.numerical_value)
            elif token.type not in ['<', '>', '<=', '>=', '==', '!=', '(', ')', "=", "Newline"]:
                try:
                    operand_stack.append(float(token.numerical_value))
                except ValueError:
                    operand_stack.append(float(token.numerical_value[1:-1]))
            elif token.type == '(':
                operator_stack.append(token)
            elif token.type == ')':
                while operator_stack[-1].type != '(':
                    operator = operator_stack.pop().value
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    if operator == '<':
                        result = operand1 < operand2
                    elif operator == '>':
                        result = operand1 > operand2
                    elif operator == '<=':
                        result = operand1 <= operand2
                    elif operator == '>=':
                        result = operand1 >= operand2
                    elif operator == '==':
                        result = operand1 == operand2
                    elif operator == '!=':
                        result = operand1 != operand2
                    operand_stack.append(result)
                operator_stack.pop()
    def pa_mine(self):
        raise NotImplementedError