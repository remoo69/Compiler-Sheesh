import sys
sys.path.append('.')
from source.core.symbol_table import Token
from source.core.error_handler import SyntaxError as Error
from time import perf_counter
from collections import deque
from source.core.AST import AST

class SyntaxAnalyzer:

    
    def __init__(self, tokens:list[Token], debugMode=False) -> None:

        

        self.tokens:list[Token]=tokens
        self.Tree = AST("Root")
        self.buffer = deque([])
        self.syntax_errors =[]
        self.success = "Success"
        self.expected = None
        self.isnullable = True
        self.expectset = []

        self.cur=None

        self.req_type=None
        self.matched=[]

        self.semantic=None
        
        
        if debugMode:
            self.debug=True
            self.debug_fail=True
            self.tree_debug=True
            self.status_report=True
        else:
            #Mode 1
            # self.debug=False
            # self.debug_fail=False
            # self.tree_debug=True
            # self.status_report=False

            self.debug=False
            self.debug_fail=False
            self.tree_debug=False
            self.status_report=False

    

        


# region WRAPPERS
    def require(func):
        def wrapper2(self, *args, **kwargs):
            self.isnullable = False
            result = func(self, *args, **kwargs)
            # self.isnullable=True
            if result is None:
                self.enforce()
                self.failed()
            else:
                return result
        return wrapper2
    
    def nullable(func):
        def wrapper(self, *args, **kwargs):
            self.isnullable = True
            result = func(self, *args, **kwargs)
            if result is None:
                return
            else:
                return result

        return wrapper

# endregion WRAPPERS______________________________________________________

# region FUNCTIONS________________________________________________________

    def reset(self):
        self.Tree = AST("Root")
        self.buffer = deque([])
        self.syntax_errors = []
        self.success = "Success"
        self.expected = None
        self.isnullable = True
        self.expectset = []

        self.cur=None

        self.req_type=None
        self.matched=[]

        self.semantic=None

        # self.semantic=semantic(self.matched)

    def parse(self):
        print("Parsing...")
        self.reset()
        if len(self.tokens) == 0:
            self.syntax_errors.append(
                "No Tokens to Syntactically Analyze. Please Input Code.")
            return self.syntax_errors
        else:
            try:
                if self.status_report:
                    start=perf_counter()

                    self.program()
                    
                    end=perf_counter() 
                    
                    self.Tree.end_tree()   

                    tr=perf_counter()
                    print(f"Parsing: {end-start}")
                    print(f"Print Tree: {tr-end}")
                else:
                    self.program()
                    self.Tree.end_tree() 
                if self.tree_debug:
                    print(self.Tree)

                # self.semantic=semantic(self.Tree)
                # self.semantic.analyze()
                # self.Tree.visualize()


                # print(f"IDs:{self.semantic.id_vars}\n\nFUNCs:{self.semantic.id_funcs}")
                # return self.syntax_errors, self.semantic.semantic_errors
            except SyntaxError as e:
                print(e) if self.debug else None
            # self.semantic=semantic(self.Tree)
            # self.semantic.analyze()

            return

    
    def enforce(self):
        self.isnullable = False

    def peek(self, chars_ahead=0):
        if len(self.tokens) > chars_ahead:
            try:
                return self.tokens[0 + chars_ahead].type
            except IndexError:
                return None
        else:
            return None

    def see(self, consumable):
        toklen = len(self.tokens)
        if (toklen != 0) and (self.tokens[0].type == consumable):
            return consumable
            # print(self.tokens)
        else:
            return None

    def consume(self, consumable):
        toklen = len(self.tokens)
        if (toklen != 0) and (self.tokens[0].type == consumable):
            self.buffer.append(consumable)
            self.tokens.pop(0)
            return consumable

        else:
            return None
        
    def stop(self):
        raise SyntaxError("Syntax Error")


    def error(self):
        if len(self.tokens) <= 0:
            self.expectset = list(set(self.expectset))
            self.syntax_errors.append(
                Error(
                    expected=self.expectset,
                    unexpected="EOF",
                    value="EOF",
                    line="EOF",
                    toknum=0))
            self.stop()
            return "EOF"
        else:
            self.expectset = list(set(self.expectset))
            self.syntax_errors.append(
                Error(
                    expected=self.expectset,
                    unexpected=self.tokens[0].type,
                    value=self.tokens[0].value,
                    line=self.tokens[0].line,
                    toknum=self.tokens[0].position))
            self.stop()

    def failed(self, require=False):
        if require:
            self.isnullable=False
            
        if self.isnullable:
            self.Tree.end_branch()
            return
        else:
            self.Tree.end_branch()
            if self.error() == "EOF":
                return


    def eat_endl(self):
        if self.peek() == "Newline":
            self.consume("Newline")

    
    def match(self, consumable, skippable=False, newline_Optional=True):
        try:
            self.cur=self.tokens[0]
        except IndexError:
            pass
        if len(self.buffer) >= 1 and self.buffer[-1] == "Newline":
            while self.peek() == "Newline":
                self.consume("Newline")
                
        self.expected = consumable

        if len(self.tokens) == 0:
            self.expectset.append(self.expected)
            print(f"EOF, nothing to match {consumable} with.") if self.debug_fail else None
            self.failed()
            # self.Tree.end_branch()
            self.expected = None
            
            return False
        
        consumed = self.see(consumable)

        if consumed is None: 
            if not skippable :
                self.enforce()

                if self.debug_fail:
                    try:
                        print(
                            f"Failed Match: {self.expected} FROM {self.Tree.current_func()}, got {self.tokens[0].type}")
                    except IndexError:
                        print(f"Failed Match: {self.expected} FROM {self.Tree.current_func()}, got EOF")
                self.expectset.append(self.expected)
                self.expected = None
                self.failed()
                return False
            else:
                print(f"No {self.expected} FROM {self.Tree.current_func()} detected. Skipping.") if self.debug_fail else None
                self.expectset.append(self.expected)
                self.expected = None
                return
        else:
            self.matched.append(self.tokens[0])
            self.consume(self.expected)
            
            self.expected = None
            self.expectset = []
            print("Matched:", consumed, "FROM ", self.Tree.current_func()) if self.debug else None
            if consumed == "#":
                if self.peek() == "}":
                    self.Tree.add_children(self.matched[-1])
                    return True
                self.match("Newline")
                self.matched.pop(-1)
                self.Tree.add_children(self.matched[-1])
                
                
                self.eat_endl()
                return True
            else:
                self.Tree.add_children(self.matched[-1])
                return True



