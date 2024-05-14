import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
from source.core.AST import AST
from source.CodeGeneration.Functionality.Evaluators import Evaluators
from source.core.symbol_table import SymbolTable
import source.core.constants   as const
# from source.CodeGeneration.CodeGen import CodeGenerator
class Loops:
    """  
    Algorithm:
    1. Check the type of loop
    2. Get the loop body
    3. Traverse the loop body
    4. Execute the loop body
    5. When loop body has been executed, check condition
    6. If condition is met, go to loop_body node; re-execute loop body

    """
    def __init__(self, codegen) -> None:
        # self, node:AST, output_stream, symbol_table, current_scope, runtime_errors
        # self.node=node
        # self.leaves=self.node.leaves()
        # self.output_stream=output_stream
        # self.symbol_table:SymbolTable=symbol_table
        # self.current_scope=current_scope
        # self.runtime_errors=runtime_errors
        self.codegen=codegen
        self.debug=True

    def bet_whilst(self):
        condition=self.codegen.current_node.children[5]
        loop_body=self.codegen.current_node.children[1]
        while Evaluators(condition).logic_rel()==False:
            loop_body


    def for_(self):
        
        iterator=self.codegen.symbol_table.find_var(self.codegen.current_node.children[3].value, self.codegen.current_scope)
        iterator.assign(op="=",value= const.types[iterator.type](self.codegen.current_node.children[5].leaves()[0].numerical_value))
        end=self.codegen.current_node.children[7].leaves()[0].numerical_value #idk if this'll work for seq and funcs
        try:
            step=self.codegen.current_node.find_node("step_statement").leaves()[1]
        except AttributeError as e:
            step=1
     
        loop_body=None
        
        children=self.codegen.current_node.children

        loop_body=self.codegen.current_node.children[-1].children[1]

        # if children[3].type=="Identifier":
        #     iterator=children[3]

        # if children[7].root=="whl_value":
        #     end=children[7].leaves()[0]
        #     print(end)

        # try:
        #     if children[8].root=="step_statement":
        #         step=children[8].leaves()[1]
        #         print(step)
        # except AttributeError as e:
        #     print(e)
        #     print("No step statement")

        
        while iterator.value != end:
            self.codegen.current_node = self.codegen.semantic.parse_tree.traverse(loop_body)
            self.previous_node=self.codegen.current_node
            self.codegen.routines[self.codegen.current_node.root]()
        
            # self.routines["in_loop_body"]()
            iterator.assign("+=",step)
            print("Iterator: ", iterator.value, "End: ", end, "Step: ", step)

        if self.debug:
            print(f"For Loop: \n\tIterator: {iterator}\n\t End: {end}\n\t Step: {step}")

    def to(self):
        raise NotImplementedError
    
    def felloff(self):
        #statement that should break loops
        raise NotImplementedError
    

    def step(self):
        raise NotImplementedError
    
    def pass_(self):
        pass