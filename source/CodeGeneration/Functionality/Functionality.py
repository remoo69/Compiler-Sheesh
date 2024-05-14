import re
import sys
sys.path.append(".")
# from source.CodeGeneration.CodeGen import CodeGenerator

from source.CodeGeneration.Functionality.Loops import Loops
from source.CodeGeneration.Functionality.ControlFlow import ControlFlow
from source.CodeGeneration.Functionality.Declarations import Identifier, Expression

from source.core.error_types import Semantic_Errors as se
from source.core.AST import AST

debug=False

class Functionality:
    """  
    Algorithm:
    1. Codegen callls to functionality should include the current node and the output stream..
    2. Execute the called functionality from codegen. When executed, execute next node.
    #This is recursive.
    3. Functionality should only take 1 node. This acts as the interface between the codegen and the functions of the compiler.
    4. Output stream stores any printings or outputs from the codegen.
    
    """
    def __init__(self, node:AST, output_stream:list) -> None:
        self.node=node
        self.output=output_stream

        self.classify()




        
    
    
    def classify(self):
        Statement(self.node, self.output)
        # if self.node in loops:
        #     Loops(self.node, self.output)
        # elif self.node in control_flow:
        #     ControlFlow(self.node, self.output)
        # elif self.node in statements:
        #     Statement(self.node, self.output)  
            
    

    
    def yeet(self):
        raise NotImplementedError
    
    def based(self):
        raise NotImplementedError
    
    def def_(self):
        raise NotImplementedError
    
    
    
    


    


   
    def pa_mine(self):
        raise NotImplementedError

class Function:
    def __init__(self, parameters, return_type, body):
        self.parameters:list[str]=[]
        self.return_type:str=None
        self.body:list[Statement]=[]