# endregion FUNCTIONS_____________________________________________________

# region GRAMMAR_________________________________________________________________________________________________________________

# MAIN_____________________________________________________________________________________________________________________
    def program(self):
        self.Tree.initialize_new()

        self.eat_endl()
        self.import_()
        self.global_declaration()
        self.function_definition()
        self.sheesh_declaration()
        self.function_definition()
        self.eat_endl()

        self.isnullable = False
        if self.tokens == []:
            self.Tree.end_branch()
            return self.success
        else:
            print("FAILED")
            return self.failed()

# IMPORTS_________________________________________________________________________________________________________________
    # I didn't change anything here since alaws naman change sa implementation
    # kahit meron sa cfg

#region non-decl
    @nullable
    def import_(self):
        self.Tree.initialize_new()
        if self.match('use', True):
            self.import_prog()
            self.match("#")
            self.more_import()
            self.Tree.end_branch()
            return self.success
        else:
            self.failed()
    
    @nullable
    def more_import(self):
        self.Tree.initialize_new()
        if self.import_():
            self.Tree.end_branch()
            return self.success
        else:
            return self.failed()

    def import_prog(self):
        self.Tree.initialize_new()
        if self.match("Identifier", True):
            self.func_paren(); self.import_tail()
            self.Tree.end_branch()
            return self.success
        else:
            return self.failed()

    @nullable
    def import_tail(self):
        self.Tree.initialize_new()
        if self.more_importprog() == self.success:
            self.Tree.end_branch()
            return self.success
        elif self.match("from", True):
            self.enforce()
            self.match("Identifier")
            self.Tree.end_branch()
            return self.success
        else:
            return self.failed()
    @nullable
    def func_paren(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.enforce
            if self.match(")"):
                self.Tree.end_branch()
                return self.success
            else:
                return self.failed()
        else:
            return self.failed()

    def more_importprog(self):
        self.Tree.initialize_new()

        if self.match(",", True):
            self.import_prog()
            self.Tree.end_branch()
            return self.success
        else:
            return self.failed()
        
    @nullable
    def global_declaration(self):
        self.Tree.initialize_new()
        if self.global_statement()==self.success:
            self.more_globaldec()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_globaldec(self):
        self.Tree.initialize_new()
        if self.global_declaration()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def global_statement(self):
        self.Tree.initialize_new()
        if self.var_or_seq_dec() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.constant_declaration() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def parameter(self):
        self.Tree.initialize_new()
        if self.match("blank", True):
            self.Tree.end_branch(); return self.success
        elif self.in_param() == self.success:
            self.Tree.end_branch(); return self.success

        else:
            return self.failed()

    def in_param(self):
        self.Tree.initialize_new()
        if self.match("charr", True):
            self.enforce()
            self.match("text")
            self.match("Identifier")
            self.more_paramtail()
            self.Tree.end_branch(); return self.success
        elif self.seq_dtype() == self.success:
            self.enforce()
            self.match("Identifier")
            self.index_param()
            self.more_paramtail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_param(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.enforce()
            self.in_param()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_paramtail(self):
        self.Tree.initialize_new()
        if self.more_param() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def two_d_param(self):
        self.Tree.initialize_new()
        if self.match("[", True):
            self.match("Whole")
            self.match("]")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def index_param(self):
        self.Tree.initialize_new()
        if self.match("[", True):
            self.enforce()
            # self.match("Whole") #NOTE - HUH?
            self.match("]")
            self.two_d_param()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def seq_dtype(self):
        self.Tree.initialize_new()
        dtypes = ["whole", "dec", "text", "sus"]
        ltypes = ["Whole", "Dec", "Text", "Sus"]
        for i, type in enumerate(dtypes):
            if self.match(type, True):
                self.req_type = ltypes[i]
                self.Tree.end_branch(); return self.success
            
    def yeet_type(self): 
        self.Tree.initialize_new()
        if self.match("blank", True) or self.seq_dtype() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("charr", True):
            self.enforce()
            self.match("text")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def numeric_value(self):
        self.Tree.initialize_new()
        if self.match("Whole", True) or self.match("Dec", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
#ANCHOR - Main Function
    @require
    def sheesh_declaration(self):
        self.Tree.initialize_new()
        if self.match('sheesh'):
            self.enforce()
            self.match('(')
            self.match(')')
            self.eat_endl()
            if self.reg_body() == self.success: 
                self.Tree.end_branch(); return self.success
            else: return self.failed()
        else:
            return self.failed()

    def statement(self):
        self.Tree.initialize_new()
        if self.single_statement() == self.success:
            self.more_statement()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def single_statement(self, is_required = False):
        self.Tree.initialize_new()
        if self.allowed_in_loop() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.control_flow_statement() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            if is_required:
                self.isnullable=False
                return self.failed()    
            return self.failed()

    @nullable
    def allowed_in_loop(self):
        self.Tree.initialize_new()
        if (self.var_or_seq_dec() == self.success) or (self.looping_statement() == self.success) or (self.yeet_statement() == self.success):
            self.Tree.end_branch(); return self.success
        elif self.match("Identifier", True):

            self.id_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("up", True):
            self.enforce()
            self.match("(")
            if self.up_argument():
                self.match(")")
                self.match("#")
                self.Tree.end_branch(); return self.success 
        else:
            return self.failed()

    def id_tail(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.func_argument()
            self.match(")")
            self.match("#")
            self.Tree.end_branch(); return self.success
        elif self.one_dim() == self.success:
            self.enforce()
            self.id_next_tail()
            self.match("#")
            self.Tree.end_branch(); return self.success
        elif self.id_next_tail() == self.success:
            self.enforce()
            self.match("#")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def id_next_tail(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.assign_value()
            self.enforce()
            self.Tree.end_branch(); return self.success
        elif self.assign_op() == self.success:
            self.enforce()
            self.literal_or_expr()
            self.enforce()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_statement(self):
        self.Tree.initialize_new()
        if self.statement() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def up_argument(self):
        self.Tree.initialize_new()
        if self.match("Text"):
            self.next_args()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def next_args(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.literal_or_expr(True)
            self.more_up_args()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def more_up_args(self):
        self.Tree.initialize_new()
        if self.next_args() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
         
    def reg_body(self):
        self.Tree.initialize_new()
        self.eat_endl()
        if self.match("{", True): #NOTE - Might be error cause
            self.eat_endl()
            self.single_statement(is_required = True)
            self.more_statement()
            self.eat_endl()
            self.enforce()
            self.match("}")
            self.eat_endl()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def in_loop_body(self):
        self.Tree.initialize_new()
        self.eat_endl()
        if self.match("{", True): #NOTE - Might be error cause
            self.eat_endl()
            self.loop_body()
            self.eat_endl()
            self.match("}")
            self.eat_endl()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#endregion non-decl

    def var_or_seq_dec(self):
        self.Tree.initialize_new()  
        if self.match("whole", True):
            self.match("Identifier")
            self.w_var_seq_tail()
            self.match("#")
            self.Tree.end_branch(); return self.success
        
        elif self.match("dec", True):
            self.match("Identifier")
            self.d_var_seq_tail()
            self.match("#")

            self.Tree.end_branch(); return self.success
        
        elif self.match("sus", True):
            self.match("Identifier")


            self.s_var_seq_tail()

            self.match("#")

            self.Tree.end_branch(); return self.success
        
        elif self.match("text", True):
            self.match("Identifier")

            self.t_var_seq_tail()

            self.match("#")

            self.Tree.end_branch(); return self.success
        
        elif self.match("charr", True):
            self.match("text")
            self.match("Identifier")


            self.c_vardec_tail()

            self.match("#")

            self.Tree.end_branch(); return self.success
        
        else:
            return self.failed()

#ANCHOR - whole vardec
    def w_var_seq_tail(self):
        self.Tree.initialize_new()
        if self.w_vardec_tail() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.index()== self.success:

            # sa.id_as_sequence(self.matched[-1])

            self.w_seq_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def w_vardec_tail(self):
        self.Tree.initialize_new()
        # if self.one_dim()==self.success:
        #     self.more_whl_var()
        #     self.Tree.end_branch();return self.success
        if self.w_val_assign()==self.success:
            self.more_whl_var()
            self.Tree.end_branch();return self.success 
        elif self.more_whl_var()==self.success: #NOTE - added this
            self.Tree.end_branch();return self.success
        else:
            return self.failed()
    
    @nullable
    def w_val_assign(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            if self.whl_all_value()==self.success:
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    @nullable
    def more_whl_var(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")

            # self.new_id_more()

            self.w_vardec_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def whl_all_value(self):
        self.Tree.initialize_new()
        if self.whl_value()==self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("pa_mine", True):
            self.match("(")
            if self.match("Text") and '$w' in self.cur.value: #REVIEW - this might cause issue
                self.match(")")
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    def  whl_value(self, required = False):
        self.Tree.initialize_new() 
        if self.match("Whole", True):
            self.whl_op()
            self.Tree.end_branch(); return self.success
        elif self.id_as_val()==self.success:
            self.whl_op()
            self.Tree.end_branch(); return self.success
        elif self.whl_val_withparen()==self.success:
            self.whl_op()
            self.Tree.end_branch(); return self.success
        else:
            if required:
                self.isnullable = False
                return self.failed()
            return self.failed()

    def whl_val_withparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.whl_value()
            self.enforce()
            self.match(")")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def whl_op(self):
        self.Tree.initialize_new()
        if self.math_op()==self.success:
            self.whl_value()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable  
    def w_seq_tail(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.w_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index()==self.success:
            self.w_seq_tail_next()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def w_seq_tail_next(self):
        self.Tree.initialize_new()
        if self.w_const_dimtail2()==self.success or self.more_whl_var()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def w_seq_init(self):
        self.Tree.initialize_new()
        if self.match("{", True): #NOTE - Might be error cause
            self.w_elem_init()
            self.enforce()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def w_elem_init(self):
        self.Tree.initialize_new()
        if self.match("Whole", True):
            self.next_whl_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def w_two_d_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.w_seq_init()
            self.w_more_two_d()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def w_more_two_d(self):
        self.Tree.initialize_new()
        if self.w_two_d_init()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def next_whl_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.w_elem_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
#ANCHOR - dec var dec

    def d_var_seq_tail(self):
        self.Tree.initialize_new()
        if self.d_vardec_tail() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.index()== self.success:

            # sa.id_as_sequence(self.matched[-1])

            self.d_seq_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def d_vardec_tail(self):
        self.Tree.initialize_new()
        # if self.one_dim()==self.success:
        #     self.more_dec_var()
        #     self.Tree.end_branch();return self.success
        if self.d_val_assign()==self.success:
            self.more_dec_var()
            self.Tree.end_branch();return self.success  
        elif self.more_dec_var()==self.success: #NOTE - added this
            self.Tree.end_branch();return self.success
        else:
            return self.failed()
    
    @nullable
    def d_val_assign(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            if self.dec_all_value()==self.success:
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    @nullable
    def more_dec_var(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            
            # self.new_id_more()

            self.d_vardec_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def dec_all_value(self):
        self.Tree.initialize_new()
        if self.dec_value()==self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("pa_mine", True):
            self.match("(")
            if self.match("Text") and '$d' in self.cur.value: #REVIEW - this might cause issue
                self.match(")")
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    def  dec_value(self):
        self.Tree.initialize_new() 
        if self.match("Dec", True):
            self.dec_op()
            self.Tree.end_branch(); return self.success
        elif self.id_as_val()==self.success:
            self.dec_op()
            self.Tree.end_branch(); return self.success
        elif self.dec_val_withparen()==self.success:
            self.dec_op()
            self.Tree.end_branch(); return self.success
        else: return self.failed()

    def dec_val_withparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.dec_value()
            self.match(")")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def dec_op(self):
        self.Tree.initialize_new()
        if self.math_op()==self.success:
            self.dec_value()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable  
    def d_seq_tail(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.d_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index()==self.success:
            self.d_seq_tail_next()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def d_seq_tail_next(self):
        self.Tree.initialize_new()
        if self.d_const_dimtail2()==self.success or self.more_dec_var()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def d_seq_init(self):
        self.Tree.initialize_new()
        if self.match("{", True): #NOTE - Might be error cause
            self.d_elem_init()
            self.enforce()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def d_elem_init(self):
        self.Tree.initialize_new()
        if self.match("Dec", True):
            self.next_dec_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def d_two_d_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.d_seq_init()
            self.d_more_two_d()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def d_more_two_d(self):
        self.Tree.initialize_new()
        if self.d_two_d_init()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def next_dec_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.d_elem_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#ANCHOR - SUS var dec
    def s_var_seq_tail(self):
        self.Tree.initialize_new()
        if self.s_vardec_tail() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.index()== self.success:

            # sa.id_as_sequence(self.matched[-1])

            self.s_seq_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def s_vardec_tail(self):
        self.Tree.initialize_new()
        # if self.one_dim()==self.success:
        #     self.more_sus_var()
        #     self.Tree.end_branch();return self.success
        if self.s_val_assign()==self.success:
            self.more_sus_var()
            self.Tree.end_branch();return self.success  
        elif self.more_sus_var()==self.success: #NOTE - added this
            self.Tree.end_branch();return self.success
        else:
            return self.failed()
    
    @nullable
    def s_val_assign(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            if self.logic_value()==self.success:
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    @nullable
    def more_sus_var(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")

            # self.new_id_more()

            self.s_vardec_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def sus_all_value(self):
        self.Tree.initialize_new()
        if self.logic_value()==self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("pa_mine", True):
            self.match("(")
            if self.match("Text") and '$s' in self.cur.value: #REVIEW - this might cause issue
                self.match(")")
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    

    @nullable  
    def s_seq_tail(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.match("{")
            self.s_elem_init()
            self.match("}")
            self.Tree.end_branch(); return self.success
        elif self.index()==self.success:
            self.s_seq_tail_next()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def s_seq_tail_next(self):
        self.Tree.initialize_new()
        if self.s_const_dimtail2()==self.success or self.more_sus_var()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def s_seq_init(self):
        self.Tree.initialize_new()
        if self.match("{", True): #NOTE - Might be error cause
            self.s_elem_init()
            self.enforce()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def s_elem_init(self):
        self.Tree.initialize_new()
        if self.match("Sus", True):
            self.next_sus_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def s_two_d_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.s_seq_init()
            self.s_more_two_d()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def s_more_two_d(self):
        self.Tree.initialize_new()
        if self.s_two_d_init()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def next_sus_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.s_elem_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#ANCHOR - text var dec

    def t_var_seq_tail(self):
        self.Tree.initialize_new()
        if self.t_vardec_tail() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.index()== self.success:
            self.t_seq_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def t_vardec_tail(self):
        self.Tree.initialize_new()
        # if self.one_dim()==self.success:
        #     self.more_txt_var()
        #     self.Tree.end_branch();return self.success
        if self.t_val_assign()==self.success:
            self.more_txt_var()
            self.Tree.end_branch();return self.success  
        elif self.more_txt_var()==self.success: #NOTE - added this
            self.Tree.end_branch();return self.success
        else:
            return self.failed()
    
    @nullable
    def t_val_assign(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            if self.txt_all_value()==self.success:
                self.Tree.end_branch()
                return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    @nullable
    def more_txt_var(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.t_vardec_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def txt_all_value(self):
        self.Tree.initialize_new()
        if self.txt_value()==self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("pa_mine", True):
            self.match("(")
            if self.match("Text") and '$t' in self.cur.value: #REVIEW - this might cause issue
                self.match(")")
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    def  txt_value(self):
        self.Tree.initialize_new() 
        if self.match("Text", True):
            self.txt_op()
            self.Tree.end_branch(); return self.success
        elif self.id_as_val()==self.success:
            self.txt_op()
            self.Tree.end_branch(); return self.success
        elif self.txt_val_withparen()==self.success:
            self.txt_op()
            self.Tree.end_branch(); return self.success
        else: return self.failed()

    def txt_val_withparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.txt_value()
            self.match(")")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def txt_op(self):
        self.Tree.initialize_new()
        if self.match("...", True):
            self.txt_value()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable  
    def t_seq_tail(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.t_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index()==self.success:
            self.t_seq_tail_next()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def t_seq_tail_next(self):
        self.Tree.initialize_new()
        if self.t_const_dimtail2()==self.success or self.more_txt_var()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def t_seq_init(self):
        self.Tree.initialize_new()
        if self.match("{", True): #NOTE - Might be error cause
            self.t_elem_init()
            self.enforce()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def t_elem_init(self):
        self.Tree.initialize_new()
        if self.match("Text", True):
            self.next_txt_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def t_two_d_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.t_seq_init()
            self.t_more_two_d()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def t_more_two_d(self):
        self.Tree.initialize_new()
        if self.t_two_d_init()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def next_txt_init(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.t_elem_init()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#LINK - charr var dec
    
    @nullable
    def c_vardec_tail(self):
        self.Tree.initialize_new()
        if self.c_val_assign()==self.success:
            self.more_chr_var()
            self.Tree.end_branch();return self.success  
        elif self.more_chr_var()==self.success: #NOTE - added this
            self.Tree.end_branch();return self.success
        else:
            return self.failed()
    
    @nullable
    def c_val_assign(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            if self.charr_all_value()==self.success:
                self.Tree.end_branch()
                return self.success
            else:
                return self.failed()
        else:
            return self.failed()
    
    @nullable
    def more_chr_var(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.c_vardec_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def charr_all_value(self):
        self.Tree.initialize_new()
        if self.match("pa_mine", True):
            self.match("(")
            if self.match("Text") and '$c' in self.cur.value: #REVIEW - this might cause issue
                self.match(")")
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
        elif self.charr_value()==self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def  charr_value(self):
        self.Tree.initialize_new() 
        if self.match("Charr", True):
            self.Tree.end_branch(); return self.success
        elif self.match("Identifier", True):
            self.func_call()
            self.Tree.end_branch(); return self.success
        elif self.match("(", True):
            self.enforce()
            self.match("Charr")
            self.match(")")
            self.Tree.end_branch(); return self.success
        else: return self.failed()

#endregion

#ANCHOR - OtHERS

    @nullable
    def func_call(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.func_argument()
            self.match(")")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def one_dim(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.two_dim()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def two_dim(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def index(self):
        self.Tree.initialize_new()
        if self.match("[", True):
            self.enforce()
            self.whl_value(required = True)
            self.enforce()
            self.match("]")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def constant_declaration(self):
        self.Tree.initialize_new()
        if self.match("based", True):
            self.const_type()
            self.match("#")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def const_type(self):
        self.Tree.initialize_new()
        if self.match("whole", True):
            self.match("Identifier")
            self.w_const_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("dec", True):
            self.match("Identifier")
            self.d_const_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("sus", True):
            self.match("Identifier")
            self.s_const_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("text", True):
            self.match("Identifier")
            self.t_const_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("charr", True):
            self.match("text")
            self.match("Identifier")
            self.c_const_var_tail()
            self.enforce()
            # self.match("#")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
#region var const
#ANCHOR - whole
    def w_const_tail(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.enforce()
            self.w_const_dimtail1()
            self.Tree.end_branch(); return self.success
        elif self.w_const_var_tail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def w_const_dimtail1(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.w_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index() == self.success:
            self.w_const_dimtail2()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def w_const_dimtail2(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.match("{")
            self.w_seq_init()
            self.w_two_d_init()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def w_const_var_tail(self):
        self.Tree.initialize_new()
        if self.match("="):
            self.whl_value()
            self.more_whl_const()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable   
    def more_whl_const(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.w_const_var_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
#ANCHOR - dec
    def d_const_tail(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.enforce()
            self.d_const_dimtail1()
            self.Tree.end_branch(); return self.success
        elif self.d_const_var_tail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def d_const_dimtail1(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.d_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index() == self.success:
            self.d_const_dimtail2()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def d_const_dimtail2(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.match("{")
            self.d_seq_init()
            self.d_two_d_init()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def d_const_var_tail(self):
        self.Tree.initialize_new()
        if self.match("="):
            self.dec_value()
            self.more_dec_const()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable   
    def more_dec_const(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.d_const_var_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
#ANCHOR - sus

    def s_const_tail(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.enforce()
            self.s_const_dimtail1()
            self.Tree.end_branch(); return self.success
        elif self.s_const_var_tail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def s_const_dimtail1(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.s_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index() == self.success:
            self.s_const_dimtail2()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def s_const_dimtail2(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.match("{")
            self.s_seq_init()
            self.s_two_d_init()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def s_const_var_tail(self):
        self.Tree.initialize_new()
        if self.match("="):
            self.logic_value()
            self.more_sus_const()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable   
    def more_sus_const(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.s_const_var_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
#ANCHOR - text


    def t_const_tail(self):
        self.Tree.initialize_new()
        if self.index() == self.success:
            self.enforce()
            self.t_const_dimtail1()
            self.Tree.end_branch(); return self.success
        elif self.t_const_var_tail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def t_const_dimtail1(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.t_seq_init()
            self.Tree.end_branch(); return self.success
        elif self.index() == self.success:
            self.t_const_dimtail2()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def t_const_dimtail2(self):
        self.Tree.initialize_new()
        if self.match("=", True):
            self.enforce()
            self.match("{")
            self.t_seq_init()
            self.t_two_d_init()
            self.match("}")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def t_const_var_tail(self):
        self.Tree.initialize_new()
        if self.match("="):
            self.txt_value()
            self.more_txt_const()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable   
    def more_txt_const(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.t_const_var_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#ANCHOR - charr

    def c_const_var_tail(self):
        self.Tree.initialize_new()
        if self.match("="):
            self.charr_value()
            self.more_chr_const()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def more_chr_const(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.match("Identifier")
            self.c_const_var_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
#endregion

    def assign_op(self):
        self.Tree.initialize_new()  # issue
        aops = ["=", "+=", "-=", "*=", "/=", "%="]
        for op in aops:
            if self.match(op, True):
                self.Tree.end_branch(); return self.success
        return self.failed()


    @nullable
    def func_argument(self):
        self.Tree.initialize_new()
        if self.argument() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def argument(self):
        self.Tree.initialize_new()
        if self.literal_or_expr() == self.success:
            self.more_args()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_args(self):
        self.Tree.initialize_new()
        if self.match(",", True):
            self.argument()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

#region control flow
    def control_flow_statement(self):
        self.Tree.initialize_new()
        if self.match("kung", True):
            self.enforce()
            self.match("(")
            self.condition()
            self.enforce()
            self.match(")")
            self.reg_body()
            self.cond_tail()
            self.Tree.end_branch(); return self.success
        elif self.match("choose", True):
            self.match("(")
            self.match("Identifier")
            self.match(")")
            self.eat_endl()
            self.match("{")
            self.eat_endl()
            self.when_statement()
            self.choose_default()
            self.eat_endl()
            self.match("}")
            self.eat_endl()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def ehkung_statement(self):
        self.Tree.initialize_new()
        if self.match("ehkung", True):
            self.enforce()
            self.match("(")
            self.condition()
            self.enforce()
            self.match(")")
            self.reg_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def cond_tail(self):
        self.Tree.initialize_new()
        if self.ehkung_statement() == self.success:
            self.more_condtail()
            self.Tree.end_branch(); return self.success
        elif self.match("deins", True):
            self.enforce()
            self.reg_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def more_condtail(self):
        self.Tree.initialize_new()
        if self.cond_tail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def when_statement(self):
        self.Tree.initialize_new()
        if self.match("when", True):
            self.when_literal()
            self.match("::")

            self.eat_endl()

            if self.statement_for_choose() == self.success:
                self.more_when()
            else:
                self.enforce()
                return self.failed()
            
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def when_literal(self):
        self.Tree.initialize_new()
        if self.match("Whole", True) or self.match("Charr", True): 
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def statement_for_choose(self):
        self.Tree.initialize_new()
        if self.single_statement() == self.success:
            self.more_stmt_choose()
            self.Tree.end_branch(); return self.success
        elif self.match("felloff", True):
            self.enforce()
            self.match("#")
            self.Tree.end_branch(); return self.success
        else:
            self.enforce
            return self.failed()

    @nullable
    def more_stmt_choose(self):
        self.Tree.initialize_new()
        if self.statement_for_choose() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_when(self):
        self.Tree.initialize_new()
        if self.when_statement() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def choose_default(self):
        self.Tree.initialize_new()
        if self.match("default", True):
            self.match("::")

            self.eat_endl()

            self.statement_for_choose()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def looping_statement(self):
        self.Tree.initialize_new()
        if self.match("bet", True):
            self.enforce()
            self.in_loop_body()
            self.match("whilst")
            self.match("(")
            self.condition()
            self.enforce()
            self.match(")")
            self.match("#")
            self.Tree.end_branch(); return self.success
        elif self.match("for", True):
            self.enforce()
            self.match("(")
            self.match("whole")
            self.match("Identifier")
            self.match("=")
            self.whl_value()
            self.enforce()
            self.match("to")
            self.whl_value()
            self.step_statement()
            self.enforce()
            self.match(")")
            self.in_loop_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def step_statement(self):
        self.Tree.initialize_new()
        if self.match("step", True):
            self.enforce()
            self.whl_value()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def loop_body(self):
        self.Tree.initialize_new()
        if self.loop_body_statement() == self.success:
            self.more_loop_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def loop_body_statement(self):
        self.Tree.initialize_new()
        if (self.allowed_in_loop() == self.success):
            self.Tree.end_branch(); return self.success
        elif self.match("felloff", True):
            self.enforce()
            self.match("#")
            self.Tree.end_branch(); return self.success
        elif self.match("pass", True):
            self.enforce()
            self.match("#")
            self.Tree.end_branch(); return self.success
        elif self.match("kung", True):
            self.enforce()
            self.match("(")
            self.condition()
            self.enforce()
            self.match(")")
            self.in_loop_body()
            self.in_loop_condtail()
            self.Tree.end_branch(); return self.success
        elif self.match("choose", True):
            self.match("(")
            self.match("Identifier")
            self.match(")")
            self.eat_endl()
            self.match("{")
            self.eat_endl()
            self.loop_when()
            self.loop_default()
            self.eat_endl()
            self.match("}")
            self.eat_endl()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def more_loop_body(self):
        self.Tree.initialize_new()
        if self.loop_body() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def loop_ehkung(self):
        self.Tree.initialize_new()
        if self.match("ehkung", True):
            self.enforce()
            self.match("(")
            self.condition()
            self.enforce()
            self.match(")")
            self.in_loop_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def in_loop_condtail(self):
        self.Tree.initialize_new()
        if self.loop_ehkung() == self.success:
            self.more_inloop_condtail()
            self.Tree.end_branch(); return self.success
        elif self.match("deins", True):
            self.enforce()
            self.in_loop_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def more_inloop_condtail(self):
        self.Tree.initialize_new()
        if self.in_loop_condtail() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def loop_when(self):
        self.Tree.initialize_new()
        if self.match("when", True):
            self.when_literal()
            self.enforce()
            self.match("::")

            self.eat_endl()
            
            self.loop_body()
            self.in_loop_when()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def in_loop_when(self):
        self.Tree.initialize_new()
        if self.loop_when() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def loop_default(self):
        self.Tree.initialize_new()
        if self.match("default", True):
            self.enforce()
            self.match("::")

            self.eat_endl()

            self.loop_body()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def yeet_statement(self):
        self.Tree.initialize_new()
        if self.match("yeet", True):
            self.return_val()
            self.enforce()
            self.match("#")
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def return_val(self):
        self.Tree.initialize_new()
        if self.literal_or_expr() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def function_definition(self):
        self.Tree.initialize_new()
        if self.func_def() == self.success:
            self.more_funcdef()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def func_def(self):
        self.Tree.initialize_new()
        if self.match("def", True):
            self.enforce()
            self.yeet_type()
            self.enforce()
            self.match("Identifier")

            # sa.id_funcdef(self.matched[-1], self.matched[-2].value)

            self.match("(")
            self.parameter()
            self.match(")")
            self.func_def_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def func_def_tail(self):
        self.Tree.initialize_new()
        if self.reg_body() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("#", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def more_funcdef(self):
        self.Tree.initialize_new()
        if self.function_definition() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    @nullable
    def id_as_val(self):
        self.Tree.initialize_new()
        if self.match("Identifier", True):
            self.id_val_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def id_val_tail(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.func_argument()
            self.match(")")
            self.Tree.end_branch(); return self.success
        elif self.one_dim() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def assign_value(self):
            self.Tree.initialize_new()
            if self.match("pa_mine", True):
                self.enforce()
                self.match("(")
                self.match("Text")
                self.match(")")
                self.Tree.end_branch(); return self.success
            elif self.literal_or_expr() == self.success:
                self.Tree.end_branch(); return self.success
            else:
                self.enforce()
                return self.failed()


#FIXME - fix this

    def literal_or_expr(self, required=False):
        self.Tree.initialize_new()
        if self.id_as_val() == self.success:
            if self.num_math_op() == self.success:
                if self.relop() == self.success:
                    self.enforce()
                    self.rel_val()
                    self.logic_expr()
                    self.Tree.end_branch(); return self.success
                self.Tree.end_branch(); return self.success
            elif self.rel_expr() == self.success:
                self.Tree.end_branch(); return self.success
            elif self.txt_op() == self.success:
                self.Tree.end_branch(); return self.success
            elif self.logic_expr() == self.success:
                self.Tree.end_branch(); return self.success
            self.Tree.end_branch(); return self.success
        elif self.match("Whole", True) or self.match("Dec", True):
            self.num_math_op()
            self.rel_expr()
            self.Tree.end_branch(); return self.success
        # elif self.literal_logicval() == self.success:
        #     self.Tree.end_branch(); return self.success
        elif self.match("Sus", True):
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        elif self.match("Text", True):
            self.txt_op()
            self.Tree.end_branch(); return self.success
        elif self.match("Charr", True):        
            self.charr_op_tail()
            self.Tree.end_branch(); return self.success
        elif self.l_expr_withparen() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            if required:
                self.enforce()
            return self.failed()
        
    def l_expr_withparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            if self.match("Whole", True) or self.match("Dec", True) == self.success:
                self.num_math_op()
                if self.rel_expr() == self.success:
                    self.match(")")
                    self.logic_expr()
                    self.Tree.end_branch(); return self.success
                self.match(")")
                self.num_math_op()
                self.rel_expr()
                self.Tree.end_branch(); return self.success
            elif self.match("Charr", True):
                if self.charr_op_tail() == self.success:
                    self.match(")")
                    self.logic_expr()
                    self.Tree.end_branch(); return self.success
                self.match(")")
                self.charr_op_tail()
                self.Tree.end_branch(); return self.success
            elif self.match("Text", True):
                self.txt_op()
                self.match(")")
                self.txt_op()
                self.Tree.end_branch(); return self.success
            elif self.match("Sus", True):
                self.logic_expr()
                self.match(")")
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.id_as_val() == self.success:
                self.id_val_next()
                self.match(")")
                self.id_val_next()
                self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def id_val_next(self):
        if self.num_math_op() == self.success:
            if self.relop() == self.success:
                self.enforce()
                self.rel_val()
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.rel_expr() == self.success:
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.txt_op() == self.success:
                self.txt_op()
                self.Tree.end_branch(); return self.success
            elif self.logic_expr() == self.success:
                self.logic_expr()
                self.Tree.end_branch(); return self.success
        elif self.relop() == self.success:
            self.enforce()
            self.rel_val()
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        elif self.txt_op() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.logic_expr() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def charr_op_tail(self):
        self.Tree.initialize_new()
        if self.charr_op() == self.success:
            self.charr_value()
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    

    def condition(self):
        self.Tree.initialize_new()
        if self.logic_value() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            self.enforce()
            return self.failed()

    def id_val_op(self):
        self.Tree.initialize_new()
        if self.id_as_val() == self.success:
            # if self.matched[-1].dtype != self.req_type:
            #     self.semantic_error(se.VAR_OPERAND_INVALID, self.matched[-1], self.req_type)
            self.id_val_tail()
            self.id_expr_tail()
            self.Tree.end_branch(); return self.success
        
        #STUB - removed?
        # elif self.id_val_paren() == self.success:
        #     self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
#STUB - REMOVE 12/04/24
    # def id_val_paren(self):
    #     self.Tree.initialize_new()
    #     if self.match("(", True):
    #         self.enforce()
    #         self.id_val_op()
    #         self.enforce()
    #         self.match(")")
    #         self.id_expr_tail()
    #         self.Tree.end_branch(); return self.success
    #     else:
    #         return self.failed()
        
    @nullable
    def id_expr_tail(self):
        self.Tree.initialize_new()
        if self.num_math_op() == self.success:
            self.rel_expr()
            self.Tree.end_branch(); return self.success
        elif self.txt_op() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.logic_expr() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def logic_value(self):
            self.Tree.initialize_new()
            if self.match("Sus", True):
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.match("Charr", True):
                self.charr_op()
                self.charr_value()
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.logic_id() == self.success:
                self.Tree.end_branch(); return self.success
            elif self.logic_not_expr() == self.success:
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.numeric_value() == self.success:
                if self.num_math_op() == self.success:
                    self.enforce()
                    self.relop()
                    self.enforce()
                    self.rel_val()
                    self.logic_expr()
                    self.Tree.end_branch(); return self.success
                self.enforce()
                self.relop()
                self.enforce()
                self.rel_val()
                self.logic_expr()
                self.Tree.end_branch(); return self.success
            elif self.l_val_withparen() == self.success:
                self.Tree.end_branch(); return self.success
            else:
                return self.failed()
            
    def l_val_withparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.logic_value()
            self.match(")")
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def logic_not_expr(self):
        self.Tree.initialize_new()
        if self.match("!", True):
            if self.logic_not_tail() == self.success:
                self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    def logic_not_tail(self):
        self.Tree.initialize_new()
        if (self.logic_not_expr() == self.success):
            self.Tree.end_branch(); return self.success
        elif (self.logic_value() == self.success):
            self.Tree.end_branch(); return self.success
        else:
            self.enforce()
            return self.failed()
    
    @nullable
    def logic_expr(self):
        self.Tree.initialize_new()
        if self.logic_op() == self.success:
            self.logic_value()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def logic_id(self):
        self.Tree.initialize_new()
        if self.id_as_val() == self.success:
            self.logic_id_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def logic_id_tail(self):
        self.Tree.initialize_new()
        if self.num_math_op() == self.success:
            self.num_arithm()
            self.enforce()
            self.relop()
            self.rel_val()
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        elif self.relop() == self.success:
            self.rel_val()
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        elif self.logic_expr() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def num_arithm(self):
        self.Tree.initialize_new()
        if self.numeric_value() == self.success:
            self.num_math_op()
            self.Tree.end_branch(); return self.success
        elif self.num_arithmparen() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def num_arithmparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.num_arithm()
            self.match(")")
            self.num_math_op()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def id_arithm(self):
        self.Tree.initialize_new()
        if self.id_as_val() == self.success:
            self.id_arithm_tail()
            self.Tree.end_branch(); return self.success
        elif self.id_arithm_paren() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    def id_arithm_paren(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.id_arithm()
            self.match(")")
            self.id_arithm_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def id_arithm_tail(self):
        self.Tree.initialize_new()
        if self.num_math_op() == self.success:
            self.logic_id_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def num_or_arithmexpr(self):
        self.Tree.initialize_new()
        if self.numeric_value_or_id() == self.success:
            self.num_math_op()
            self.Tree.end_branch(); return self.success
        elif self.num_or_arithmparen() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def num_or_arithmparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.num_or_arithmexpr()
            self.match(")")
            self.num_math_op()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable
    def num_math_op(self):
        self.Tree.initialize_new()
        if self.math_op() == self.success:
            self.num_or_arithmexpr()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()

    @nullable 
    def rel_expr(self):
        self.Tree.initialize_new()
        if self.relop() == self.success:
            self.rel_val()
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def rel_val(self):
        self.Tree.initialize_new()
        if self.num_or_arithmexpr() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.match("Charr", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def math_op(self):
        ops = ["+", "-", "*", "/", "%"]
        self.Tree.initialize_new()
        for op in ops:
            if self.match(op, True):
                self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    @nullable
    def logic_op(self):
        self.Tree.initialize_new()
        if self.match("|", True):
            self.Tree.end_branch(); return self.success
        elif self.match("&", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def charr_op(self):
        self.Tree.initialize_new()
        if self.match("==", True) or self.match("!=", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def relop(self):
        self.Tree.initialize_new()
        if self.match("==", True) or self.match(">", True) or self.match(
                ">=", True) or self.match("<", True) or self.match("<=", True) or self.match("!=", True):
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def numeric_value_or_id(self):
        self.Tree.initialize_new()
        if self.numeric_value() == self.success:
            self.Tree.end_branch(); return self.success
        elif self.id_as_val() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def literal_logicval(self):
        self.Tree.initialize_new()
        if self.match("Sus", True):
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        elif self.logic_not_expr() == self.success:
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        # elif self.literal_logicvalparen() == self.success:
        #     self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def literal_logicvalparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.literal_logicval()
            self.match(")")
            self.logic_expr()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def literal_text(self):
        self.Tree.initialize_new()
        if self.match("Text", True):
            self.txt_op()
            self.Tree.end_branch(); return self.success
        elif self.literal_textparen() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def literal_textparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.literal_text()
            self.match(")")
            self.txt_op()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    def literal_charr(self):
        self.Tree.initialize_new()
        if self.match("Charr", True):
            self.charr_op_tail()
            self.Tree.end_branch(); return self.success
        elif self.literal_charrparen() == self.success:
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
    
    def literal_charrparen(self):
        self.Tree.initialize_new()
        if self.match("(", True):
            self.literal_charr()
            self.match(")")
            self.charr_op_tail()
            self.Tree.end_branch(); return self.success
        else:
            return self.failed()
        
    
    