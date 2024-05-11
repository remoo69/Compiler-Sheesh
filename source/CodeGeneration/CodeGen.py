import re
import sys

sys.path.append('.')
from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_handler import RuntimeError
from source.core.error_types import Semantic_Errors as se
from source.CodeGeneration.Functionality.Functionality import Functionality




#TODO - Implement the code generation logic here
#TODO - KUNG
#TODO - EH KUNG
#TODO - DEINS
#TODO - CHOOSE
#TODO - WHEN
#TODO - DEFAULT
#TODO - BET
#TODO - WHILST
#TODO - FOR
#TODO - TO
#TODO - FELLOFF
#TODO - STEP
#TODO - PASS
#TODO - UP
#TODO - PA MINE
#TODO - CONCAT
#TODO - YET
#TODO - BASED
#TODO - DEF



class CodeGenerator:
    """  
    General Code Generator Logic: Traverse all nodes in the AST. Go to respective routines based on the node's root.
    """
    def __init__(self, semantic:SemanticAnalyzer, debugMode) -> None:

        self.debug=debugMode

        self.semantic=semantic
        self.symbol_table=self.semantic.symbol_table
        self.output_stream={}

        self.matched=self.semantic.parse_tree.leaves()

        self.current_node = self.semantic.parse_tree

        self.runtime_errors:list[RuntimeError] = []

        self.previous_node = None # Store the previous node to handle loops
        
        self.functionality=Functionality(self.debug)


        self.routines={

            """  
            Routines act as the entry point for the functions in the program. As such, each routine should contain teir respective
            functionalities. 
            """


            "allowed_in_loop":self.allowed_in_loop,
            "var_or_seq_dec":self.var_or_seq_dec,
            "looping_statement":self.looping_statement,
            "loop_body_statement":self.loop_body_statement,
            "in_loop_body":self.in_loop_body,
            "loop_body":self.loop_body,
            "more_loop_body":self.more_loop_body,
            "control_flow_statement":self.control_flow_statement,
            "statement":self.statement,

        }

        # self.functionality={

        #     "yeet":self.functionality.yeet,
        #     "def":self.functionality.def_,
        #     "based":self.functionality.based,
        #     "up":self.functionality.up,
        #     "pa_mine":self.functionality.pa_mine,
            
            
        #     "pass":self.functionality.pass_,
        #     "kung":self.functionality.kung,
        #     "ehkung":self.functionality.ehkung,
        #     "deins":self.functionality.deins,
        #     "choose":self.functionality.choose,
        #     "when":self.functionality.when,
        #     "default":self.functionality.default,
            
        #     "bet":self.functionality.loops.bet,
        #     "whilst":self.functionality.loops.whilst,
        #     "for":self.functionality.loops.for_loop,
        #     # "to":self.to_loop,
        #     "felloff":self.functionality.felloff,
        #     # "step":self.step,
        #     "pass":self.functionality.pass_,


        #     "...":self.functionality.concat,


        # }
        

    def statement(self):
        pass
    def generate_code(self):
        print("Generating code...")
        while True:
            if self.current_node.root not in self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            else:
                self.routines[self.current_node.root]()
                self.previous_node=self.current_node
                try:
                    self.current_node = self.semantic.parse_tree.traverse(self.current_node)
                except AttributeError:
                    break
            if self.current_node is None:
                break  # Exit the loop if the tree has been fully traversed

    
    

    def loop_body_statement(self):

        # try:
        #     self.functionality[self.current_node.root]()
        #     self.previous_node=self.current_node
        #     self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        # except KeyError:
        try:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines[self.current_node.root]()

        except KeyError:
            if self.previous_node.children[0].type=="kung":
                self.current_node=self.previous_node
                self.functionality[self.current_node.children[0].type]()
            try:
                if self.previous_node.parent.children[-1].root=="more_loop_body":
                    self.previous=self.current_node
                    self.current_node=self.previous_node.parent.children[-1]
                    self.routines["more_loop_body"]()
            except AttributeError:
                pass
            

    def looping_statement(self):
        if self.current_node.children[0].value=="for":
            self.functionality["for"]()

        elif self.current_node.children[0].value=="bet":
            self.functionality["bet"]()

    def var_or_seq_dec(self):
        # try:
            if self.current_node.children[-1].value=="#":
                pass
                # self.eval_arithm()
    def more_loop_body(self):
        try:
            if self.current_node.children[0].root in  self.routines.keys():
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
                self.routines[self.current_node.children[0].root]()
            else:
                self.previous_node=self.current_node
                self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            print("nag key error par")
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body_statement"]()

    def allowed_in_loop(self):

        # try:
        #     if self.current_node.children[0].value in self.functionality.keys():
        #         self.functionality[self.current_node.children[0].value]()
        #         self.previous_node=self.current_node
        #         self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        #     elif self.current_node.children[0].type=="Identifier":

        #         self.assign(self.current_node.children[0])

        #     else:
        #         # raise Exception("Routine not found")
        #         print(f'Functionality {self.current_node.children[0].value} not found')
        #         pass
        # except AttributeError as e:
        #     # print(e)
        #     # print(f"No Functionality for {self.current_node.children[0].root} in {self.current_node.root}")
            
        #     pass

        routines={
            "up":self.functionality.io.up,
        }
        items=self.current_node.leaves()
        if self.current_node.children[0].value in routines:
            routines[self.current_node.children[0].value]()

    def in_loop_body(self):
        try:
            self.functionality[self.current_node.root]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body"]()
            

    def loop_body(self):
        try:
            self.functionality[self.current_node.children[0].children[0].children[0].value]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except AttributeError: 
            self.functionality[self.current_node.children[0]]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
        except KeyError:
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)
            self.routines["loop_body_statement"]()  
            
    def control_flow_statement(self):
        if self.current_node.children[0].value in ["choose", "kung"]:
            self.functionality[self.current_node.children[0].value]()
            self.previous_node=self.current_node
            self.current_node = self.semantic.parse_tree.traverse(self.current_node)




    
    
    







