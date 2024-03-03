from source.LexicalAnalyzer.tokenclass import Token
# import source.SyntaxAnalyzer.grammar as grammar
from source.core.error_handler import SyntaxError as Error
import sys


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
        # self.failed="Failed Parsing"
        self.expected=None
        self.isnullable=False
        self.expectset=[]
        
    def require(func):
        def wrapper(self, *args, **kwargs):
            self.isnullable=False
            result=func(self,*args, **kwargs)
            # self.isnullable=True
            # if result==None:
            #     self.failed()
            # else:
            #     self.isnullable=True
        return wrapper

    def nullable(func):
        def wrapper(self, *args, **kwargs):
            self.isnullable=True
            result=func(self,*args, **kwargs)
            if result==None:
                self.isnullable=False
                return
            # print(func)
            # print(self.isnullable)
            # self.isnullable=False  
    
        return wrapper
    

    # 
    def parse(self):
        if len(self.tokens)==0:
            self.syntax_errors.append("No tokens to parse fool")
            return self.syntax_errors
        else:
            try:
                self.program()
                return self.syntax_errors
            except SyntaxError as e:
                    print(e)
                    return self.syntax_errors
                

    # 
    def see(self, consumable):
        toklen=len(self.tokens)
        if (toklen!=0) and (self.tokens[0].type==consumable):
            return consumable
            # print(self.tokens)
        else: 
            return None

    # def retry(self):

    def skip(self):

        return self.success
            # self.retry()
        # print(self.tokens)

    # 
    def consume(self, consumable):
        toklen=len(self.tokens)
        if (toklen!=0) and (self.tokens[0].type==consumable):
            self.buffer.append(consumable)
            self.tokens.pop(0)
            return consumable
            # print(self.tokens)

        else: 
            return None
    
    # 
    def stop(self):
        raise SyntaxError("Syntax Error")

    def move(self):
        self.pointer+=1

    def error(self):
        print(len(self.tokens))
        if len(self.tokens)<=0:
            self.expectset=list(set(self.expectset))
            self.syntax_errors.append(Error(expected=self.expectset, unexpected="EOF", line="EOF"))
            return "EOF"        
        else:
            self.expectset=list(set(self.expectset))
            self.syntax_errors.append(Error(expected=self.expectset, unexpected=self.tokens[0].type, line=self.tokens[0].line))
            self.stop()

    def failed(self):
        if self.isnullable:
            # self.skip()
            # raise Exception("No Items for this Production")
            return
        else:
            if self.error()=="EOF":
                return
            else:
                # self.skip()
                print(f"pumasok sa skip ")
                print(self.tokens)
                
    def clear(self):
        self.buffer=[]    

    #     
    def match(self, consumable, skippable=False):
        self.expected=consumable
        if len(self.tokens)==0:
            self.expectset.append(self.expected)
            print(f"EOF, nothing to match {consumable} with.")
            self.expected=None
            return False
        consumed=self.see(consumable)  
        if consumed==None  : #and not nullable:
            if not skippable and not self.isnullable:
                
                try:
                    print(f"Failed Match: {consumable}, got {self.tokens[0]}" )
                except IndexError:
                    print(f"Failed Match: {consumable}, got EOF" )
                # self.skip()
                self.expectset.append(self.expected)
                self.expected=None
                
                return False
            else:
                print(f"No {consumable} detected. Skipping.")
                self.expectset.append(self.expected)
                self.expected=None
            # self.skip()
                return 

         #char not matched; might be wrong to do this
        # elif consumed==None and nullable:
        #     print(f"Failed Matching: {consumable}, got {self.tokens[0]}" )
        #     return Falses
   
            
        else: 
            self.consume(consumable)
            self.expected=None
            self.expectset=[]
            print("Matched:",consumed)
            return True
            # print(f"Expected {consumable} but found {self.tokens[0].type} at line {self.tokens[0].line}")
    # def __repr__(self) -> str:
    #     return 
        





