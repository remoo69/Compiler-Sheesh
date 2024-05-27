import sys
sys.path.append( '.' )
# from source.core.symbol_table import Token
from source.core.error_handler import SemanticError as SemError
from source.core.error_types import Semantic_Errors as se
from source.core.AST import AST
import source.core.constants as const
from source.core.symbol_table import SymbolTable
# from copy import deepcopy


class Context:
    def __init__(self, name, parent) -> None:
        self.name=name
        self.parent=parent
        self.symbol_table:SymbolTable=SymbolTable()
        self.runtime_errors=[]
        self.output_stream={}
        if parent != None:
            self.symbol_table.symbols.update(self.parent.symbol_table)
            # self.runtime_errors.extend(self.parent.runtime_errors)
            
            # self.output_stream.update(self.parent.output_stream)
  
    def __repr__(self) -> str:
        return f"Context({self.name})"
    
    def symbols(self):
        self.symbol_table=SymbolTable()
        self.symbol_table.extend(self.parent.symbol_table)
        return self.symbol_table

class SemanticAnalyzer:
    """  
    TASKS:
        1. Arr element sizes
        2. Fix Scoping
        3. Func Argument size
        4. func argument type
        5. func call in expr return
    
    The semantic analyzer traverses the parse tree.
    The semantic analyzer will check the AST for any semantic errors.
    The SA must also assign identifiers to the symbol table.
    The SA will check:
        - Variable Declaration
        - Variable Use
        - Function Declaration
        - Function Use
        - Function Return Type
        - Function Arguments
        - Function Calls
        - Variable Assignment
        - Sequence Size
        - Sequence Access
        - Sequence Assignment


    Things to check:
        - Identifiers
        - Parameters/ Arguments
        - Return Types
        - Sequence Size
        - Sequence Access
        - Sequence Assignment/ Init


    BASTA TRABAHO NG SEMANTIC ANALYZER AY MAGINITIALIZE NG IDENTIFIERS SA SYMBOL TABLE.
    SA CODE GEN NA YUNG MGA ASSIGNMENTS, ETC. TANDAAN MO YAN ROMEO PATENO.


    ANG RUNTIME ERROR SUBSET NG SEMANTIC ERRORS. 

    

    #TODO - Function Declaration
    #TODO - Function Use (Check Decl)
    #TODO - Function Return Type
    #TODO - Function Arguments
    #TODO - Function Calls
    #TODO - Variable Assignment (Check operands)
    #TODO - Sequence Size
    #TODO - Sequence Access
    #TODO - Sequence Assignment
    #TODO - Sequence Declaration

    """


    
    def __init__(self, parse_tree:AST, debugMode=False) -> None:

        self.debug=debugMode

        self.parse_tree:AST=parse_tree
        # self.context.symbol_table=SymbolTable()
        self.context=None
        self.all_contexts={
        }
        
        
        self.semantic_expected=[]

        self.semantic_errors: list[SemError]=[]


        self.block_counter=1

        #for declarations
        self.req_type=None
    
        self.arr1=None
        self.arr2=None
        

        self.current_node:AST=self.parse_tree
        self.previous_node:AST=None

        self.current_scope=const.GBL

        self.buffer=[]

        self.nearest_id=None

        self.in_arg=False

        self.reverse_types={v: k for k, v in const.types.items()}
        
        self.visited=[]
        self.passed_tokens=[]
        
        self.routines={

            "allowed_in_loop": self.allowed_in_loop,

            "var_or_seq_dec": self.var_or_seq_dec,

            "w_vardec_tail": self.vardec_tail,
            "d_vardec_tail": self.vardec_tail,
            "s_vardec_tail": self.vardec_tail,
            "t_vardec_tail": self.vardec_tail,
            "c_vardec_tail": self.c_vardec_tail,

            "more_whl_var": self.more_var,
            "more_dec_var": self.more_var,
            "more_sus_var": self.more_var,
            "more_txt_var": self.more_var,
            "more_chr_var": self.more_chr_var,

            "w_const_tail": self.const_tail,
            "d_const_tail": self.const_tail,
            "s_const_tail": self.const_tail,
            "t_const_tail": self.const_tail,
            # "c_const_tail": self.c_const_tail,

            "charr_value": self.charr_value, 
            "const_type": self.const_type, 
            "control_flow_statement": self.control_flow_statement,
        
            "id_as_val": self.id_as_val,
        
            "sheesh_declaration": self.sheesh_declaration,
            "math_op": self.math_op,
            "reg_body": self.reg_body,
            "assign_op": self.assign_op,
            "looping_statement": self.looping_statement,
            "func_def":self.func_def,
            "in_loop_body":self.body,
            "control_flow_statement":self.body,   #choose
            "loop_body_statement":self.body,   #choose
            
            
            }
    
    def all_symbols(self):
        
        all_symbs=SymbolTable()
        print (self.all_contexts.values())if self.debug else None
        for context in self.all_contexts.values():
            all_symbs.symbols.update(context.symbol_table.symbols)
            print(context.symbol_table.symbols)if self.debug else None
        return all_symbs
    
    def __repr__(self) -> str:
        return f"SemanticAnalyzer({self.parse_tree})"
    
    def add_context(self, name):
        pass
        if name==const.GBL:
            self.context=Context(name, self.context)
            self.all_contexts[self.context.name]=self.context
        else:
            pass
        # self.context.symbol_table=self.context.symbol_table
        
    def end_context(self):
        if self.context.name!=const.GBL:
            self.context=self.context.parent
        else:
            pass
        
    def traverse(self, node):
        """ 
        Traverse the tree in a depth-first manner

        """
        if node.children:
            for child in node.children:
                if isinstance(child, AST):  # Check if the child is an AST
                    self.visited.append(child.root)
                    return child
                else:
                    self.passed_tokens.append(child.value)
                    if self.passed_tokens[-1]=="}" and self.passed_tokens[-2]=="#":
                        self.end_context()
        # If the node has no children or no AST children, go up the tree to find the next sibling
        while node.parent:
            sibling_index = node.parent.children.index(node) + 1
            if sibling_index < len(node.parent.children):
                for sibling in node.parent.children[sibling_index:]:
                    if isinstance(sibling, AST):  # Check if the sibling is an AST
                        return sibling
                    elif sibling.value=="}" and node.parent.children[sibling_index-1].leaves()[-1].value=="#":
                        self.end_context()
            node = node.parent

    def analyze(self):
        print("Semantic Analysis...")
        self.add_context(const.GBL)
        while True:
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                self.current_node = self.traverse(self.current_node)
            if self.current_node is None:
                # self.code_gen.generate_code()
                print(self.context.symbol_table)
                break  # Exit the loop if the tree has been fully traversed


    def body(self):
        if self.current_node.root in ["in_loop_body"] :
            self.add_context(self.current_node.parent.children[0].value)
        else:
            if isinstance(self.current_node.children[0], AST):
                pass
            else:
                if self.current_node.children[0].value in ["kung", "choose"]:
                    self.add_context(self.current_node.children[0].value)

    def func_def(self):
        items=self.current_node.leaves()
        
        type=items[1].value
        if type=="charr":
            id=items[3].value
        else:
            id=items[2].value

        parameter=self.current_node.children[4].leaves()
        
        try:
            self.context.symbol_table.function(id=id, return_type=type, parameters=parameter, body=None)
        except ValueError as e:
            e=str(e)
            self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])

        params=[]
        
        self.add_context(F"FUNCTION {id}")
        
        for i, param in enumerate(parameter):
            if param.type in const.DATA_TYPES:
                param_type=param.type
                param_id=parameter[i+1].value
                params.append(param_id)
                try:
                    try:
                        if parameter[i+2].type=="[":
                            self.context.symbol_table.sequence(id=param_id, type=param_type, rows=const.rows, cols=const.cols)
                        else:
                            self.context.symbol_table.variable(id=param_id, type=param_type)
                    except IndexError:
                        self.context.symbol_table.variable(id=param_id, type=param_type)
                except ValueError as e:
                    e=str(e)
                    self.semantic_error(error=getattr(se, e), token=param, expected=se.expected[str(e)])
            elif param.type==")":
                break

        body=self.current_node.find_node("func_def_tail")
        
            


    def allowed_in_loop(self):
        try:
            items= self.current_node.leaves()
            if items[0].type=="Identifier":
                self.nearest_id=items[0]
                id_obj=items[0]
                id=id_obj.value

                if items[1].type=="[":
                    try:
                        self.context.symbol_table.find_seq(id)
                    except ValueError as e:
                        e=str(e)
                        self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])
                elif items[1].type=="(":
                    try:
                        self.context.symbol_table.find_func(id)
                    except ValueError as e:
                        e=str(e)
                        self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])
                elif items[1].type in const.asop:
                    try:
                        var=self.context.symbol_table.find_var(id,)
                        self.req_type=var.type
                    except ValueError as e:
                        e=str(e)
                        self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])
                    try:
                        in_pamine=False
                        for item in items:
                            
                            if item.type=="#":
                                break
                            elif item.type=="pa_mine":
                                in_pamine=True
                            elif item.type=="Text" and in_pamine:
                                pass
                            elif item.type==")" and  in_pamine:
                                in_pamine=False
                            elif item.type in ["Whole", "Dec", "Sus", "Text", "Charr"] and not in_pamine:
                                if str(item.type).lower()!=str(self.req_type).lower():
                                    self.semantic_error(se.VAR_OPERAND_INVALID, item, f"Variable of Type {self.req_type}, Got {item.type}")
                    except AttributeError:
                        raise AttributeError("IDK what happened here")
                        return


                
                else: raise NameError("Bro What")

            else: pass

        except AttributeError as e:
            e=str(e)
            self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])

    def var_or_seq_dec(self):
            items=self.current_node.leaves()
            self.req_type=items[0].value
            try:
                if len(self.current_node.children)>3 and self.current_node.children[0].value!="charr":
                    try:
                        if len(self.current_node.children[2].children)>1 or self.current_node.children[2].children[0].root=="index":
                            if self.current_node.children[2].children[0].root=="index":
                                # ind=self.current_node.children[2].children[0].leaves()
                                rows=self.current_node.children[2].children[0].leaves()
                                try:
                                    rows=self.current_node.children[2].children[0].leaves()[1].numerical_value
                                    if isinstance(self.current_node.children[2].children[0].children[1], AST):
                                        cols=self.current_node.children[2].children[0].children[1].children[0].numerical_value
                                    else:
                                        cols=0
                                except AttributeError:
                                    rows=21
                                    try:
                                        if isinstance(self.current_node.children[2].children[1].children[0], AST):
                                            cols=21
                                        else:
                                            cols=0
                                    except IndexError:
                                        pass
                                        
                                self.context.symbol_table.sequence(id=items[1].value, type=self.req_type, rows=rows, cols=cols)
                            else:
                                return
                        else:
                            self.context.symbol_table.variable(id=items[1].value, type=self.req_type) 
                    except AttributeError:
                        self.context.symbol_table.variable(id=items[2].value, type=self.req_type, )
                elif self.current_node.children[0].value=="charr":
                    self.context.symbol_table.variable(id=items[2].value, type=self.req_type)
                else:
                    self.context.symbol_table.variable(id=items[1].value, type=self.req_type, )
                    # return

            except KeyError as e:
                e=str(e)[1:-1]
                print(e) if self.debug else None
                self.semantic_error(error=getattr(se, e), token=items[1], expected=se.expected[e])
            
    def looping_statement(self):
        try:
            if self.current_node.children[0].value=="for":
                self.req_type=self.current_node.children[2].value
                self.context.symbol_table.variable(id=self.current_node.children[3].value, type=self.req_type, )
        except KeyError as e:
            e=str(e)[1:-1]
            self.semantic_error(error=getattr(se, e), token=self.current_node.children[3], expected=se.expected[e])


    
    def vardec_tail(self):
    #TODO Find a way to reset reqtype
        try:
            id=self.current_node.parent.parent.children[1].value
            id_obj=self.current_node.parent.parent.children[1]
            # id=self.current_node.parent.children[1].value
        except AttributeError:
            id=self.current_node.parent.children[1].value
            id_obj=self.current_node.parent.children[1]

        except IndexError:
            return
        
  
        try:
            if self.current_node.children[0].root=="one_dim":
                self.context.symbol_table.sequence(id=id, type=self.req_type)

            else:
                # self.context.symbol_table.variable(id=id, type=self.req_type, scope=self.current_scope)
                return

        except KeyError as e:
            e=str(e)[1:-1]
            self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])


    def more_var(self):
        try:
            id=self.current_node.children[1].value
            self.context.symbol_table.variable(id=id, type=self.req_type, )

        except KeyError as e:
            e=str(e)
            self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])


    def c_vardec_tail(self):
    #TODO Find a way to reset reqtype
        try:
            id=self.current_node.parent.children[2].value
            id_obj=self.current_node.parent.children[2]

        except AttributeError:
            id=self.current_node.children[1].value

        try:
            # self.context.symbol_table.variable(id=id, type=self.req_type, )
            pass #NOTE - eyo
        except KeyError as e:
            e=str(e)[1:-1]
            self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])
            

    def more_chr_var(self):
        try:
            id=self.current_node.children[1].value
            self.context.symbol_table.variable(id=id, type=self.req_type, )

        except KeyError as e:
            e=str(e)
            self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])

    def charr_value(self):
        if self.current_node.children[0].type=="Identifier":
            self.nearest_id=self.current_node.children[0].value #NOTE - binago

            if len(self.current_node.children)>1:
                self.context.symbol_table.find_func(self.nearest_id)
            else:
                self.context.symbol_table.find_var(self.nearest_id, )


    def const_type(self):
        if self.current_node.children[1].type=="Identifier":
            self.req_type=self.current_node.children[0].value

    def const_tail(self):
        try:
            id=self.current_node.parent.children[1].value

        except AttributeError:
            id=self.current_node.children[1].value
  
        if self.current_node.children[0].root=="one_dim":
            self.context.symbol_table.sequence(id=id, type=self.req_type)

        else:
            self.context.symbol_table.variable(id=id, type=self.req_type)
    



    def control_flow_statement(self):
        # try:
        leaves=self.current_node.leaves()
        if leaves[2].type=="Identifier" and leaves[0].value=="choose":
            var=self.context.symbol_table.find_var(leaves[2].value, )
            if var.value==None:
                self.semantic_error(se.VAR_UNDEF, var, se.expected[se.VAR_UNDEF])
            if var.type!=const.WHOLE:
                self.semantic_error(se.WRONG_INDEX_TYPE, var, se.expected[se.WRONG_INDEX_TYPE].format(const.WHOLE))
            if var.scope !=self.current_scope:
                self.semantic_error(se.VAR_SCOPE_INVALID, var, se.expected[se.VAR_SCOPE_INVALID].format(self.context.name))
    

    def id_as_val(self):
        items= self.current_node.leaves()
        if items[0].type=="Identifier":
            self.nearest_id=items[0]
            id_obj=items[0]
            id=id_obj.value
            try:
                if len(items)>1:
                    try:
                        if items[1].type=="[":
                            self.context.symbol_table.find(id)
                        elif items[1].type=="(":
                            self.context.symbol_table.find_func(id)
                    except KeyError as e:
                        e=str(e)[1:-1]
                        self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[e])
                        

                else: 
                    try:
                        var=self.context.symbol_table.find(id) #NOTE - changed
                    except KeyError as e:
                        e=str(e)[1:-1]
                        self.semantic_error(error=e, token=id_obj, expected=se.expected[e])
                    # if var==None:
                    #     self.semantic_error(se.VAR_UNDEF, id_obj, se.expected["VAR_UNDEF"])
            except AttributeError as e:
                e=str(e)
                self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])

        else: pass


            
      


    def sheesh_declaration(self):
        if self.current_node.children[0].type=="sheesh":
            self.add_context("FUNCTION sheesh")

    def assign_op(self):
        # assign_ops={
        #     "=": self.create.assign,
        #     "+=": self.create.assign,
        #     "-=": self.create.assign,
        #     "*=": self.create.assign,
        #     "/=": self.create.assign,
        #     "%=": self.create.assign,
        # }

        # self.create.explore(assign_ops)
        
        # try:
        #     assign_ops[self.current_node.children[0].root]()
        # except AttributeError:
        #     if self.current_node.children[0].value=="/=":
        #         operand=self.check.next_operand()
        #         if (operand.numerical_value<1 and operand.numerical_value >-1) and operand.numerical_value %1 == 0:

        #             self.semantic_error(se.ZERO_DIV, operand, "Non-zero value")
        #         else:
        #             assign_ops[self.current_node.children[0].value]()
        #     else:
        #         assign_ops[self.current_node.children[0].value]()
        pass


    def math_op(self):
        # if self.current_node.children[0].type=="/":
        #     if self.current_node.parent.children[1].leaves()[0].type=="Identifier":
        #         id=self.current_node.parent.children[1].leaves()[0]
        #         try:
        #             operand=self.context.symbol_table.find(self.current_node.parent.children[1].leaves()[0].value)
        #             if operand.value != None:
        #                 if (operand.value<1 and operand.value >-1) and operand.value%1 == 0:
        #                     self.semantic_error(se.ZERO_DIV, operand, "Non-zero value")
                            
        #         except KeyError as e:
        #             e=str(e)[1:-1]
        #             self.semantic_error(error=e, token=id, expected=se.expected[e])
            pass
            

    def reg_body(self):
        if self.current_node.parent.root in ["func_def_tail", "sheesh_declaration"]:
            # self.add_context(f"{self.current_node.parent.parent.children[2].value} {self.block_counter}")
            pass
        else:
            self.add_context(f"{self.current_node.parent.children[0].value} {self.block_counter}")
        if len(self.current_node.children)<=2:
            
            self.block_counter+=1
            self.semantic_error(se.EMPTY_BODY, self.current_node.children[0], "Non-empty body")


    def semantic_error(self, error, token, expected):
        self.semantic_expected.append(expected)
        self.semantic_errors.append(SemError(error=error, line=token.line, toknum=token.position, value=token.value, expected=expected))
        
    def reset_arr(self):
        self.arr1=None
        self.arr2=None

