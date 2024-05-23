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

            # "in_param": self.in_param,
            "allowed_in_loop": self.allowed_in_loop,

            "var_or_seq_dec": self.var_or_seq_dec,

            "w_vardec_tail": self.vardec_tail,
            "d_vardec_tail": self.vardec_tail,
            "s_vardec_tail": self.vardec_tail,
            "t_vardec_tail": self.vardec_tail,
            "c_vardec_tail": self.c_vardec_tail,
            # "w_seq_tail": self.w_seq_tail,

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
            # "more_whl_const": self.more_whl_const, 
            # "more_dec_const": self.more_dec_const, 
            # "more_sus_const": self.more_sus_const, 
            # "more_txt_const": self.more_txt_const,
            # "more_chr_const": self.more_chr_const,
            "control_flow_statement": self.control_flow_statement,
            # "looping_statement": self.looping_statement,
            # "loop_body_statement": self.loop_body_statement,
            # "func_def": self.func_def,
            "id_as_val": self.id_as_val,
            # "id_val_tail": self.id_val_tail,
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
        self.context=Context(name, self.context)
        self.all_contexts[self.context.name]=self.context
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
                    self.context.symbol_table.variable(id=param_id, type=param_type)
                except ValueError as e:
                    e=str(e)
                    self.semantic_error(error=getattr(se, e), token=param, expected=se.expected[str(e)])
            elif param.type==")":
                break

        body=self.current_node.find_node("func_def_tail")
        
            


    # def in_param(self):


    #     if self.current_node.children[1].type=="Identifier":
    #         id=self.current_node.children[1]
    #         type=self.current_node.children[0].children[0].value
    #         if self.current_node.children[2].type=="[":
    #             param_type=const.SEQ
    #         else:
    #             param_type=const.VAR
    #         try:
    #             self.context.symbol_table.parameter(id=id, type=type,param_type=param_type)
    #         except ValueError as e:
    #             e=str(e)
    #             self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])

    #     elif self.current_node.children[2].type=="Identifier":
    #         id=self.current_node.children[2]
    #         type="charr"
    #         param_type=const.VAR
    #         try:
    #             self.context.symbol_table.parameter(id=id, type=type, param_type=param_type)
    #         except ValueError as e:
    #             e=str(e)
    #             self.semantic_error(error=getattr(se, e), token=id, expected=se.expected[str(e)])

