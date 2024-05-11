import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
from source.core.AST import AST



class Loops:
    def __init__(self, node:AST) -> None:

        self.node=node

    def bet(self):
        raise NotImplementedError

    def whilst(self):
        raise NotImplementedError   

    def for_(self):
        
        children=self.codegen.current_node.children

        iterator=None
        end=None
        step=1
        loop_body=self.codegen.current_node.children[-1].children[1]

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
            self.codegen.current_node = self.semantic.parse_tree.traverse(loop_body)
            # self.previous_node=self.current_node
            self.codegen.routines[self.codegen.current_node.root]()
        
            # self.routines["in_loop_body"]()
            iterator.numerical_value+=step
            print("Iterator: ", iterator.numerical_value, "End: ", end.numerical_value, "Step: ", step)

        if self.debug:
            print(f"For Loop: \n\tIterator: {iterator}\n\t End: {end}\n\t Step: {step}")

    def to(self):
        raise NotImplementedError
    
    def felloff(self):
        raise NotImplementedError
    

    def step(self):
        raise NotImplementedError
    
    def pass_(self):
        raise NotImplementedError