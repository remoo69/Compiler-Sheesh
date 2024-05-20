import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
from source.core.AST import AST
from source.CodeGeneration.Functionality.Evaluators import Evaluators
from source.core.symbol_table import SymbolTable
import source.core.constants   as const
from source.CodeGeneration.cg2 import CodeGenerator
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
        while Evaluators(runtime_errors=self.codegen.runtime_errors, 
                         expression=condition, 
                         context=self.codegen.context).evaluate(expr=condition, type=const.dtypes.sus)==True:
            
            self.previous_node=self.node
            self.node = self.semantic.parse_tree.traverse(loop_body)
            
            self.routines[self.node.root]()


    def for_(self):
        
        iterator=self.codegen.context.symbol_table.find_var(self.codegen.current_node.children[3].value)
        # iterator.assign(op="=",value= const.types[iterator.type](self.node.children[5].leaves()[0].numerical_value))
        # end=self.node.children[7].leaves()[0].numerical_value #idk if this'll work for seq and funcs
        end=Evaluators(expression=self.codegen.current_node.children[7].leaves(),
                            runtime_errors=self.codegen.runtime_errors,
                            context=self.codegen.context,
                            ).evaluate(type=const.dtypes.whole, expr=self.codegen.current_node.children[7].leaves())
        try:
            step=int(self.codegen.current_node.find_node("step_statement").leaves()[1].numerical_value)
            
        except AttributeError as e:
            step=1

        loop_body=self.codegen.current_node.children[-1]
        
        while iterator.value != end:
            # self.codegen.previous_node=self.codegen.current_node
            # self.codegen.current_node=loop_body
            # self.codegen.current_node = self.codegen.parse_tree.traverse(self.codegen.current_node)
            # self.codegen.routines[self.codegen.current_node.root]()
            # self.codegen.generate_code(loop_body)
            # self.codegen.gen_code(loop_body.children[1])
            code=CodeGenerator(loop_body, self.debug) 
        
            # self.routines["in_loop_body"]()
            iterator.assign("+=",step)
            print("Iterator: ", iterator.value, "End: ", end, "Step: ", step)

        if self.debug:
            print(f"For Loop: \n\tIterator: {iterator}\n\t End: {end}\n\t Step: {step}")

    # def to(self):
    #     raise NotImplementedError
    
    def felloff(self):
        #statement that should break loops
        self.codegen.previous_node=self.codegen.current_node
        self.codegen.current_node = self.codegen.current_node.parent.children[1]
        self.codegen.routines[self.codegen.current_node.root]()
    

    # def step(self):
    #     raise NotImplementedError
    
    def pass_(self):
        if self.codegen.current_node.root=="loop_body_statement":
            self.codegen.previous_node=self.codegen.current_node
            self.codegen.current_node = self.codegen.current_node.parent.children[1]