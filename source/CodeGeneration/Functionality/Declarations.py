
import sys
sys.path.append(".")
from source.core.AST import AST
from source.core.symbol_table import SymbolTable
from source.CodeGeneration.Functionality.Evaluators import Evaluators
import source.core.constants as const
from source.core.error_handler import RuntimeError

from source.core.error_types import Semantic_Errors as se

class Identifier:
    """  
    All identifier-related operations are contained here. Assignments, 
    declarations (already done in the semnatic analyzer), and function invocations are performed here.
    """
    def __init__(self, node:AST, output_stream, symbol_table, current_scope, runtime_errors) -> None:
        self.node=node
        self.leaves=self.node.leaves()
        self.output_stream=output_stream
        self.symbol_table:SymbolTable=symbol_table
        self.current_scope=current_scope
        self.runtime_errors=runtime_errors

    def initialize(self):
        if self.node.root=="var_or_seq_dec":
            id=self.leaves[1].value
            dtype=self.leaves[0].value
            value=Evaluators(self.node.children[0]).evaluate()
            if isinstance(value, const.types[dtype]):
                self.symbol_table.find_var(id,self.current_scope).assign("=", value=value)
            else:
                self.runtime_errors.append(
                    RuntimeError(error=se.VAL_OPERAND_INVALID, token=self.leaves[1], expected=se.expected["VAL_OPERAND_INVALID"] ))

            

    def assignment(self):
        pass

    def function_call(self):
        pass
    
    def sequence(self):
        pass


    def id_tail(self):
        leaves=self.node.leaves()
        if leaves[1].type=="(":
            self.function_call()
        elif leaves[1].type=="=":
            Evaluators(self.leaves, self.runtime_errors, self.current_scope, self.symbol_table).assign(self.node.children[0])
        else:
            pass

    
    


class Expression:
    """ All expressions are contained here. Expression evaluations, and operations are performed here."""
    def __init__(self, node) -> None:
        self.node=node

    def evaluate(self):
        pass