#FIXME - handle current scope
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
                        for item in items:
                            if item.type=="#":
                                break
                            if item.type in ["Whole", "Dec", "Sus", "Text", "Charr"]:
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
                                # rows=self.current_node.children[2].children[0].leaves()
                                try:
                                    rows=self.current_node.children[2].children[0].leaves()[1].numerical_value
                                    if isinstance(self.current_node.children[2].children[1].children[0], AST):
                                        cols=self.current_node.children[2].children[1].children[0].children[1].numerical_value
                                    else:
                                        cols=0
                                except AttributeError:
                                    rows=21
                                    if isinstance(self.current_node.children[2].children[1].children[0], AST):
                                        cols=21
                                    else:
                                        cols=0
                                        
                                self.context.symbol_table.sequence(id=items[1].value, type=self.req_type, rows=rows, cols=cols)
                            else:
                                return
                        else:
                            self.context.symbol_table.variable(id=items[1].value, type=self.req_type) 
                    except AttributeError:
                        self.context.symbol_table.variable(id=items[2].value, type=self.req_type, )

                else:
                    self.context.symbol_table.variable(id=items[2].value, type=self.req_type, )
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
    


    # def more_whl_const(self):
    #     if self.current_node.children[1].type=="Identifier":
    #         self.nearest_id=self.current_node.children[1]
    #         self.create.new_id( type="whole", attribute=CONST)
    # def more_dec_const(self):
    #     if self.current_node.children[1].type=="Identifier":
    #         self.nearest_id=self.current_node.children[1]
    #         self.create.new_id(type="dec", attribute=CONST)
    # def more_sus_const(self):
    #     if self.current_node.children[1].type=="Identifier":
    #         self.nearest_id=self.current_node.children[1]
    #         self.create.new_id(type="sus", attribute=CONST)
    # def more_txt_const(self):
    #     if self.current_node.children[1].type=="Identifier":
    #         self.nearest_id=self.current_node.children[1]
    #         self.create.new_id( type="text", attribute=CONST)
    # def more_chr_const(self):
    #     if self.current_node.children[1].type=="Identifier":
    #         self.nearest_id=self.current_node.children[1]
    #         self.create.new_id( type="charr", attribute=CONST)
    

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
        # except AttributeError:
        #     print(f"Attribute Error sa {self.current_node.root}, had {self.current_node.children}")if self.debug else None
        #     pass

    # def looping_statement(self):
    #     if self.current_node.children[3].type=="Identifier" and self.current_node.children[0].value=="for" and self.current_node.children[2].type=="whole":
    #         self.nearest_id=self.current_node.children[3]
    #         self.create.new_id(type="whole", attribute=VAR)
    #         self.create.assign()

    # def loop_body_statement(self):
    #     # try:
    #         leaves=self.current_node.leaves()
    #         if leaves[2].type=="Identifier" and leaves[0].value=="choose":
    #             self.nearest_id=self.current_node.children[2]
    #             self.check.var()
    #             self.check.var_value()
    #             self.check.scope()
    #         else:
    #             pass
    #     # except IndexError as e:
    #     #     print(f"Index Error sa {self.current_node.root}, had {self.current_node.children}")if self.debug else None
    #     #     pass

    # def func_def(self):

    #     self.current_scope=FUNC

    #     if self.current_node.children[2].type=="Identifier":
    #         self.nearest_id=self.current_node.children[2]
    #         self.create.new_func( type=self.current_node.children[1].children[0].value)
    #     elif self.current_node.children[3].type=="Identifier":
    #         self.nearest_id=self.current_node.children[3]
    #         self.create.new_func( type=self.current_node.children[1].children[0].value)
    

    def id_as_val(self):
        items= self.current_node.leaves()
        if items[0].type=="Identifier":
            self.nearest_id=items[0]
            id_obj=items[0]
            id=id_obj.value
            try:
                if len(items)>1:
                    if items[1].type=="[":
                        self.context.symbol_table.find_seq(id)
                    elif items[1].type=="(":
                        self.context.symbol_table.find_func(id)
                        

                else: 
                    var=self.context.symbol_table.find(id) #NOTE - changed
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
        if self.current_node.children[0].type=="/":
            operand=self.current_node.parent.children[1].leaves()[0]
            if (operand.numerical_value<1 and operand.numerical_value >-1) and operand.numerical_value%1 == 0:
                self.semantic_error(se.ZERO_DIV, operand, "Non-zero value")
            

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



# class Check:
        
#         def __init__(self, semantic: SemanticAnalyzer) -> None:
#             self.semantic=semantic


#         def func(self):
#             id=self.semantic.nearest_id
#             if id.value not in self.semantic.id.accessible_ids():
#                 exp=f"Declared Function {id.value}"
#                 err=se.FUNC_UNDECL
#                 self.semantic.semantic_error(err, id, exp)
#                 return
            
#         def seq(self):
#             id=self.semantic.nearest_id
#             if id.value not in self.semantic.id.accessible_ids():
#                 exp=f"Declared Sequence {id.value}"
#                 err=se.SEQ_UNDECL
#                 self.semantic.semantic_error(err, id, exp)
#                 return
            
#         def var(self):
#             id=self.semantic.nearest_id
#             if id.value not in self.semantic.id.accessible_ids().keys():
#                 exp=f"Declared Variable {id.value}"
#                 err=se.VAR_UNDECL
#                 self.semantic.semantic_error(err, id, exp)
#                 return False
#             else:
#                 self.semantic.create.load_var(id)
#                 return True
                
        

#         def var_value(self):
#             id=self.semantic.nearest_id
#             if id.numerical_value==None:
#                 exp=f"Value for Variable {id.value}"
#                 err=se.VAR_UNDEF
#                 self.semantic.semantic_error(err, id, exp)
#                 return
#             else: return True

#         def var_type(self):
#             id=self.semantic.nearest_id
#             if id.dtype!=self.semantic.req_type:
#                 if not self.semantic.in_arg:
#                     exp=f"Variable of Type {self.semantic.req_type}, Got {id.dtype}"
#                     err=se.VAR_OPERAND_INVALID
#                     self.semantic.semantic_error(err, id, exp)
#                     return
            
