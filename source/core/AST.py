


import sys
sys.path.append('.')
# import networkx as nx
# import matplotlib.pyplot as plt
from graphviz import Digraph
# from source.core.symbol_table import Token

debug=True

class AST:
    """ 
    This class represents the abstract syntax tree produced during parsing. Adding and traversing nodes is a recursive process. 
    Children can be either tokens or other ASTs (sibling node). 
    """
    created=0
    branches_ended=0
    unended=[]
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
        self.parent=None
        self.root= root
        self.children = []
        self.stack:list[AST]=[]

        
        self.buffer=None

        

    def __repr__(self, level=0):
        # print("Printing Tree from IDK")
        indent = '  ' * level
        repr_str = f"{indent}{self.root}:\n"
        for child in self.children:
            if isinstance(child, AST):
                repr_str += child.__repr__(level + 1)
            else:
                repr_str += f"{indent}  \"{child}\"\n"
        repr_str += f"{indent}\n"
        return repr_str
    
        # return f"{self.root}: {self.children}"
    

    def traverse(self, node):
        """ 
        Traverse the tree in a depth-first manner. When a leaf is reached, get the parent then the sibling ast to the right of the current node.
        """
        if node.children:
            for child in node.children:
                if isinstance(child, AST):  # Check if the child is an AST
                    return child
        # If the node has no children or no AST children, go up the tree to find the next sibling
        while node.parent:
            sibling_index = node.parent.children.index(node) + 1
            if sibling_index < len(node.parent.children):
                for sibling in node.parent.children[sibling_index:]:
                    if isinstance(sibling, AST):  # Check if the sibling is an AST
                        return sibling
            node = node.parent
        # If we've reached the root and there are no more siblings, the tree has been fully traversed
        return None

    
        
    def visualize(self):
        """ This method is used to produce a pdf file of the ast for visualization """
        dot = Digraph(comment='AST')

        def add_nodes_edges(tree, dot=None):
            # Create Digraph object
            if dot is None:
                dot = Digraph(comment='AST')

            # Add node
            dot.node(name=str(id(tree)), label=str(tree.root))

            # Add nodes of children recursively
            for child in tree.children:
                if isinstance(child, AST):
                    # Recursive call
                    add_nodes_edges(child, dot=dot)
                    # Add edge between parent and child
                    dot.edge(str(id(tree)), str(id(child)))
                else:
                    # Add node for leaf (no children)
                    dot.node(name=str(id(child)), label=str(child))
                    # Add edge between parent and leaf
                    dot.edge(str(id(tree)), str(id(child)))

            return dot

        # Add nodes recursively and create a graph
        dot = add_nodes_edges(self)

        # Visualize the graph
        dot.view()

    
    # def draw_graph(tree):
    #     G = nx.DiGraph()

    #     def add_edges(tree):
    #         G.add_node(id(tree), label=str(tree.root))
    #         for child in tree.children:
    #             if isinstance(child, AST):
    #                 add_edges(child)
    #                 G.add_edge(id(tree), id(child))
    #             else:
    #                 G.add_node(id(child), label=str(child))
    #                 G.add_edge(id(tree), id(child))

    #     add_edges(tree)

    #     pos = nx.spring_layout(G)
    #     labels = nx.get_node_attributes(G, 'label')
    #     nx.draw(G, pos, labels=labels, with_labels=True)
    #     plt.show()

    # draw_graph(self)

    def find_node(self, root):
        """ This method just traverses all children and returns the child ast if it exists. This method only checks the top level children. """
        if self.root==root:
            return self
        else:
            for child in self.children:
                if isinstance(child, AST):
                    return child.find_node(root)
                else:
                    if child==root:
                        return child
                    else:
                        pass
            return None
        
    def expand(self):
        return self.children

    def current_func(self, elem=2):
        """ Returns current func for node names """
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

        self.buffer.parent=self.stack[-1] if self.stack!=[] else None

        self.stack.append(self.buffer)
        print(f"Created: {self.stack[-1].root}") if debug else None
        AST.unended.append(self.stack[-1].root)
        

    def add_children(self, children):
        if children.type!="Newline":
            self.buffer.children.append(children)
        else:
            pass


    def end_branch(self):
        """ 
        End branch should add the function to the previous function's children
        """
        try:
            print(f"Ended from {self.stack[-1].root}") if debug else None
            AST.branches_ended+=1
            last:AST=self.stack[-2]
            if self.stack[-1].children==[] or self.stack[-1].children==None:
                self.stack.pop(-1)
                self.buffer=self.stack[-1]
                AST.unended.pop(-1)
            else:
                last.children.append(self.stack[-1])
                self.stack.pop(-1)
                self.buffer=self.stack[-1]
                AST.unended.pop(-1)
        except IndexError as e:
            print(e)
            return

    
    def end_tree(self):
        print(f"Created: {AST.created}, Ended: {AST.branches_ended}, Unended Branches: {AST.unended}") if debug else None
        if len(self.stack)==1:
            self.buffer=self.stack[0]
            self.children.append(self.buffer)
            self.buffer=None
        else:
            raise ValueError("Stack not empty")
        

    def leaves(self):
        """ 
        Returns all the leaves of the tree
        """
        leaves=[]
        for child in self.children:
            if isinstance(child, AST):
                leaves.extend(child.leaves())
            else:
                leaves.append(child)
        return leaves
    
    def values(self):
        """ 
        Returns all the values of the tree
        """
        leaves=self.leaves()
        values=[]

        for leaf in leaves:
            values.append(leaf.value)
        return values

