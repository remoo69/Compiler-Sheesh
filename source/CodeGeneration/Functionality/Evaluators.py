import sys
sys.path.append(".")
from source.core.error_types import Semantic_Errors as se
import source.core.constants as const
import source.core.symbol_table as st
from source.core.symbol_table import SymbolTable, Token 
from source.core.error_handler import RuntimeError as RError


"""  
THIS IS ONE OF THE MOST IMPORTANT CLASSES IN THE CODE GENERATOR. 
THIS CLASS IS RESPONSIBLE FOR EVALUATING EXPRESSIONS, CONDITIONS, AND OTHER TYPES OF VALUES.

"""


class Evaluators:
    """  
    This is a general helper class for evaluations. An evaluator can take either a value, variable, function call, or an expression.
    The evaluator will then evaluate the expression and return the result.
    The evaluator should be given an expression, and the symbol table. It then outputs the result of the expression.
    The expression should be a list of tokens.
    
    """
    def __init__(self, expression, runtime_errors, context) -> None:
        self.expression=expression
        self.runtime_errors=runtime_errors
        self.context=context
        # self.context.name=scope
        # self.context.symbol_table:st.SymbolTable=symbol_table

    def build_expression(self, expression):
        """  
        This method extracts all possible values from the expression. It then returns a list of the values.
        This method should evaluate funcs, sequences, and variables first before evaluating the expression.
        """
        final_expression=""
        eq_found=False
        for i, expr in enumerate(expression):
 
                if expr.type not in const.keywords:
                    if expr.type=="Identifier":
                        try:
                            var= self.context.symbol_table.find(expr.value)
                            if isinstance(var, st.Sequence): 
                                
                                index=self.evaluate(expression[i+2:], type=const.dtypes.whole)
                                col=self.evaluate(expression[i+3:], type=const.dtypes.whole) # FIXME can' eval col because can't find second index.
                                # sequence=self.context.symbol_table.find(var.value, self.context.name)
                                final_expression+=var.get(row=index, col=col)
                                
                            elif isinstance(var, st.Variable):
                                if var.type in ["whole", "dec",]:
                                    final_expression+=str(var.value)
                                elif var.type in ["sus", "text", "charr"]:
                                    final_expression+=var.value 
                                    #NOTE - idk what to do here. ito muna lagay ko
                            elif isinstance(var, st.Function):
                                
                                func=var
                                final_expression+=func 
                            elif isinstance(var, Token):
                                if var.type in ["Whole", "Dec"]:
                                    final_expression+=var.numerical_value
                                else:
                                    self.runtime_errors.append(RuntimeError(se.EWAN, expr, "Invalid Expression"))
                        except KeyError as e:
                            e=str(e)[1:-1]
                            self.codegen.context.runtime_errors.append(RError(error=getattr(se, e), token=expr, expected=se.expected[e]))

                    elif expr.type in ["Whole", "Dec", ]:
                        final_expression+=expr.value
                    elif expr.type in ["Text", "Charr"]:
                        final_expression+=expr.value
                    elif expr.type in ["Sus"]:
                        if expr.value =="nocap":
                            final_expression+="True"
                        else:
                            final_expression+="False"
                    elif expr.type in const.aop:
                        final_expression+=expr.value
                    elif expr.type in ["#", "]"]:
                        break
                    else:
                        final_expression+=expr.value
                else:
                    pass
                
        return final_expression
    
    def evaluate(self, expr, type):
        expression=self.build_expression(expression=expr)
        return const.py_types[type]( self.general_evaluator(expression))
        
    # def evaluate(self, expr):
    #     new_expr=self.build_expression()
    #     if not any(op in new_expr for op in const.all_op):
    #         return new_expr
    #     else:
    #         return eval(new_expr)


    
    def general_evaluator(self, expr:str):
        """ TRIES to evaluate expressions using python's eval() """
        if expr!=None and expr!="":
            if not any(op in expr for op in const.all_op):
                return expr
            else:
                return eval(expr)
        else:
            return None
    
    def assign(self, id):
        """  
        This function should take the name of the id, and the symbol table. It should then assign the value to the id.

        """
        assign_ops=["=", "+=", "-=", "*=", "/=", "%="]
        op=None
        for index, vals in enumerate(self.expression):
            if vals.type in assign_ops:
                op=self.expression[index].type
                break
        
        value=None
        if id.value in self.context.symbol_table.keys():
            items=self.expression
            try:
                var=self.context.symbol_table.find(id.value, self.context.name)
                #FIXME - no type checking for var

                if var.type in ["dec", "whole"]:
                    temp=self.build_expression(self.expression)
                else:
                    temp=self.build_condition()
                
            
                value=self.general_evaluator(temp)

                id_ref=self.context.symbol_table.find_var(id.value, self.context.name)
                if id_ref.value==None:
                    id_ref.value=0 #NOTE -  medj sus; idk if oks lang bang ganto default
                if op != "=":
                    if op=="+=":
                        value+=id_ref.value
                    elif op=="-=":
                        value-=id_ref.value
                    elif op=="*=":
                        value*=id_ref.value
                    elif op=="/=":
                        value/=id_ref.value
                    elif op=="%=":
                        value%=id_ref.value
        
                
                if value != None:
                    print(type(value))
                    print(const.types[id_ref.type])
                    if type(value)==const.py_types[id_ref.type]:
                        if id_ref.type in ["whole", "dec"]:
                            self.context.symbol_table[id.value].assign(op=op, value=const.py_types[id_ref.type](value)[1:-1])
                        else:
                            self.context.symbol_table[id.value].assign(op=op, value=value)
                        return True
                    
                    elif type(value)==str:
                        value=const.py_types[id_ref.type](value)
                        self.context.symbol_table[id.value].assign(op=op, value=value)
                        return True
                    else:
                        if value%1==0 or value>0 or value<0:
                            value=self.semantic.data_types[id.dtype](value)
                            self.context.symbol_table[id.value].assign(op=op, value=value)
                            return True
                        else:
                            # self.semantic.semantic_error(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}")
                            self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, id, f"Value of Type {id.dtype}, got {self.semantic.reverse_types[type(value)]}"))
                else:
                    # self.semantic.semantic_error(se.VAR_UNDEF, id, "Value pare")
                    self.runtime_errors.append(RuntimeError(error=se.VAR_UNDEF,token= id, expected="Value pare"))
            except KeyError as e:
                        e=str(e)[1:-1]
                        self.codegen.context.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
    
         
         
         
    

    def concat(self):
        """  
        Algorithm:
        1. Get Text Expression. 
        2. Temp=first_text
        3. While concat op, temp+=next_text
        """

    def evaluate_cond(self)->bool:
        new_expr=self.build_condition()
        if new_expr!=None and new_expr!="":
            if not any(op in new_expr for op in const.all_op):
                return new_expr
            else:
                return eval(new_expr)
        else:
            return None
    
    def arithm(self, expr):

        # eval=[]
        # for match in reversed(expr):
        #     if match.type in ["#", "Newline"]:
        #         pass
        #     else:
        #         eval.append(match)
        eval=self.build_expression()

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
    
    def logic(self, expr):
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

    def relational(self, eval):
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

    def condition(self, condition):
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
    
    @DeprecationWarning
    def build_condition(self):
        """  
        This method extracts all possible values from the expression. It then returns a list of the values.
        If there is a function, variable, sequence, or any other type of value, it should be evaluated first.

        """
        final_expression=""
        eq_found=False
        for expr in self.expression:
                
            # if eq_found:
            try:
                if expr.type not in const.keywords:
                    if expr.type=="Identifier":
                        var= self.context.symbol_table.find(expr.value, self.context.name)
                        if isinstance(var, st.Sequence):
                            #FIXME - Implement sequence indexing
                            raise NotImplementedError
                            index1=self.expression[self.expression.index(expr)+1]
                            final_expression+=var.index_getvalue(index1, index2)
                        elif isinstance(var, st.Variable):
                            if var.type in ["whole", "dec",]:
                                final_expression+=str(var.get_val())
                            elif var.type in ["sus", "text", "charr"]:
                                final_expression+=var.get_val()
                                #NOTE - idk what to do here. ito muna lagay ko
                        elif isinstance(var, st.Function):
                            final_expression+=var.execute() #NOTE - IMPLEMENT FUNC EXECUTION
                        elif isinstance(var, Token):
                            if var.type in ["Whole", "Dec"]:
                                final_expression+=var.numerical_value
                            else:
                                self.runtime_errors.append(RuntimeError(se.EWAN, expr, "Invalid Expression"))

                    elif expr.type in ["Whole", "Dec", ]:
                        final_expression+=expr.value
                    elif expr.type in ["Text", "Charr"]:
                        final_expression+=expr.value
                    elif expr.type in ["Sus"]:
                        if expr.value =="nocap":
                            final_expression+="True" 
                        else:
                            final_expression+="False"
                    elif expr.type in const.all_op:
                        final_expression+=expr.value
                    elif expr.type=="#":
                        break
                    else:
                        self.runtime_errors.append(RuntimeError(error=se.EWAN,token= expr, expected="Invalid Condition"))
                else:
                    pass
            
            except ValueError as e:
                e=str(e)
                self.runtime_errors.append(RuntimeError(error=getattr(se,e), token=expr, expected=se.expected[e]))
                return
            # else:
            #     if expr.type in const.asop or (expr.type in const.keywords and expr.type not in const.DATA_TYPES):
            #         eq_found=True
            #         pass
        return final_expression
            
    
    @DeprecationWarning
    def build_concat(self):
        final_expression=""
        eq_found=False
        for expr in self.expression:
                
            if eq_found:
                if expr.type not in const.keywords:
                    if expr.type=="Identifier":
                        var= self.context.symbol_table.find(expr.value, self.context.name)
                        if isinstance(var, st.Sequence):
                            #FIXME - Implement sequence indexing
                            raise NotImplementedError
                            index1=self.expression[self.expression.index(expr)+1]
                            final_expression+=var.index_getvalue(index1, index2)
                        elif isinstance(var, st.Variable):
                            if var.type in ["whole", "dec",]:
                                self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, expr, se.expected["VAR_OPERAND_INVALID"]))
                            elif var.type in ["sus"]:
                                self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, expr, se.expected["VAR_OPERAND_INVALID"]))
                            elif var.type in [ "text", "charr"]:
                                final_expression+=var.value
                                #NOTE - idk what to do here. ito muna lagay ko
                        elif isinstance(var, st.Function):
                            final_expression+=var.execute() #NOTE - IMPLEMENT FUNC EXECUTION
                        elif isinstance(var, Token):
                            if var.type in ["Whole", "Dec"]:
                                self.runtime_errors.append(RuntimeError(se.VAR_OPERAND_INVALID, expr, se.expected["VAR_OPERAND_INVALID"]))
                            else:
                                self.runtime_errors.append(RuntimeError(se.EWAN, expr, "Invalid Expression"))

                    elif expr.type in ["Text", "Charr"]:
                        final_expression+=expr.value
                   
                    elif expr.type in const.concat:
                        final_expression+="+"
                    elif expr.type=="#":
                        break
                    else:
                        self.runtime_errors.append(RuntimeError(se.EWAN, expr, "Invalid Condition"))
                else:
                    pass
            
            else:
                if expr.type in const.asop or (expr.type in const.keywords and expr.type not in const.DATA_TYPES):
                    eq_found=True
                    pass
        return final_expression

    def logic_rel(self):
        raise NotImplementedError

    def function_call(self):
        pass