#         def scope(self):
#             id=self.semantic.nearest_id
#             if id.scope!=self.semantic.current_scope:
#                 exp=f"In {self.semantic.current_scope} Scope"
#                 err=se.VAR_SCOPE_INVALID
#                 self.semantic.semantic_error(err, id, exp)
#                 print(id.scope, self.semantic.current_scope)if self.debug else None
#                 return


#         def next_operand(self):
#             temp_node=self.semantic.previous_node
#             # try:
#             #     if temp_node.children[1].children[0].type in ["Identifier", "Whole", "Dec"]:
#             #         return temp_node.children[1].children[0]

#             # except AttributeError:
#             #     # return temp_node.children[2]
#             #     if temp_node.children[1].children[0].children[0].type in ["Identifier", "Whole", "Dec"]:
#             #         return temp_node.children[1].children[0].children[0]
#             leaves=temp_node.leaves()
#             if leaves[1].type in ["Identifier", "Whole", "Dec"]:
#                 return leaves[1]
            
        

# class Create:

#     def __init__(self, semantic:SemanticAnalyzer) -> None:
#         self.semantic=semantic


#     def explore(self, map):
#         try:
#             map[self.semantic.current_node.children[0].root]()
#         except AttributeError:
#             map[self.semantic.current_node.children[0].value]()

#         except KeyError:
#             pass

#     def assign(self, to_id=None, )->None:
#         assign_ops=["=", "+=", "-=", "*=", "/=", "%="]
#         op=None
#         for index, vals in enumerate(self.semantic.current_node.leaves()):
#             if vals.type in assign_ops:
#                 op=self.semantic.current_node.leaves()[index].value
#                 break
        

#         if to_id==None:
#             to_id=self.semantic.nearest_id
#         expr=[]
#         value=None
#         if self.semantic.check.var():
#             items=self.semantic.current_node.parent.leaves()
#             temp=self.semantic.current_node.parent.values()
            
#             eq_index=temp.index(op)
#             for children in items[eq_index+1:]:
#                 # try:
#                     if children.type not in ["#", ",", "Newline", "whole", "dec", "sus", "text", "charr", "for" ]:
#                         if children.type=="Identifier":
#                             self.semantic.nearest_id=children
#                             if self.semantic.check.var() and self.semantic.check.var_value():
#                                 expr.append(self.semantic.nearest_id)
#                         elif children.type=="to":
#                             break
#                         else: expr.append(children)
                    
#                 # except AttributeError:
#                 #     raise AttributeError("No Identifier Found")
            
        
#             value=self.semantic.create.eval_arithm(expr)

#             id_ref=self.semantic.parse_tree.symbol_table.accessible_ids()[to_id.value]
#             if id_ref.numerical_value==None:
#                 id_ref.numerical_value=0
#             if op != "=":
#                 if op=="+=":
#                     value+=id_ref.numerical_value
#                 elif op=="-=":
#                     value-=id_ref.numerical_value
#                 elif op=="*=":
#                     value*=id_ref.numerical_value
#                 elif op=="/=":
#                     value/=id_ref.numerical_value
#                 elif op=="%=":
#                     value%=id_ref.numerical_value
    
            
#             if value != None:
#                 if type(value)==self.semantic.data_types[to_id.dtype]:
#                     self.semantic.parse_tree.symbol_table.accessible_ids()[to_id.value].numerical_value=value
#                     return True
#                 else:
                
#                     if value%1==0:
#                         value=self.semantic.data_types[to_id.dtype](value)
#                         self.semantic.parse_tree.symbol_table.accessible_ids()[to_id.value].numerical_value=value
#                         return True
#                     else:
#                         self.semantic.semantic_error(se.VAR_OPERAND_INVALID, to_id, f"Value of Type {to_id.dtype}, got {self.semantic.reverse_types[type(value)]}")
#             else:
#                 self.semantic.semantic_error(se.VAR_UNDEF, to_id, "Value pare")
        
#     def get_var(self, id:Token):
#         try:
#             return self.semantic.id.vars[id.value]
#         except KeyError:
#             self.semantic.semantic_error(se.VAR_UNDECL, id, f"Variable {id.value}")

#     def load_type(self, id:Token):
#         self.semantic.req_type=id.dtype

#     def load_var(self, id:Token):
#         declared=self.semantic.id.vars[id.value]

#         self.semantic.nearest_id.dtype=declared.dtype
#         self.semantic.nearest_id.numerical_value=declared.numerical_value
#         self.semantic.nearest_id.scope=declared.scope
#         self.semantic.nearest_id.attribute=declared.attribute

