from source.LexicalAnalyzer.tokenclass import Token
# import source.SyntaxAnalyzer.grammar as grammar
from source.core.error_handler import SyntaxError as Error

def log_method_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class SyntaxAnalyzer:
    
    def __init__(self, tokens:list[Token]) -> None:
        self.tokens=tokens
        self.pointer=0
        self.production_stack=[]
        self.current_prod=[]
        self.buffer=[]
        self.syntax_errors=[]
        self.toklen=len(self.tokens)
        self.success="Success"
        self.failed="Failed Parsing"
        

    # @log_method_call
    def parse(self):
        status=self.program()
        return status,self.syntax_errors

    # @log_method_call
    def look_ahead(self):
        if self.pointer<len(self.tokens):
            return self.tokens[self.pointer+1]
        else:
            return None

    # @log_method_call
    def consume(self, consumable):
        toklen=len(self.tokens)
        if (toklen!=0) and (self.tokens[0].type==consumable):
            self.buffer.append(consumable)
            self.tokens.pop(0)
            return consumable
            # print(self.tokens)

        else: 
            return None
    
    # @log_method_call
    def move(self):
        self.pointer+=1

    # @log_method_call    
    def match(self, consumable, nullable=False):
        if len(self.tokens)==0:
            return False
        self.expected=consumable
        consumed=self.consume(consumable)      
        if consumed==None and not nullable:
            self.syntax_errors.append(Error(expected=consumable, unexpected=self.tokens[0].type, line=self.tokens[0].line))    
            return 

         #char not matched; might be wrong to do this
        elif consumed==None and nullable:
            return False
        else: return True
            # print(f"Expected {consumable} but found {self.tokens[0].type} at line {self.tokens[0].line}")
    # def __repr__(self) -> str:
    #     return 
        
    def program(self):
        # self.production_stack.append("program")
        # self.current_prod.append(grammar.Grammar.cfg[self.production_stack[-1]])
        # self.production_stack.pop()
        self.import_()
        self.global_declaration()
        self.function_definition()
        self.sheesh_declaration()
        self.function_definition()
        return self.success
    
    # @log_method_call
    def import_(self):
        nullable=True
        if self.match('use', nullable):
            self.import_prog()
            print(self.buffer)
            self.import_next()
            print(self.buffer)
            self.match("#")
            print(self.buffer)
            self.more_import()
            return "Success"
        else: return "Failed Parsing"

        

    # @log_method_call
    def more_import(self):
        nullable=True
        if self.import_():
         return "Success"
        else:
            return "Failed Parsing"
        
    # @log_method_call
    def import_prog(self):
        if self.match("Identifier"):
            self.more_importprog()
            return "Success"
        else: return "Failed Parsing"

    # @log_method_call
    def more_importprog(self):
        nullable=True

        if self.match(",", True):
            self.import_prog()
            return self.success
        else: return self.failed
           

    # def function_definition(self):
    #     if self.match("function"):
    #         self.function_prototype()
    #         self.match("{")
    #         self.statement()
    #         self.match("}")
    # @log_method_call
    def import_next(self):
        nullable=True
        if self.match("from"):
            self.match("Identifier")
            return self.success
        else: return self.failed



    @log_method_call
    def global_declaration(self):
        nullable=True
        self.global_statement()
        self.more_globaldec()
        

    @log_method_call
    def more_globaldec(self):
        pass

    def global_statement(self):
        pass

    def function_prototype(self):
        pass

    def parameter(self):
        pass

    def more_param(self):
        pass

    def more_paramtail(self):
        pass

    def yeet_type(self):
        pass

    def all_dtype(self):
        if self.seq_dtype()==self.success:
            return self.success
        elif self.match("charr"):
            if self.match("text"):
                return self.success
            else: return self.failed
        else: return self.failed
        

    def seq_dtype(self):
        dtypes=["whole", "dec", "text", "sus"]
        for type in dtypes:
            if self.match(type):
                return self.success
        return self.failed

    def all_literal(self):

        if self.seq_literal()==self.success or self.match("Charr"):
            return self.success
        else: return self.failed
        

    def seq_literal(self):
        seqlits=["Text", "Whole", "Dec", "Sus"]
        for lit in seqlits:
            if self.match(lit):
                return self.success
        return self.failed

    def numeric_value(self):
        pass

    def sheesh_declaration(self):
        if self.match('sheesh'):
            self.match('(')
            self.match(')')
            self.match("{")
            self.statement()
            self.match("}")
            return self.success
        
        else: return self.failed

    def statement(self):
        if self.single_statement()==self.success:
            self.more_statement()
            return self.success
        else: return self.failed

    def single_statement(self):
        if self.allowed_in_loop()==self.success:
            return self.success
        elif self.control_flow_statement()==self.success:
            return self.success
        else: return self.failed

    def allowed_in_loop(self):
        if self.variable_declaration()==self.success:
            return self.success
        elif self.sequence_declaration()==self.success:
            return self.success
        elif self.function_invocation()==self.success:
            self.match("#")  
            return self.success
        elif self.looping_statement()==self.success:
            return self.success
        elif self.yeet_statement()==self.success:
            return self.success
        elif self.io_statement()==self.success:
            return self.success
        elif self.seq_use_assign()==self.success:
            return self.success
        elif self.variable_reassign()==self.success:
            self.match("#")
            return self.success
        else: return self.failed

    def more_statement(self):
        nullable=True
        if self.statement()==self.success:
            return self.success
        else: return self.success #issue

    def io_statement(self):
        if self.pa_mine_statement()==self.success:
            return self.success
        elif self.up_statement()==self.success:
            return self.success
        else: return self.failed

    def pa_mine_statement(self):
        if self.match("pa_mine"):
            self.match("(")
            self.argument()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed

    def up_statement(self):
        if self.match("up"):
            self.match(")")
            self.argument()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed

    def variable_declaration(self):
        if self.all_dtype()==self.success:
            self.vardec_tail()
            self.match("#")
            return self.success
        else: return self.failed

    def vardec_tail(self):
        if self.match("Identifier"):
            self.variable_assign()
            self.more_vardec()
            return self.success
        else: return self.failed

    def more_vardec(self):
        nullable=True
        if self.match(",", nullable):
            self.vardec_tail()
            return self.success
        else: return self.success #issue

    def variable_assign(self):
        nullable=True
        if self.match("=", nullable):
            self.assign_value()
            return self.success
        else: return self.success #issue

    def variable_reassign(self):
        if self.match("Identifier"):
            self.assign_op()
            self.assign_value()
            return self.success

    def common_val(self):
        if self.match("Identifier") or (self.function_invocation()==self.success):
            return self.success
        else: return self.failed


    def assign_value(self):
        if (self.common_val()==self.success) or (self.all_literal()==self.success) or (self.expression()==self.success) or (self.seq_use()==self.success):
            return self.success
        else: return self.failed

    def constant_declaration(self):
        if (self.const_var()==self.success) or (self.const_seq()==self.success):
            return self.success
        else: return self.failed

    def const_seq(self):
        if self.match("based"):
            pass

    def const_var(self):
        pass

    def const_tail(self):
        pass

    def more_const(self):
        pass

    def assign_op(self): #issue
        ops=["=","+=","-=","*=","/=", "%="]
        for op in ops:
            if self.match(op):
                return self.success
        return self.failed

    def function_invocation(self):
        if self.match("Identifier"):
            self.match("(")
            self.func_argument()
            self.match(")")
            return self.success
        else: return self.failed

    def func_argument(self):
        nullable=True
        if self.argument()==self.success:
            return self.success
        else: return self.success #issue

    def argument(self):
        pass

    def args_value(self):
        pass

    def more_args(self):
        pass

    def control_flow_statement(self):
        pass

    def kung_statement(self):
        pass

    def ehkung_statement(self):
        pass

    def deins_statement(self):
        pass

    def cond_tail(self):
        pass

    def more_condtail(self):
        pass

    def choose_statement(self):
        pass

    def when_statement(self):
        pass

    def statement_for_choose(self):
        pass

    def more_when(self):
        pass

    def choose_default(self):
        pass

    def looping_statement(self):
        pass

    def bet_statement(self):
        pass

    def for_statement(self):
        pass

    def end_val(self):
        pass

    def for_initial_val(self):
        pass

    def step_statement(self):
        pass

    def loop_body(self):
        pass

    def loop_body_statement(self):
        pass

    def more_loop_body(self):
        pass

    def loop_kung(self):
        pass

    def loop_ehkung(self):
        pass

    def loop_deins(self):
        pass

    def in_loop_condtail(self):
        pass

    def more_inloop_condtail(self):
        pass

    def loop_choose(self):
        pass

    def loop_when(self):
        pass

    def in_loop_when(self):
        pass

    def loop_default(self):
        pass

    def loop_control_statement(self):
        pass

    def condition(self):
        pass

    def sequence_declaration(self):
        pass

    def seq_tail(self):
        pass

    def seq_assign(self):
        pass

    def seq_init(self):
        pass

    def seq_elem(self):
        pass

    def seq_two_d_init(self):
        pass

    def seq_three_d_init(self):
        pass

    def seq_elem_value(self):
        pass

    def next_elem_value(self):
        pass

    def multi_seq(self):
        pass

    def more_seq(self):
        pass

    def more_seqtail(self):
        pass

    def seq_one_dim(self):
        pass

    def seq_two_dim(self):
        pass

    def seq_three_dim(self):
        pass

    def index(self):
        pass

    def seq_index_val(self):
        pass

    def seq_use(self):
        pass

    def seq_use_assign(self):
        pass

    def expression(self): #issue, sus
        if (self.arithmetic_expression==self.success) or (self.logical_expression==self.success) or (self.relational_expression==self.success) or (self.text_concat==self.success):
            return self.success
        else: return self.failed

    def arithmetic_expression(self):
        if self.arithm_term()==self.success:
            self.arithm_addtail()
            return self.success
        else: return self.failed

    def arithm_term(self):
        if self.arithm_factor()==self.success:
            self.arithm_mult_term()
            return self.success
        else: return self.failed

    def arithm_factor(self):
        if self.numeric_value==self.success:
            return self.success
        elif self.match("("):
            self.arithmetic_expression()
            self.match(")")
            return self.success
        else: return self.failed    

    def arithm_tail(self):
        if self.add_op==self.success:
            self.arithm_term()
            self.arithm_addtail()
            return self.success
        else: return self.failed

    def arithm_addtail(self):
        nullable=True
        if self.arithm_tail()==self.success:
            self.success
        else: return self.success

    def arithm_term_tail(self):
        if self.mult_op()==self.success:
            self.arithm_factor()
            self.arithm_mult_term()
            return self.success
        else: return self.failed

    def arithm_mult_term(self):
        nullable=True
        if self.arithm_term_tail()==self.success:
            return self.success
        else: return self.success

    def add_op(self):
        if self.match("+") or self.match("-"):
            return self.success
        else : return self.failed

    def mult_op(self):
        if self.match("*") or self.match("/") or self.match("%"):
            return self.success
        else: return self.failed

    def relational_expression(self):
        pass

    def relexrp_with_paren(self):
        pass

    def relexrp_without_paren(self):
        pass

    def charr_val(self):
        pass

    def relop(self):
        pass

    def logical_expression(self):
        pass

    def logic_term(self):
        pass

    def logic_factor(self):
        pass

    def logic_tail(self):
        pass

    def logic_ortail(self):
        pass

    def logic_term_tail(self):
        pass

    def logic_andterm(self):
        pass

    def logical_not_expression(self):
        pass

    def logic_not_tail(self):
        pass

    def logic_not(self):
        pass

    def logic_value(self):
        pass

    def text_concat(self):
        pass

    def concat_tail(self):
        pass

    def more_concat(self):
        pass

    def concat_val(self):
        pass

    def function_definition(self):
        pass

    def func_def(self):
        pass

    def more_funcdef(self):
        pass

    def yeet_statement(self):
        pass

    def return_value(self):
        pass
