import re
import sys

sys.path.append('.')
# from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_handler import RuntimeError as RError
from source.core.error_handler import SemanticError as SError
from source.core.error_types import Semantic_Errors as se
import source.core.constants as const
from source.core.symbol_table import SymbolTable, Context

from source.CodeGeneration.Functionality.ControlFlow import ControlFlow
from source.CodeGeneration.Functionality.Loops import Loops
# from source.CodeGeneration.Functionality.Declarations import Identifier
from source.CodeGeneration.Functionality.Evaluators import Evaluators
from source.CodeGeneration.Functionality.InOut import InOut
from source.core.AST import AST
from copy import deepcopy



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
    
    Code Generator Tasks:
    1. Each node in the ast is traversed during code generation + semantic analysis. 
    2. Variables are created and directly added to the symbol table.
    3. Functions such as up, pa_mine, and user defined function invocations function similarly. Arguments are assigned to parameters as variables in the function block.
        the body of the function is then executed using gen_code()<-might need some optimization/fixing
    4. Each method in this class represents a node in the ast and extracts necessary information for the execution of the node. 
    5. 
    
    """
    def __init__(self, parse_tree:AST, debugMode) -> None:

        self.debug=debugMode

        self.parse_tree=parse_tree
        # self.symbol_table=SymbolTable()
        
        self.output_stream={}

        self.matched=self.parse_tree.leaves()
        
        self.req_type=None
        self.current_node:AST = parse_tree
        self.previous_node:AST=None #Stores the previous node to handle loops?
        self.nearest_id=None

        self.semantic_errors:list[SError]=[]
        self.runtime_errors:list[RError] = []

        # self.scope_tree=self.symbol_table.scopetree
        self.context:Context=None
        self.new_context(const.GBL)
        self.ctx_dict={}
        

        self.reverse_types={v:k for k, v in const.types.items()}

        self.block_counter=1
        self.temp_id=None
        """  
        Routines act as the entry point for the functions in the program. As such, each routine should contain their respective
        functionalities. 
        """
        self.routines={

            # "sheesh_declaration": self.sheesh_declaration,
            "allowed_in_loop": self.allowed_in_loop,
            # "id_tail": self.id_tail, #handled in backend
            # "id_next_tail": self.id_next_tail,
            "reg_body": self.reg_body,
            "var_or_seq_dec": self.var_or_seq_dec,
            # "val_assign": self.val_assign, #handled in backend; var or seq dec
            # "all_value": self.all_value,
            # "seq_tail": self.seq_tail,
            # "seq_init": self.seq_init,
            # "var_seq_tail": self.var_seq_tail,
            # "txt_op": self.txt_op,
            "const_type": self.const_type,
            "in_loop_body":self.in_loop_body,
            # "loop_body":self.loop_body,
            # "const_dimtail1": self.const_dimtail1,
            # "const_dimtail2": self.const_dimtail2,
            # "const_var_tail": self.const_var_tail,
            # "const_tail": self.const_tail,
            # "control_flow_statement": self.control_flow_statement,
            # "ehkung_statement": self.ehkung_statement,
            # "cond_tail": self.cond_tail,
            # "when_statement": self.when_statement,
            # "statement_for_choose": self.statement_for_choose,
            # "choose_default": self.choose_default,
            "looping_statement": self.looping_statement,
            "func_def": self.func_def,
            "loop_body_statement": self.loop_body_statement,
            "control_flow_statement":self.control_flow_statement,
            # "yeet_statement": self.yeet_statement, 
            # "step_statement": self.step_statement,
            # "loop_body_statement": self.loop_body_statement,
            # "loop_ehkung": self.loop_ehkung,
            # "in_loop_condtail": self.in_loop_condtail,
            # "loop_when": self.loop_when,
            # "loop_default": self.loop_default,
            # "yeet_statement": self.yeet_statement,
            # "func_def": self.func_def,
            # "id_as_val": self.id_as_val,
            # "id_val_tail": self.id_val_tail,
            # "assign_value": self.assign_value,
            # "literal_or_expr": self.literal_or_expr,
            # "l_expr_withparen": self.l_expr_withparen,
            # "charr_op_tail": self.charr_op_tail,
            # "condition": self.condition,
            # "id_val_op": self.id_val_op,
            # "id_val_paren": self.id_val_paren,
            # "logic_value": self.logic_value,
            # "l_val_withparen": self.l_val_withparen,
            # "logic_not_expr": self.logic_not_expr,
            # "logic_expr": self.logic_expr,
            # "logic_id": self.logic_id,
            # "logic_id_tail": self.logic_id_tail,
            # "num_arithm": self.num_arithm,
            # "num_arithmparen": self.num_arithmparen,
            # "id_arithm": self.id_arithm,
            # "id_arithm_paren": self.id_arithm_paren,
            # "id_arithm_tail": self.id_arithm_tail,
            # "num_or_arithmexpr": self.num_or_arithmexpr,
            # "num_or_arithmparen": self.num_or_arithmparen,
            # "num_math_op": self.num_math_op,
            # "rel_expr": self.rel_expr,
            # "rel_val": self.rel_val


    
        }


    def new_context(self, context):
        self.context=Context(context, self.context)
        cpy=self.context.deepcopy()
        self.ctx_dict[context]=cpy
        
    # def get_context(self, context):
        
        
    def generate_code(self):
        print("Generating code...")
        while True:
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                try:
                    self.current_node = self.parse_tree.traverse(self.current_node)
                except AttributeError:
                    break
            if self.current_node is None:
                # print(self.scope_tree)
                break  # Exit the loop if the tree has been fully traversed
            
    def gen_code(self, node):
        print("Generating code for node...")
        current_node=node
        previous_node=None
        while True:
            if current_node.root not in self.routines.keys():
                previous_node=current_node
                current_node = self.parse_tree.traverse(current_node)
            else:
                self.routines[current_node.root]()
                previous_node=current_node
                try:
                    current_node = self.parse_tree.traverse(current_node)
                except AttributeError:
                    break
            if current_node is None:
                # print(self.scope_tree)
                break  # Exit the loop if the tree has been fully traversed
            
    def advance(self):
        self.previous_node=self.current_node
        self.current_node = self.parse_tree.traverse(self.current_node)
        self.routines[self.current_node.root]()
        
    
    def allowed_in_loop(self):
        current=self.current_node
        if isinstance(self.current_node.children[0], AST):
            return
        if self.current_node.children[0].value=="up":
            up=InOut(node=current, 
                  output_stream=self.output_stream, 
                  symbol_table=self.symbol_table, 
                  current_scope=self.current_scope, 
                  runtime_errors=self.runtime_errors)
            up.up()
            self.runtime_errors+=up.runtime_errors
            
        elif self.current_node.children[0].type=="Identifier":
            id=Identifier(node=current, 
                       output_stream=self.output_stream, 
                       symbol_table=self.symbol_table, 
                       current_scope=self.current_scope, 
                       runtime_errors=self.runtime_errors).id_tail()
            self.runtime_errors+=id.runtime_errors
        
        else: return

    
    def reg_body(self): #FIXME - IDK if it'll be an issue, but I'm not sure this resets to the previous block after the block ends. 
        if self.current_node.parent.root=="sheesh_declaration":
            # self.current_scope=self.scope_tree.add(self.current_scope, "FUNCTION sheesh")
            self.new_context("FUNCTION sheesh")
        else:
            if self.current_node.parent.parent.root=="func_def":
                self.new_context(f"FUNCTION {self.current_node.parent.parent.children[2].value}")
                # self.current_scope=self.scope_tree.add(self.current_scope, f"FUNCTION {self.current_node.parent.parent.children[2].value}")
            else:
                self.new_context(f"{self.current_node.parent.children[0].value} {self.block_counter}")
                self.block_counter+=1

    def in_loop_body(self):
        if isinstance(self.current_node.parent.children[0], AST):
            # self.current_scope=self.scope_tree.add(context=self.current_scope, scope=f"{self.current_node.parent.children[0].children[0].value} {self.block_counter}")
            self.new_context(f"{self.current_node.parent.children[0].children[0].value} {self.block_counter}")
            self.block_counter+=1
        else:
            # self.current_scope=self.scope_tree.add(context=self.current_scope, scope=f"{self.current_node.parent.children[0].value} {self.block_counter}")
            self.new_context(f"{self.current_node.parent.children[0].value} {self.block_counter}")
            self.block_counter+=1
    
    def loop_body_statement(self):
        if isinstance(self.current_node.children[0], AST):
            self.previous_node=self.current_node
            self.current_node = self.parse_tree.traverse(self.current_node)
           
            self.routines[self.current_node.root]()
        else:
            if self.current_node.children[0].type=="kung":
                ControlFlow(self).kung()
            elif self.current_node.children[0].type=="choose":
                ControlFlow(self).choose_when_default()
            elif self.current_node.children[0].value=="felloff":
                Loops(self).felloff()
            elif self.current_node.children[0].value=="pass":
                Loops(self).pass_()
                
    # def loop_body(self):
    #     main=self.current_node.children[0]
    #     m=CodeGenerator(main, False)
    #     m.current_scope=self.current_scope
    #     m.symbol_table=self.symbol_table
    #     m.generate_code()
    #     if len(self.current_node.children)>1:
    #         next=self.current_node.children[1]
    #         n=CodeGenerator(next, False)
    #         n.current_scope=self.current_scope
    #         n.symbol_table=self.symbol_table
    #         n.generate_code()
        
    def var_or_seq_dec(self):
        type=self.current_node.children[0].value

        if type==const.dtypes.charr:
            id=self.current_node.children[2]
        else:
            id=self.current_node.children[1]

        # print(self.current_node.children[-2].children[0].root[2:])
        if isinstance(self.current_node.children[-2], AST):
            if self.current_node.children[-2].children[0].root[2:]=="vardec_tail":
                items=self.current_node.children[-2].children[0].leaves()
                for i,item in enumerate(items):
                    if item.type==",":
                        pass
                    elif item.type=="=":
                        try:
                            self.symbol_table.variable(id=id.value,
                                                    type=type,
                                                    scope=self.current_scope).assign(op=item.type,
                                                                                        value=Evaluators(
                                                                                            expression=self.current_node.children[-2].children[0].children[0].children[1].leaves(),
                                                                                            runtime_errors=self.runtime_errors,
                                                                                            scope=self.current_scope,
                                                                                            symbol_table=self.symbol_table
                                                                                        ).evaluate(expr=self.current_node.children[-2].children[0].children[0].children[1].leaves(),
                                                                                                type=type))
                        except KeyError as e:
                            e=str(e)[1:-1]
                            self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                    elif item.type=="Identifier":
                        if items[i+1].type=="=":
                            try:
                                op=items[i+1].type
                                value=[]
                                j=0
                                while items[i+j].type not in [const.asop, "," ]:
                                    value.append(items[i+j])#tokens
                                    j+=1
                                value=Evaluators(expression=value, 
                                                runtime_errors=self.runtime_errors, 
                                                scope=self.current_scope, 
                                                symbol_table=self.symbol_table).evaluate()
                                
                                self.symbol_table.variable(id=item.value, 
                                                        type=type, 
                                                        scope=self.current_scope).assign(op=op, value=value )
                            except KeyError as e:
                                e=str(e)[1:-1]
                                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                        else:
                            try:
                                self.symbol_table.variable(item.value, type, self.current_scope)
                            except KeyError as e:
                                e=str(e)[1:-1]
                                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                    elif item.type=="#":
                        break
                    else:
                        pass
            elif self.current_node.children[-2].children[0].root=="index":
                rows=0
                cols=0
                index=[]
                items=self.current_node.children[-2].children[0].leaves()
                k=0
                while items[k].type not in [const.asop]:
                    index.append(items[k])
                    
                    if items[k].type=="]":
                        break
                    k+=1
                    
                try:
                    rows=Evaluators(expression=index, 
                                    runtime_errors=self.runtime_errors, 
                                    scope=self.current_scope, 
                                    symbol_table=self.symbol_table).evaluate(expr= index[1:-1], type=const.dtypes.whole)
                    if len(self.current_node.children[-2].children)>1:
                        items=self.current_node.children[-2].children[1].leaves()
                        if items[0].type=="[":
                            col=[]
                            k=0
                            while items[k].type not in [const.asop]:
                                col.append(items[k])
                                if items[k].type=="]":
                                    break
                                k+=1
                            cols=Evaluators(expression=index, 
                                            runtime_errors=self.runtime_errors, 
                                            scope=self.current_scope, 
                                            symbol_table=self.symbol_table).evaluate(expr=col[1:-1], type=const.dtypes.whole)
                    
                    if len(self.current_node.children[-2].children)>1:
                        if isinstance(self.current_node.children[-2].children[1].children[0], AST):
                            if self.current_node.children[-2].children[1].children[0].root=="index":
                                items=self.current_node.children[-2].children[1].leaves()
                                for i,item in enumerate(items):
                                    if item.type==",":
                                        pass
                                    elif item.type=="Identifier":
                                        if items[i+1].type=="=":
                                            op=items[i+1].type
                                            value=[]
                                            j=0
                                            while items[i+j].type not in [const.asop, "," ]:
                                                value.append(items[i+j])
                except KeyError as e:
                    e=str(e)[1:-1]
                    self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
                        
                else:
                    try:    
                        self.symbol_table.sequence(id=id, type=type, scope=self.current_scope, rows=rows, cols=cols)
                    except KeyError as e:
                        e=str(e)[1:-1]
                        self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
        else:
            try:
                self.symbol_table.variable(id=id, type=type, scope=self.current_scope)
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))

    def const_type(self):  
        type=self.current_node.children[0].value
        id=self.current_node.children[1].value
        if self.current_node.children[-1].children[0].root=="index":
            index=[]
            items=self.current_node.children[-1].children[0].leaves()
            k=0
            while items[k].type not in [const.asop]:
                index.append(items[k])
                
                if items[k].type=="]":
                    break
                k+=1
                
            try:
                rows=Evaluators(expression=index, 
                                runtime_errors=self.runtime_errors, 
                                scope=self.current_scope, 
                                symbol_table=self.symbol_table).evaluate(expr= index[1:-1], type=type)
                if len(self.current_node.children[-1].children)>1:
                    items=self.current_node.children[-1].children[1].leaves()
                    if items[0].type=="[":
                        col=[]
                        k=0
                        while items[k].type not in [const.asop]:
                            col.append(items[k])
                            if items[k].type=="]":
                                break
                            k+=1
                        cols=Evaluators(expression=index, 
                                        runtime_errors=self.runtime_errors, 
                                        scope=self.current_scope, 
                                        symbol_table=self.symbol_table).evaluate(expr=col[1:-1])
                        
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=items[k], expected=se.expected[e]))
                
            if len(self.current_node.children[-1].children)>1:
                if isinstance(self.current_node.children[-1].children[1].children[0], AST):
                    if self.current_node.children[-1].children[1].children[0].root=="index":
                        items=self.current_node.children[-1].children[1].leaves()
                        for i,item in enumerate(items):
                            if item.type==",":
                                pass
                            elif item.type=="Identifier":
                                if items[i+1].type=="=":
                                    op=items[i+1].type
                                    value=[]
                                    j=0
                                    while items[i+j].type not in [const.asop, "," ]:
                                        value.append(items[i+j])
                    
            else:
                try:
                    self.symbol_table.sequence(id=id, type=type, scope=self.current_scope, rows=rows, cols=cols)
                except KeyError as e:
                    e=str(e)[1:-1]
                    self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))
    
    
    def control_flow_statement(self):
        if self.current_node.children[0].type=="kung":
            ControlFlow(codegen=self).kung()
                # node=self.current_node, 
                #         output_stream=self.output_stream, 
                #         symbol_table=self.symbol_table, 
                #         current_scope=self.current_scope, 
                #         runtime_errors=self.runtime_errors).kung()
            
        elif self.current_node.children[0].type=="choose":
            ControlFlow(node=self.current_node, 
                        output_stream=self.output_stream, 
                        symbol_table=self.symbol_table, 
                        current_scope=self.current_scope, 
                        runtime_errors=self.runtime_errors).choose_when_default()
        else:
            raise ValueError("ERROR??????????") #NOTE - huy alisin mo to

    
    def ehkung_statement(self):
        raise NotImplementedError
    
    def looping_statement(self):
        if self.current_node.children[0].type=="bet":
            Loops(node=self.current_node, 
                  output_stream=self.output_stream, 
                  symbol_table=self.symbol_table, 
                  current_scope=self.current_scope, 
                  runtime_errors=self.runtime_errors,
                  codegen=self).bet_whilst()
            
            
        elif self.current_node.children[0].type=="for":
            try:
                self.symbol_table.variable(id=self.current_node.children[3].value,
                                        type=self.current_node.children[2].value,
                                        scope=self.current_scope).assign(op=self.current_node.children[4].type,
                                                                            value=Evaluators(expression=self.current_node.children[5],
                                                                                            runtime_errors=self.runtime_errors,
                                                                                            scope=self.current_scope,
                                                                                            symbol_table=self.symbol_table).evaluate(expr=self.current_node.children[5].leaves(), type=self.current_node.children[2].value))
            except KeyError as e:
                e=str(e)[1:-1]
                self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))                          
            Loops(codegen=self).for_()    
    
    # def yeet_statement(self): #NOTE idk dito
    #     return Evaluators(
    #         expression=self.current_node.children[1],
    #         runtime_errors=self.runtime_errors,
    #         scope=self.current_scope,
    #         symbol_table=self.symbol_table
    #     ).evaluate(expr=self.current_node.children[1].leaves(), type=self.)
    
    def func_def(self):
        """  
        To do:
        1. 
        2.  
        """
        dtype=self.current_node.children[1].leaves()[0].value
        id=self.current_node.children[2].value
        parameters=self.current_node.children[3]
        tail=self.current_node.children[-1]
        try:
            self.symbol_table.function(id=id,
                                    return_type=dtype,
                                    parameters=parameters,
                                    body=tail,)
        except KeyError as e:
            e=str(e)[1:-1]
            self.runtime_errors.append(RError(error=getattr(se, e), token=id, expected=se.expected[e]))

        

    
import sys
sys.path.append(".")
from source.CodeGeneration.cg2 import CodeGenerator
from source.core.symbol_table import Function
# from source.core.AST import AST



class FuncRunner:
    def __init__(self, func:Function, arguments):
        self.func=func
        self.body=func.func_body
        # self.codegen=codegen
        self.arguments=arguments
        self.runtime_errors=[]
        self.debug=False
        
    def run(self):
        run=CodeGenerator(self.body, self.debug)
        run.current_scope=f"FUNCTION {self.func.id}"
        for i,arg in enumerate(self.arguments):
            run.symbol_table.variable(
                name=self.func.parameters[i].id, 
                dtype=self.func.parameters[i].type, 
                scope=run.current_scope
            ).assign("=", arg)
            
        return run.generate_code()







