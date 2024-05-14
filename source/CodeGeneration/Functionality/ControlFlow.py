import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality
from source.CodeGeneration.Functionality.Evaluators import Evaluators


class ControlFlow:
    """  
    Algorithm:
    1. Check Statement Type
    2. Get condition
    4. Get main body
    5. Get sub-bodies
    6. Evaluate condition, if success, go to main_body node; execute main body
    7. If condition is not met, go to fail node; execute fail node
    8. If fail node is not present, pass
    
    For choose:
    1. Get Check Value
    2. Get bodies
    3. Evaluate check value == body value
    4. If success, execute node; else, check other bodies.
    5. If no body matches, go to default node; execute default node

    """
    def __init__(self, codegen) -> None:
        self.codegen=codegen
        # self.debug=functionality.debug
        # self.node=node
        # self.output_stream=output_stream
        
    def kung(self):
        #initializers
        condition=None
        body=None
        cond_tail=None

        condition=self.codegen.current_node.children[2].leaves()
        success=self.codegen.current_node.children[4]
        if len(self.codegen.current_node.children)==5:
            # fail=self.codegen.current_node.parent.children[0]
            fail=None
            
        else:
            fail=self.codegen.current_node.children[-1] 

        if Evaluators(expression=condition, runtime_errors=self.codegen.runtime_errors, scope=self.codegen.current_scope, symbol_table=self.codegen.symbol_table).evaluate_cond(condition)==True:
            self.codegen.current_node = self.semantic.parse_tree.traverse(success)
            self.codegen.routines[self.codegen.current_node.root]()

        else:
            if fail==None:
                pass
            else:
                while True:
                    try:
                        self.codegen.current_node = self.codegen.semantic.parse_tree.traverse(fail)
                        self.codegen.routines[self.codegen.current_node.root]()
                        break  # if the above lines don't raise an exception, break the loop
                    except KeyError:
                        while self.codegen.current_node.root!="statement":
                            print(self.codegen.current_node.root)
                            self.codegen.current_node = self.codegen.previous_node
                            self.codegen.previous_node=self.codegen.previous_node.parent
                        fail= self.codegen.current_node=self.codegen.current_node.children[1].children[0].children[0]


    def ehkung(self):
        condition=None
        body=None
    
    def deins(self):
        body=None
    
    def choose(self):
        checker=None
        body=None
    
    def when(self):
        raise NotImplementedError
    
    def default(self):
        raise NotImplementedError