#         return True


#     def new_id(self, type, scope=const.LOCAL,  attribute=None):
#         id=self.semantic.nearest_id #NOTE - idk if this is the right way to do this
#         if id.value not in self.semantic.id.accessible_ids():
#             id.dtype=type
#             id.attribute=attribute
#             id.scope=self.semantic.current_scope

#             self.semantic.id.vars.add(id)
#             self.semantic.nearest_id=id
#         else:
#             self.semantic.semantic_error(se.VAR_REDECL_INSCOPE, id, f"Other Identifier. Current: {id.value}")


#     def new_func(self,type, attribute=const.FUNC):
#         id=self.semantic.nearest_id
#         if id.value not in self.semantic.id.accessible_ids():
#             id.dtype=type
#             id.attribute=attribute
#             id.scope=const.GBL

#             self.semantic.id.funcs.add(id)
#         else:
#             self.semantic.semantic_error(se.FUNC_REDECL_INSCOPE, id, f"Function {id.value}")

    
#     def new_param(self,  type, scope=const.FUNC, attribute=const.PARAM):
#         id=self.semantic.nearest_id
#         if id.value not in self.semantic.id.params.keys():
#             id.dtype=type
#             id.attribute=attribute
#             id.scope=scope

#             self.semantic.id.params.add(id)
#         else:
#             self.semantic.semantic_error(se.PARAM_REDECL, id, f"Parameter {id.value}")

#     def evaluate(self, eval:list):
#         precedence = {'+':1, '-':1, '*':2, '/':2, '%':2}
#         operator_stack = []
#         operand_stack = []

#         for token in reversed(eval):
#             if token.type == "Identifier":
#                 operand_stack.append(token.numerical_value)
#             elif token.type not in ['+', '-', '*', '/', '^', '(', ')', "=", "%", "Newline"]:
#                 try:
#                     operand_stack.append(float(token.numerical_value))
#                 except ValueError:
#                     operand_stack.append(float(token.numerical_value[1:-1]))
#             elif token.type == '(':
#                 operator_stack.append(token)
#             elif token.type == ')':
#                 while operator_stack[-1].type != '(':
#                     operator = operator_stack.pop().value
#                     operand2 = operand_stack.pop()
#                     operand1 = operand_stack.pop()
#                     if operator == '+':
#                         result = operand1 + operand2
#                     elif operator == '-':
#                         result = operand1 - operand2
#                     elif operator == '*':
#                         result = operand1 * operand2
#                     elif operator == '/':
#                         result = operand1 / operand2
#                     elif operator=='%':
#                         result = operand1 % operand2
#                     operand_stack.append(result)
#                 operator_stack.pop()  # Remove the '(' from the stack
#             else:
#                 while (operator_stack and operator_stack[-1].type != '(' and 
#                     precedence[operator_stack[-1].type] >= precedence[token.type]):
#                     operator = operator_stack.pop().value
#                     operand2 = operand_stack.pop()
#                     operand1 = operand_stack.pop()
#                     if operator == '+':
#                         result = operand1 + operand2
#                     elif operator == '-':
#                         result = operand1 - operand2
#                     elif operator == '*':
#                         result = operand1 * operand2
#                     elif operator == '/':
#                         result = operand1 / operand2
#                     elif operator=='%':
#                         result = operand1 % operand2
#                     operand_stack.append(result)
#                 operator_stack.append(token)

#         while operator_stack:
#             operator = operator_stack.pop().value
#             operand2 = operand_stack.pop()
#             operand1 = operand_stack.pop()
#             if operator == '+':
#                 result = operand1 + operand2
#             elif operator == '-':
#                 result = operand1 - operand2
#             elif operator == '*':
#                 result = operand1 * operand2
#             elif operator == '/':
#                 try:
#                     result = operand1 / operand2
#                 except ZeroDivisionError:
#                     self.semantic.semantic_error(se.ZERO_DIV, token, "Non-zero value")
#             elif operator=='%':
#                 result = operand1 % operand2
#             operand_stack.append(result)

#         print(operand_stack[0]) if self.debug else None
#         return operand_stack[0]
    
#     def eval_arithm(self, expr):

#         eval=[]
#         for match in reversed(expr):
#             if match.type in ["#", "Newline"]:
#                 pass
#             else:
#                 eval.append(match)

#         return self.evaluate(eval)


  