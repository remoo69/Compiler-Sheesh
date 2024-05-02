


import sys

debug=False

class AST:
    created=0
    branches_ended=0
    """ 
    Output should be:
        Root:[root:children, root:[root:[root:children, root:children] ]
      
    Functions needed:
    1. initialize_new: makes new ast, root is caller func name
    2. add_children: append value to list of current children
    3. end_branch: should only be used at the end of the function
    """
    # @memoize
    def __init__(self, root):
        self.root= root
        self.children = []
        self.stack:list[AST]=[]
        
        self.bufer=None


    def __repr__(self, level=0):
        indent = '  ' * level
        repr_str = f"{indent}{self.root}:\n"
        for child in self.children:
            if isinstance(child, AST):
                repr_str += child.__repr__(level + 1)
            else:
                repr_str += f"{indent}  \"{child}\"\n"
        repr_str += f"{indent}\n"
        return repr_str

    def current_func(self, elem=2):

        caller_frame =sys._getframe(elem)
        caller_function_name = caller_frame.f_code.co_name
    
        if caller_function_name in ["wrapper", "nullable", "required", "match", None]:
            return "Outisde"
        else:

            return caller_function_name

    def new_ast(self, root, value):
        self.initialize_new(root)
        self.root=root
        self.children.append(value)


    def initialize_new(self):
        # pass
        AST.created+=1
        root=self.current_func()
        self.buffer=AST(root)
        self.stack.append(self.buffer)
        print(f"Created: {self.stack[-1].root}") if debug else None
        

    def add_children(self, children):
         self.buffer.children.append(children)
        # pass

    def end_branch(self):
        """ 
        End branch should add the function to the previous function's children
        """
        # pass
        try:
            print(f"Ended from {self.stack[-1].root}") if debug else None
            AST.branches_ended+=1
            last:AST=self.stack[-2]
            if self.stack[-1].children==[] or self.stack[-1].children==None:
                self.stack.pop(-1)
            else:
                last.children.append(self.stack[-1])
                self.stack.pop(-1)
                self.buffer=self.stack[-1]
        except IndexError:
            print("End of Trees")
            return

    
    def end_tree(self):
        # pass
        print(f"Created: {AST.created}, Ended: {AST.branches_ended}") if debug else None
        if len(self.stack)==1:
            self.buffer=self.stack[0]
            self.children.append(self.buffer)
            self.buffer=None
        else:
            raise ValueError("Stack not empty")
