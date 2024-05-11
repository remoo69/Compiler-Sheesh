import sys
sys.path.append(".")
from source.CodeGeneration.Functionality.Functionality import Functionality
from source.core.error_types import Semantic_Errors as se


class Evaluators:
    def __init__(self, functionality:Functionality) -> None:
        self.codegen=functionality.codegen
        self.debug=functionality.debug


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

        print(operand_stack[0]) if self.debug else None
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


    def evaluate_condition(self, condition):
        evaluate=""
        for cond in condition:
            if cond.type=="Identifier":
                evaluate+=str(self.get_value(cond, self.id_dict).numerical_value)
            elif cond.type in ["kung", "ehkung"]:
                break
            elif cond.type in ["whole", "dec", ]:
                evaluate+=cond.numerical_value
            else:     
                evaluate+=cond.value

        
        output= eval(evaluate)
        return output