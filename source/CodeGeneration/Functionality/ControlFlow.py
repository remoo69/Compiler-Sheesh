import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality


class ControlFlow:
    def __init__(self, node) -> None:
        # self.codegen=functionality.codegen
        # self.debug=functionality.debug
        self.node=node
    def kung(self):

        condition=self.codegen.current_node.children[2].leaves()
        success=self.codegen.current_node.children[4]
        if len(self.codegen.current_node.children)==5:
            fail=self.codegen.current_node.parent.children[0]
            
        else:
            fail=self.codegen.current_node.children[-1] 

        if self.evaluate_condition(condition)==True:
            self.codegen.current_node = self.semantic.parse_tree.traverse(success)
            self.codegen.routines[self.codegen.current_node.root]()

        else:
            if fail==None:
                pass
            else:
                while True:
                    try:
                        self.codegen.current_node = self.semantic.parse_tree.traverse(fail)
                        self.codegen.routines[self.codegen.current_node.root]()
                        break  # if the above lines don't raise an exception, break the loop
                    except KeyError:
                        while self.codegen.current_node.root!="statement":
                            print(self.codegen.current_node.root)
                            self.codegen.current_node = self.codegen.previous_node
                            self.codegen.previous_node=self.codegen.previous_node.parent
                        fail= self.codegen.current_node=self.codegen.current_node.children[1].children[0].children[0]


    def ehkung(self):
        raise NotImplementedError
    
    def deins(self):
        raise NotImplementedError
    
    def choose(self):
        raise NotImplementedError
    
    def when(self):
        raise NotImplementedError
    
    def default(self):
        raise NotImplementedError