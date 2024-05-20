import re
import sys

sys.path.append('.')
# from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_handler import RuntimeError as RError
from source.core.error_handler import SemanticError as SError
from source.core.error_types import Semantic_Errors as se
import source.core.constants as const
from source.core.symbol_table import SymbolTable, ScopeTree

from source.CodeGeneration.Functionality.ControlFlow import ControlFlow
from source.CodeGeneration.Functionality.Loops import Loops
from source.CodeGeneration.Functionality.Declarations import Identifier
from source.CodeGeneration.Functionality.Evaluators import Evaluators
from source.CodeGeneration.Functionality.InOut import InOut
from source.core.AST import AST



"""  
TODO
1. Literal Limits
2. Choose-when-default
3. Func def,call, as expr, prototype #NOTE - partially done
4. Sequence def, init, call, as expr #NOTE  - started
5. Multiple init
6. Seq bounds checking
7. Seq size enforcement

8. Break when runtime or semantic error

"""
class CodeGenerator:
    """  
    *UPDATE: CODE GEN NOW INCLUDES SEMNATIC ANALYZER

    General Code Generator Logic: Traverse all nodes in the AST. Go to respective routines based on the node's root.
    Algorithm:
    * The Code Generator Functions like a Depth First Search Traversal.
    * The code gen executes routines based on the current node's leaf or root, depending on the implementation for that type.
    1. Traverse the tree
    2. If a root with a routine is found, execute routine.
    3. If success, go to the next node.
    4. If fail, raise runtime error.


    Update:
        A routine exists for each node where the node's first set is a terminal. This is to ensure that all possible outcomes in the code generator has an output.
        In some cases, however, multiple nodes are agreggated into one if their functions are similar. This is to reduce redundancy in the code generator.
    
    Functionalities will be direct calls to their respective modules. This is to ensure that the code generator is modular and can be easily updated.
    
    """
    def __init__(self, parse_tree:AST, debugMode) -> None:

        self.debug=debugMode

        self.parse_tree=parse_tree
        self.symbol_table=SymbolTable()
        
        self.output_stream={}

        self.matched=self.semantic.parse_tree.leaves()


        self.req_type=None
        self.current_node:AST = parse_tree
        self.previous_node=None #Stores the previous node to handle loops?
        self.nearest_id=None

        self.semantic_errors:list[SError]=[]
        self.runtime_errors:list[RError] = []

        self.scope_tree=ScopeTree(const.GBL)
        self.current_scope=const.GBL

        self.reverse_types={v:k for k, v in const.types.items()}

        """  
        Routines act as the entry point for the functions in the program. As such, each routine should contain their respective
        functionalities. 
        """
        self.routines={

       

            # "looping_statement":self.looping_statement,
            # "loop_body_statement":self.loop_body_statement,
            # "in_loop_body":self.in_loop_body,
            # "loop_body":self.loop_body,
            # "more_loop_body":self.more_loop_body,
            # "control_flow_statement":self.control_flow_statement,
            # # "statement":self.statement,
            # # "in_param":self.in_param,
            # # "more_param":self.more_param,
            # # "sheesh_declaration":self.sheesh_declaration,
            # "allowed_in_loop":self.allowed_in_loop,
            # # "id_tail":self.id_tail,
            # # "id_next_tail":self.id_next_tail,
            # # "up_argument":self.up_argument, #NOTE - idk
            # # "reg_body":self.reg_body,
            # # "in_loop_body":self.in_loop_body,
            # "var_or_seq_dec":self.var_or_seq_dec,
            # "w_val_assign":self.w_val_assign,
            # "more_whl_var":self.more_whl_var,
            # "whl_all_value":self.whl_all_value,
            # "whl_value":self.whl_value,
            # "whl_val_withparen":self.whl_val_withparen,
            # "w_seq_tail":self.w_seq_tail,
            # "w_seq_init":self.w_seq_init,
            # "w_elem_init":self.w_elem_init,
            # "w_two_d_init":self.w_two_d_init, #NOTE - might not get detected?
            # "next_whl_init":self.next_whl_init,
            # "d_val_assign":self.d_val_assign,
            # "more_dec_var":self.more_dec_var,
            # "dec_all_value":self.dec_all_value,
            # "dec_value":self.dec_value,
            # "dec_val_withparen":self.dec_val_withparen,
            # "d_seq_tail":self.d_seq_tail,
            # "d_seq_init":self.d_seq_init,
            # "d_elem_init":self.d_elem_init,
            # "d_two_d_init":self.d_two_d_init, #NOTE - might not get detected?
            # "next_dec_init":self.next_dec_init,
            # "s_val_assign":self.s_val_assign,
            # "more_sus_var":self.more_sus_var,
            # "sus_all_value":self.sus_all_value,
            # "sus_value":self.sus_value,
            # "sus_val_withparen":self.sus_val_withparen,
            # "s_seq_tail":self.s_seq_tail,
            # "s_seq_init":self.s_seq_init,
            # "s_elem_init":self.s_elem_init,
            # "s_two_d_init":self.s_two_d_init, #NOTE - might not get detected?
            # "next_sus_init":self.next_sus_init,
            # "t_val_assign":self.t_val_assign,
            # "more_txt_var":self.more_txt_var,
            # "txt_all_value":self.txt_all_value,
            # "txt_value":self.txt_value,
            # "txt_val_withparen":self.txt_val_withparen,
            # "t_seq_tail":self.t_seq_tail,
            # "t_seq_init":self.t_seq_init,
            # "t_elem_init":self.t_elem_init,
            # "t_two_d_init":self.t_two_d_init, #NOTE - might not get detected?
            # "next_txt_init":self.next_txt_init,
            # "c_val_assign":self.c_val_assign,
            # "more_chr_var":self.more_chr_var,
            # "charr_all_value":self.charr_all_value,
            # "charr_value":self.charr_value,
            # "func_call" : self.func_call,
            # "index":self.index,
            # # "constant_declaration":self.constant_declaration,
            # "id_as_val":self.id_as_val,
            # "func_def":self.func_def,
            # "loop_body_statement": self.loop_body_statement,

            # "parameter": self.parameter,
            # "in_param": self.in_param, #merged to funcdef

            "sheesh_declaration": self.sheesh_declaration,
            "allowed_in_loop": self.allowed_in_loop,
            "id_tail": self.id_tail,
            "id_next_tail": self.id_next_tail,
            "reg_body": self.reg_body,
            "var_or_seq_dec": self.var_or_seq_dec,
            "val_assign": self.val_assign,
            "all_value": self.all_value,
            "seq_tail": self.seq_tail,
            "seq_init": self.seq_init,
            "var_seq_tail": self.var_seq_tail,
            "txt_op": self.txt_op,
            "const_type": self.const_type,
            "const_dimtail1": self.const_dimtail1,
            "const_dimtail2": self.const_dimtail2,
            "const_var_tail": self.const_var_tail,
            "const_tail": self.const_tail,
            "control_flow_statement": self.control_flow_statement,
            "ehkung_statement": self.ehkung_statement,
            "cond_tail": self.cond_tail,
            "when_statement": self.when_statement,
            "statement_for_choose": self.statement_for_choose,
            "choose_default": self.choose_default,
            "looping_statement": self.looping_statement,
            "step_statement": self.step_statement,
            "loop_body_statement": self.loop_body_statement,
            "loop_ehkung": self.loop_ehkung,
            "in_loop_condtail": self.in_loop_condtail,
            "loop_when": self.loop_when,
            "loop_default": self.loop_default,
            "yeet_statement": self.yeet_statement,
            "func_def": self.func_def,
            "id_as_val": self.id_as_val,
            "id_val_tail": self.id_val_tail,
            "assign_value": self.assign_value,
            "literal_or_expr": self.literal_or_expr,
            "l_expr_withparen": self.l_expr_withparen,
            "charr_op_tail": self.charr_op_tail,
            "condition": self.condition,
            "id_val_op": self.id_val_op,
            "id_val_paren": self.id_val_paren,
            "logic_value": self.logic_value,
            "l_val_withparen": self.l_val_withparen,
            "logic_not_expr": self.logic_not_expr,
            "logic_expr": self.logic_expr,
            "logic_id": self.logic_id,
            "logic_id_tail": self.logic_id_tail,
            "num_arithm": self.num_arithm,
            "num_arithmparen": self.num_arithmparen,
            "id_arithm": self.id_arithm,
            "id_arithm_paren": self.id_arithm_paren,
            "id_arithm_tail": self.id_arithm_tail,
            "num_or_arithmexpr": self.num_or_arithmexpr,
            "num_or_arithmparen": self.num_or_arithmparen,
            "num_math_op": self.num_math_op,
            "rel_expr": self.rel_expr,
            "rel_val": self.rel_val


    
        }

    def statement(self):
        pass

    def generate_code(self):
        print("Generating code...")
        while True:
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                try:
                    self.current_node = self.semantic.parse_tree.traverse(self.current_node)
                except AttributeError:
                    break
            if self.current_node is None:
                break  # Exit the loop if the tree has been fully traversed

    
    
    
    def loop_body_statement(self):

        try:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines[self.current_node.root]()

        except KeyError:
            if self.previous_node.children[0].type=="kung":
                self.current_node=self.previous_node
                ControlFlow(self).kung()
            try:
                if self.previous_node.parent.children[-1].root=="more_loop_body":
                    self.previous=self.current_node
                    self.current_node=self.previous_node.parent.children[-1]
                    self.routines["more_loop_body"]()
            except AttributeError:
                pass
            

    def looping_statement(self):
        if self.current_node.children[0].value=="for":
            Loops(self).for_()

        elif self.current_node.children[0].value=="bet":
            self.functionality["bet"]()

    def id_as_val(self):
        """  
        Each execute/evaluate should return a value? idk 
        """
        items= self.current_node.leaves()
        if items[0].type=="Identifier":
            id_obj=items[0]
            id=id_obj.value
            try:
                if len(items)>1:
                    if items[1].type=="[":
                        row=self.current_node.find_node("whl_value").evaluate #FIXME - hmmm idk 
                        try:
                            col=self.current_node.find_node("")
                        except ValueError:
                            pass

                        var=self.symbol_table.find_seq(id, self.current_scope).get(row, col)
                    elif items[1].type=="(":
                        self.symbol_table.find_func(id).execute()
                        

                else: 
                    var=self.symbol_table.find_var(id, self.current_scope)._evaluate()
                    if var==None:
                        self.semantic_error(se.VAR_UNDEF, id_obj, se.expected["VAR_UNDEF"])
            except AttributeError as e:
                e=str(e)
                self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])

        else: pass
    def var_or_seq_dec(self):
        items=self.current_node.leaves()
        self.req_type=items[0].value
        try:
            if self.current_node.children[1].type=="Identifier":
               
                if isinstance(self.current_node.children[2], AST):
                    samp=self.current_node.children[2].leaves()[0].value
                    print(samp)
                    if samp in const.asop:
                        id=self.current_node.children[1]
                        Evaluators(self.current_node.leaves(), runtime_errors=self.runtime_errors, scope=self.current_scope, symbol_table=self.symbol_table).assign(id)
                        print(self.symbol_table)
                else:
                    self.symbol_table.find_var(self.current_node.children[1].value, self.current_scope)
        except AttributeError:
            if self.current_node.children[2].type=="Identifier":
                self.symbol_table.find_var(self.current_node.children[2].value, self.current_scope).assign("=", Evaluators(self.current_node.children[0]).general_evaluator(self.current_node.children))
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
            val=self.current_node.children[0].type
            items=self.current_node.leaves()
            if val =="up":
                InOut(self.current_node, self.output_stream, self.symbol_table, self.current_scope, self.runtime_errors).up()
            elif val=="Identifier":
                self.nearest_id=items[0]
                id_obj=items[0]
                id=id_obj.value

                if items[1].type=="[":
                    self.symbol_table.find_seq(id, self.current_scope)
                elif items[1].type=="(":
                    self.symbol_table.find_func(id)
                elif items[1].type in const.asop:
                    var=self.symbol_table.find_var(id, self.current_scope)
                    self.req_type=var.type
                    try:
                        for item in items:
                            if item.type=="#":
                                break
                            if item.type in ["Whole", "Dec", "Sus", "Text", "Charr"]:
                                if str(item.type).lower()!=str(self.req_type).lower():
                                    self.semantic_error(se.VAR_OPERAND_INVALID, item, f"Variable of Type {self.req_type}, Got {item.type}")
                    except AttributeError as e:
                        e=str(e)
                        self.semantic_error(error=getattr(se, e), token=id_obj, expected=se.expected[str(e)])
        
                Identifier(node=self.current_node,output_stream= self.output_stream, symbol_table=self.symbol_table, runtime_errors=self.runtime_errors, current_scope=self.current_scope).id_tail()
        except AttributeError:
            #Probably in different node
            pass
        
    def in_loop_body(self):
        try:
            # self.functionality[self.current_node.root]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            # self.routines["loop_body"]()
            

    def loop_body(self):
        try:
            self.functionality[self.current_node.children[0].children[0].children[0].value]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except AttributeError: 
            self.functionality[self.current_node.children[0]]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node) 
            self.routines["loop_body_statement"]()  
            
    def control_flow_statement(self):
        if self.current_node.children[0].value =="choose":
            ControlFlow(self).choose()
        elif self.current_node.children[0].value =="kung":

            ControlFlow(self).kung()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)

    def func_def(self):
        type=self.current_node.children[1].leaves()[0].value
        id=self.current_node.children[2].value
        parameters=self.current_node.children[4]
        body=None
        
        if isinstance(self.current_node.children[-1].children[0], AST):
            body=self.current_node.children[-1].children[0]
            
        self.symbol_table.function(id=id, return_type=type, parameters=parameters, body=body)




    
    
    







