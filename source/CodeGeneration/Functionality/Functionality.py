import re
import sys
sys.path.append(".")
# from source.CodeGeneration.CodeGen import CodeGenerator

from source.CodeGeneration.Functionality.Loops import Loops
from source.CodeGeneration.Functionality.ControlFlow import ControlFlow
from source.CodeGeneration.Functionality.Variables import Variables, Sequences
from source.CodeGeneration.Functionality.InOut import InOut

from source.core.error_types import Semantic_Errors as se

debug=False

class Functionality:
    def __init__(self, debugMode) -> None:

        self.debug=debugMode

        # self.codegen=codegen

        self.loops=Loops(self)
        self.control=ControlFlow(self)
        # self.variables=Variables(self)
        # self.sequences=Sequences(self)
        self.io=InOut(self)

        
    
    

    
    
    def concat(self):
        raise NotImplementedError
    
    def yeet(self):
        raise NotImplementedError
    
    def based(self):
        raise NotImplementedError
    
    def def_(self):
        raise NotImplementedError
    
    
    
    


    


   
    def pa_mine(self):
        raise NotImplementedError