#GRAMMAR____________________________________________________________________________________________      

    @require
    def program(self):
        #implement a way to assess if nothing is parsed

        # self.production_stack.append("program")
        # self.current_prod.append(grammar.Grammar.cfg[self.production_stack[-1]])
        # self.production_stack.pop()
        self.import_()
        print("Import:",self.buffer)
        self.clear()
        self.global_declaration()
        print("Global Dec:", self.buffer)
        self.clear()
        self.function_definition()
        print("Func Def Pre:", self.buffer)
        self.clear()
        self.sheesh_declaration()
        print("Sheesh Dec", self.buffer)
        self.clear()
        self.function_definition()
        print("Func Def Post:",self.buffer)

        return self.success
    
    # 

    def var_or_seq_dec(self):
        if self.seq_dtype()==self.success:
            self.match("Identifier")
            self.var_seq_tail()
            self.match("#")
            return self.success
        elif self.match("charr"):
            self.match("text")
            self.match("Identifier")
            self.vardec_tail()
            self.match("#")
            return self.success
        else: return self.failed()

    def var_seq_tail(self):
        if (self.vardec_tail()==self.success) or (self.seq_tail()==self.success):
            return self.success
        else:
            return self.failed()

    @nullable
    def import_(self):
        # self.nullable=True
        if self.match('use'):
            self.import_prog()
            # print(self.buffer)
            self.import_next()
            # print(self.buffer)
            self.match("#")
            # print(self.buffer)
            self.more_import()
            return self.success
        else: self.failed()

        
    # #
    @nullable
    def more_import(self):
        # self.nullable=True
        if self.import_():
         return self.success
        else:
            return self.failed()
        
    # @require
    def import_prog(self):
        if self.match("Identifier"):
            self.more_importprog()
            return self.success
        else: return self.failed()

    # 
    @nullable
    def more_importprog(self):
        # self.nullable=True

        if self.match(",", True):
            self.import_prog()
            return self.success
        else: return self.failed()
           

    # def function_definition(self):
    #     if self.match("function"):
    #         self.function_prototype()
    #         self.match("{")
    #         self.statement()
    #         self.match("}")
    # 
        
    @nullable
    def import_next(self):
        # self.nullable=True
        if self.match("from"):
            self.match("Identifier")
            return self.success
        else: return self.failed()



    # 
    @nullable
    def global_declaration(self):
        # self.nullable=True
        if self.global_statement():
            self.more_globaldec()
            return self.success
        else: return self.failed()
        

    # 
    @nullable
    def more_globaldec(self):
       if self.global_declaration():
           return self.success
       else: return self.failed()

    # @require
    def global_statement(self):
        if self.var_or_seq_dec()==self.success:
            return self.success
        elif self.function_prototype()==self.success:
            return self.success
        elif self.constant_declaration()==self.success:
            return self.success
        else: return self.failed()
    

    # @require
    def function_prototype(self):
        if self.yeet_type()==self.success:
            self.match("Identifier")
            self.match("(")
            self.parameter()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed()

    @nullable
    def parameter(self):
        if self.all_dtype()==self.success:
            self.match("Identifier")
            self.more_paramtail()
            return self.success
        elif self.match("blank"):
            return self.success
        else: return self.failed()

    def more_param(self):
        if self.match(","):
            self.all_dtype()
            self.match("Identifier")
            self.more_paramtail()
        else: return self.failed()

    @nullable
    def more_paramtail(self):
        if self.more_param()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def yeet_type(self):
        if self.all_dtype()==self.success or self.match("blank"):
            return self.success
        else:
            return self.failed()

    # @require
    def all_dtype(self):
        if self.seq_dtype()==self.success:
            return self.success
        else:
            if self.match("charr"): #issue?
                if self.match("text"): #issue
                    return self.success
            else: return self.failed() 
            return self.failed()
        
    # @require
    def seq_dtype(self):
        dtypes=["whole", "dec", "text", "sus"]
        for type in dtypes:
            if self.match(type):
                return self.success
        
        return self.failed()

    # @require
    def all_literal(self):
        if (self.seq_literal()==self.success):
            return self.success
        if self.match("Charr", True):
            return self.success
        else: return self.failed()
        
    # @require
    def seq_literal(self):
        seqlits=["Text", "Whole", "Dec", "Sus"]
        if self.match("Text", True) or self.match("Whole", True) or self.match("Dec",True) or self.match("Sus", True):
            return self.success
        else:
            return self.failed()
    # @require
    def numeric_value(self):
        if (self.common_val()==self.success) or self.match("Whole") or self.match("Dec") or (self.seq_use()==self.success):
            return self.success
        else: return self.failed()

    # @require
    def sheesh_declaration(self):
        if self.match('sheesh'):
            self.match('(')
            self.match(')')
            self.match("{")
            self.statement()
            # self.variable_declaration()
            self.match("}")
            return self.success
        
        else: return self.failed()

    @require
    def statement(self):
        # self.isnullable=False
        if self.single_statement()==self.success:
            self.more_statement()
            return self.success
        else: return self.failed()

    # @require
    # @require
    def single_statement(self):
        if self.allowed_in_loop()==self.success:
            return self.success
        elif self.control_flow_statement()==self.success:
            return self.success
        else: 
            # self.isnullable=False
            return self.failed()

    # @require
    # @nullable
    def allowed_in_loop(self):
        if self.var_or_seq_dec()==self.success:
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
        elif self.function_invocation()==self.success:
            self.match("#")  
            return self.success
        else:
            return self.failed()

    @nullable
    def more_statement(self):
        # nullable=True
        # if len(self.tokens)>0 and self.tokens[0]!="}":
            if self.single_statement()==self.success:
                self.more_statement()
                return self.success
            else: return self.failed()

    # @require
    def io_statement(self):
        if self.pa_mine_statement()==self.success:
            return self.success
        elif self.up_statement()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def pa_mine_statement(self):
        if self.match("pa_mine"):
            self.match("(")
            self.argument()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed()

    # @require
    def up_statement(self):
        if self.match("up"):
            self.match("(")
            self.argument()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed()

    # @require
    
    def variable_declaration(self):
        if self.all_dtype()==self.success:
            self.match("Identifier")
            self.vardec_tail()
            self.match("#")
            return self.success
        else: return self.failed()

    # @require
    def vardec_tail(self):
        if self.variable_assign()==self.success:
            self.more_vardec()
            return self.success
        else: return self.failed()

    @nullable
    def more_vardec(self):
        # nullable=True ; self.isnullable
        if self.match(",", True):
            self.match("Identifier")
            self.vardec_tail()
            return self.success
        else: return self.failed()

    @nullable
    def variable_assign(self):
        # nullable=True
        if self.match("="):
            self.assign_value()
            return self.success
        else: 
            return self.failed()

    # @require
    def variable_reassign(self):
        if self.match("Identifier"):
            self.assign_op()
            self.assign_value()
            return self.success
        else: return self.failed()

    # @require
    def common_val(self):
        if (self.function_invocation()==self.success): #self.match("Identifier") or 
            return self.success
        else: return self.failed()


    # @require
    def assign_value(self):
        # self.isnullable=False
        
        if (self.all_literal() == self.success):
            return self.success
        elif (self.common_val() == self.success):
            return self.success 
        elif (self.expression()==self.success):
            return self.success
        elif(self.seq_use()==self.success):
            return self.success
        else: 
            return self.failed()

    # @require
    def constant_declaration(self):
        if self.match("based"):
            self.const_type()
        else: return self.failed()

    def const_type(self):
        if self.seq_dtype()==self.success:
            self.match("Identifier")
            self.const_tail()
            return self.success
        elif self.match("charr"):
            self.match("text")
            self.match("Identifier")
            self.const_var_tail()
            return self.success
        else: return self.failed()
    # def const_seq(self):
    #     if self.match("based"):
    #         pass
    # @require
    def const_tail(self):
        if self.const_var_tail()==self.success:
            self.match("#")
            return self.success
        if self.seq_one_dim()==self.success:
            self.match("=")
            self.seq_init()
            self.match("#")
            return self.success
        else: return self.failed()

    # @require
    def const_var_tail(self):
        if self.match("="):
            self.assign_value()
            self.more_const()
            return self.success
        else: return self.failed()    

    @nullable
    def more_const(self):
        if self.match(","):
            self.const_var_tail()
            return self.success
        else: return self.failed()

    # @require
    def assign_op(self): #issue
        aops=["=","+=","-=","*=","/=", "%="]
        for op in aops:
            if self.match(op):
                return self.success
        return self.failed()

    # @require
    def function_invocation(self):
        if self.match("Identifier"):
            if self.match("("):
                self.func_argument()
                self.match(")")
            else: return self.success
            return self.success
        else: return self.failed()

    @nullable
    def func_argument(self):
        # nullable=True 
        if self.argument()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def argument(self):
        if self.args_value()==self.success:
            self.more_args()
            return self.success
        else: return self.failed()

    # @require
    def args_value(self):
        if self.assign_value()==self.success:
            return self.success
        else: return self.failed()
    
    @nullable
    def more_args(self):
        if self.match(","):
            self.argument()
            return self.success
        else: return self.failed()    

    # @require
    def control_flow_statement(self):
        if self.kung_statement()==self.success:
            self.cond_tail()
            return self.success
        elif self.choose_statement()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def kung_statement(self):
        if self.match("kung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
            self.ehkung_statement()
            return self.success
        else: return self.failed()

    # @require
    def ehkung_statement(self):
        if self.match("ehkung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
            self.ehkung_statement()
            return self.success
        else: return self.failed()

    # @require
    def deins_statement(self):
        if self.match("deins"):
            self.match("{")
            self.statement()
            self.match("}")
            return self.success
        else: return self.failed()

    @nullable
    def cond_tail(self):
        if self.ehkung_statement()==self.success:
            self.more_condtail()
            return self.success
        elif self.deins_statement()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def more_condtail(self):
        if self.cond_tail()==self.success:
            return self.success
        else: return self.failed()

    # @require
    def choose_statement(self):
        if self.match("choose"):
            self.match("(")
            self.match("Identifier")
            self.match(")")
            self.match("{")
            self.when_statement()
            self.choose_default()
            self.match("}")
            return self.success
        else: return self.failed()

    # @require
    def when_statement(self):
        if self.match("when"):
            self.all_literal()
            self.match("::")
            self.statement_for_choose()
            self.more_when()
            return self.success
        else: return self.failed()

    # @require
    def statement_for_choose(self):
        if self.statement()==self.success:
            return self.success
        elif self.match("felloff"):
            self.match("#")
            return self.success
        else: return self.failed() 

    @nullable
    def more_when(self):
        if self.when_statement()==self.success:
            return self.success
        else: return self.failed()

    @nullable
    def choose_default(self):
        if self.match("default"):
            self.match("::")
            self.statement_for_choose()
            return self.success
        else: return self.failed()

    # @require
    def looping_statement(self):
        if (self.bet_statement()==self.success) or (self.for_statement()==self.success):
            return self.success
        else: return self.failed()

    # @require
    def bet_statement(self):
        if self.match("bet"):
            self.match("{")
            self.loop_body()
            self.match("}")
            self.match("kung")
            self.match("(")
            self.condition()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed()
        

    # @require
    def for_statement(self):
        if self.match("for"):
            self.match("(")
            self.match("Identifier")
            self.match("=")
            self.for_initial_val()
            self.match("to")
            self.end_val()
            self.step_statement()
            self.match(")")
            self.match("{")
            self.loop_body()
            self.match("}")
            return self.success
        else: return self.failed()

    # @require
    def end_val(self):
        if self.for_initial_val==self.success:
            return self.success
        else: return self.failed()

    def for_initial_val(self):
        if self.match("Whole") or (self.common_val()==self.success) or (self.arithmetic_expression()==self.success) or (self.seq_use()==self.success):
            return self.success
        else: return self.failed()

    @nullable
    def step_statement(self):
        if self.match("step"):
            self.for_initial_val()
            return self.success
        else: return self.failed()

    def loop_body(self):
        if self.loop_body_statement()==self.success:
            self.more_loop_body()
            return self.success
        else: return self.failed()

    def loop_body_statement(self):
        if (self.loop_kung()==self.success) or (self.loop_choose()==self.success) or (self.loop_control_statement()==self.success) or (self.allowed_in_loop()==self.success):
            return self.success
        else: return self.failed()

    @nullable
    def more_loop_body(self):
        if self.loop_body()==self.success:
            return self.success
        else: return self.failed()

    def loop_kung(self):
        if self.match("kung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.match("{")
            self.loop_body()
            self.match("}")
            return self.success
        else: return self.failed()

    def loop_ehkung(self):
        if self.match("ehkung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.match("{")
            self.loop_body()
            self.match("}")
            return self.success
        else: return self.failed()

    def loop_deins(self):
        if self.match("deins"):
            self.match("{")
            self.loop_body()
            self.match("}")
            return self.success
        else: return self.failed()

    @nullable
    def in_loop_condtail(self):
        if self.loop_ehkung()==self.success:
            self.more_inloop_condtail()
            return self.success
        elif self.loop_deins()==self.success:
            return self.success
        else: return self.failed()

    def more_inloop_condtail(self):
        if self.in_loop_condtail()==self.success:
            return self.success
        else: return self.failed()

    def loop_choose(self):
        if self.match("choose"):
            self.match("(")
            self.match("Identifier")
            self.match(")")
            self.match("{")
            self.loop_when()
            self.loop_default()
            self.match("}")
            return self.success
        else: return self.failed()

    def loop_when(self):
        if self.match("when"):
            self.all_literal()
            self.match("::")
            self.loop_body()
            self.in_loop_when()
            return self.success
        else: return self.failed()

    @nullable
    def in_loop_when(self):
        if self.loop_when()==self.success:
            return self.success
        else: return self.failed()

    @nullable
    def loop_default(self):
        if self.match("default"):
            self.match("::")
            self.loop_body()
            return self.success
        else: return self.failed()

    def loop_control_statement(self):
        if self.match("felloff"):
            self.match("#")
            return self.success
        elif self.match("pass"):
            self.match("#")
            return self.success
        else: return self.failed()

    def condition(self):
        if (self.relational_expression()==self.success) or (self.logical_expression()==self.success) or (self.common_val()==self.success) or (self.seq_use()==self.success) or self.match("Sus"):
            return self.success
        else: return self.failed()

    
    def sequence_declaration(self):
        if (self.seq_dtype()==self.success):
            self.match("Identifier")
            self.seq_tail()
            self.match("#")
            return self.success
        else: return self.failed()

    def seq_tail(self):
        if (self.seq_one_dim()==self.success):
            self.seq_assign()
            return self.success
        elif (self.multi_seq()==self.success):
            return self.success
        else: return self.failed()

    @nullable
    def seq_assign(self):
        if self.match("="):
            self.seq_init()
            return self.success
        else: return self.failed()

    def seq_init(self):
        if self.match("{"):
            self.seq_elem()
            self.match("}")
            return self.success
        else: return self.failed()

    def seq_elem(self):
        if (self.seq_elem_value()==self.success):
            return self.success
        elif (self.seq_init()==self.success):
            self.seq_two_d_init()
            return self.success
        else: return self.failed()

    @nullable
    def seq_two_d_init(self):
        if self.match(","):
            self.seq_init()
            self.seq_three_d_init()
            return self.success
        else: return self.failed()

    @nullable
    def seq_three_d_init(self):
        if self.match(","):
            self.seq_init()
            return self.success
        else: return self.failed()

    def seq_elem_value(self):
        if self.seq_literal()==self.success:
            self.next_elem_value()
            return self.success
        else: return self.failed()

    @nullable
    def next_elem_value(self):
        if self.match(","):
            self.seq_elem_value()
            return self.success
        else: return self.failed()

    def multi_seq(self):
        if self.seq_one_dim()==self.success:
            self.more_seqtail()
            return self.success
        else: return self.failed()

    @nullable
    def more_seq(self):
        if self.match(","):
            self.match("Identifier")
            self.seq_one_dim()
            self.more_seqtail()
            return self.success
        else: return self.failed()

    def more_seqtail(self):
        if self.more_seq()==self.success:
            return self.success
        else: return self.failed()

    def seq_one_dim(self):
        if (self.index()==self.success):
            self.seq_two_dim()
            return self.success
        else: return self.failed()

    @nullable
    def seq_two_dim(self):
        if (self.index()==self.success):
            self.seq_three_dim()
            return self.success
        else: return self.failed()

    @nullable
    def seq_three_dim(self):
        if self.index()==self.success:
            return self.success
        else: return self.failed()

    def index(self):
        if self.match("["):
            self.seq_index_val()
            self.match("]")
            return self.success
        else: return self.failed()

    def seq_index_val(self):
        if (self.common_val()==self.success) or self.match("Whole") or (self.arithmetic_expression()==self.success):
            return self.success
        else: return self.failed()

    def seq_use(self):
        if self.match("Identifier"):
            self.seq_one_dim()
            return self.success
        else: return self.failed()

    def seq_use_assign(self):
        if self.seq_use()==self.success:
            self.assign_op()
            self.assign_value()
            self.match("#")
            return self.success
        else: return self.failed()

    def expression(self): #issue, sus
        if (self.arithmetic_expression==self.success) or (self.logical_expression==self.success) or (self.relational_expression==self.success) or (self.text_concat==self.success):
            return self.success
        else: return self.failed()

    def arithmetic_expression(self):
        if self.arithm_term()==self.success:
            self.arithm_addtail()
            return self.success
        else: return self.failed()

    def arithm_term(self):
        if self.arithm_factor()==self.success:
            self.arithm_mult_term()
            return self.success
        else: return self.failed()

    def arithm_factor(self):
        if self.numeric_value==self.success:
            return self.success
        elif self.match("("):
            self.arithmetic_expression()
            self.match(")")
            return self.success
        else: return self.failed()    

    def arithm_tail(self):
        if self.add_op==self.success:
            self.arithm_term()
            self.arithm_addtail()
            return self.success
        else: return self.failed()

    @nullable
    def arithm_addtail(self):
        # nullable=True
        if self.arithm_tail()==self.success:
            self.success
        else: return self.success

    def arithm_term_tail(self):
        if self.mult_op()==self.success:
            self.arithm_factor()
            self.arithm_mult_term()
            return self.success
        else: return self.failed()

    @nullable
    def arithm_mult_term(self):
        # nullable=True
        if self.arithm_term_tail()==self.success:
            return self.success
        else: return self.success

    def add_op(self):
        if self.match("+") or self.match("-"):
            return self.success
        else : return self.failed()

    def mult_op(self):
        if self.match("*") or self.match("/") or self.match("%"):
            return self.success
        else: return self.failed()

    def relational_expression(self):
        if (self.relexrp_with_paren()==self.success) or (self.relexrp_without_paren()==self.success):
            return self.success
        else: return self.failed()

    def relexrp_with_paren(self):
        if self.match("("):
            self.relational_expression()
            self.match(")")
            return self.success
        else: return self.failed()

    def relexrp_without_paren(self):
        if (self.numeric_value()==self.success):
            self.relop()
            self.numeric_value()
            return self.success
        elif (self.charr_val()==self.success):
            self.match("==")
            self.charr_val()
            return self.success
        else: return self.failed()

    def charr_val(self):
        if (self.common_val()==self.success) or self.match("Charr"):
            return self.success
        else: return self.failed()

    def relop(self):
        if self.match("==") or self.match(">") or self.match(">=") or self.match("<") or self.match("<=") or self.match("!="):
            return self.success
        else: return self.failed()


    def logical_expression(self):
        if self.logic_term()==self.success:
            self.logic_ortail()
            return self.success
        else: return self.failed()

    def logic_term(self):
        if self.logic_factor()==self.success:
            self.logic_andterm()
            return self.success
        else: return self.failed()

    def logic_factor(self):
        if (self.logic_value()==self.success) or (self.logical_not_expression()==self.success):
            return self.success
        elif self.match("("):
            self.logical_expression()
            self.match(")")
            return self.success
        else: return self.failed()

    def logic_tail(self):
        if self.match("|"):
            self.logic_term()
            self.logic_ortail()
            return self.success 
        else: return self.failed()

    @nullable
    def logic_ortail(self):
        if self.logic_tail()==self.success:
            return self.success
        else: return self.failed()

    def logic_term_tail(self):
        if self.match("&"):
            self.logic_factor()
            self.logic_andterm()
            return self.success
        else: return self.failed()

    @nullable
    def logic_andterm(self):
        if self.logic_term_tail()==self.success:
            return self.success
        else: return self.failed()
        

    def logical_not_expression(self):
        if self.logic_not()==self.success:
            self.logic_not_tail()
            return self.success
        else: return self.failed()

    def logic_not_tail(self):
        if (self.logical_not_expression()==self.success) or (self.logic_value()==self.success):
            return self.success
        else: return self.failed()

    def logic_not(self):
        if self.match("!"):
            return self.success
        else: return self.failed()

    def logic_value(self):
        if (self.common_val()==self.success) or self.match("Sus") or (self.relational_expression()==self.success) or (self.seq_use()==self.success) or (self.logical_not_expression()==self.success):
            return self.success
        else: return self.failed()

    def text_concat(self):
        if self.concat_val()==self.success:
            self.concat_tail()
            return self.success
        else: return self.failed()

    def concat_tail(self):
        if self.match("..."):
            self.concat_val()
            self.more_concat()
            return self.success
        else: return self.failed()

    @nullable
    def more_concat(self):
        if self.concat_tail()==self.success:
            return self.success
        else: return self.failed()

    def concat_val(self):
        if self.match("Text") or (self.common_val()==self.success) or (self.seq_use()==self.success):
            return self.success
        else: return self.failed()

    @nullable
    def function_definition(self):
        if self.func_def()==self.success:
            self.more_funcdef()
            return self.success
        else: return self.failed()

    # @require
    def func_def(self):
        if self.yeet_type()==self.success:
            self.match("Identifier")
            self.match("(")
            self.parameter()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
            return self.success
        else: return self.failed()

    @nullable
    def more_funcdef(self):
        if self.function_definition()==self.success:
            return self.success
        else: return self.failed()

    @nullable
    def yeet_statement(self):
        if self.match("yeet"):
            self.return_value()
            self.match("#")
            return self.success
        else: return self.failed()

    @nullable
    def return_value(self):
        if self.assign_value()==self.success:
            return self.success
        else: return self.failed()
