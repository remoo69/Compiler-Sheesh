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
        run.get_context()
        for i,arg in enumerate(self.arguments):
            run.symbol_table.variable(
                name=self.func.parameters[i].id, 
                dtype=self.func.parameters[i].type, 
                scope=run.current_scope
            ).assign("=", arg)
            
        return run.generate_code()