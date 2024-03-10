from source.LexicalAnalyzer.tokenclass import Token
# import source.SyntaxAnalyzer.grammar as grammar
from source.core.error_handler import SyntaxError as Error
import sys
sys.path.append( '.' )

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

#___________________________WRAPPERS____________________________________________________________________________________________________________
              
    def require(func):
        def wrapper2(self, *args, **kwargs):
            self.isnullable=False
            result=func(self,*args, **kwargs)
            # self.isnullable=True
            if result==None:
                self.failed()
            else:
                # self.isnullable=True
                return result
        return wrapper2

    def nullable(func):
        def wrapper(self, *args, **kwargs):
            self.isnullable=True
            result=func(self,*args, **kwargs)
            if result==None:
                # self.isnullable=False
                return
            else:
                return result
            # print(func)
            # print(self.isnullable)
            # self.isnullable=False  
    
        return wrapper
    
# _______________________________________________FUNCTIONS_____________________

    def reset(self):
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


    def parse(self):
        self.reset()
        if len(self.tokens)==0:
            self.syntax_errors.append("No tokens to parse fool")
            return self.syntax_errors
        else:
            try:
                self.program()
                print(self.tokens)
                return self.syntax_errors
            except SyntaxError as e:
                    print(e)
                    return self.syntax_errors
                
    def enforce(self):
        self.isnullable=False

    # 
    def peek(self, chars_ahead=0):
        if len(self.tokens)>chars_ahead:
            try:
                return self.tokens[0+chars_ahead].type
            except IndexError:
                return None
        else: return None

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
            self.stop()
            return "EOF"        
        else:
            self.expectset=list(set(self.expectset))
            self.syntax_errors.append(Error(expected=self.expectset, unexpected=self.tokens[0].type, line=self.tokens[0].line))
            self.stop()

    def failed(self):
        if self.isnullable:
            # self.skip()
            # raise Exception("No Items for this Production")
            # self.isnullable=False
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
                self.failed()
                
                return False
            else:
                print(f"No {consumable} detected. Skipping.")
                self.expectset.append(self.expected)
                self.expected=None
                # self.isnullable=True
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

    # @require
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

        self.isnullable=False
        if self.tokens==[]:
            return self.success
        else:
            print("failed")
            return self.failed()    
    
    # 
    # def inside_func_invocation(self):
    #     if self.argument()==self.success:
    #         # if self.match(")"):
    #             return self.success
    #     else: return self.failed()

    # def var_or_seq_or_funcinvoc_dec(self):
    #     if self.seq_dtype()==self.success:
    #         self.enforce()
    #         if self.match("Identifier"): #ambiguity
    #             if self.var_seq_tail()==self.success:
    #                 self.match("#")
    #                 return self.success
    #             elif self.match("("):
    #                 self.inside_func_invocation()
    #                 if self.match(")") :
    #                     self.match("#")
    #                 else: return self.failed()
    #                 return self.success
    #             else: return self.failed()

            
    #         else: return self.failed()
    #     elif self.match("charr", True):
    #         self.enforce()
    #         if self.match("text"):
    #             self.match("Identifier")
    #             self.vardec_tail()
    #             self.match("#")
    #             return self.success
    #         else: return self.failed()
    #     else: return self.failed()



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
        
    
    def import_prog(self): #sussy
        if self.match("Identifier", True):
            self.func_imptail()
            self.more_importprog()
            return self.success
        else: return self.failed()

    @nullable
    def func_imptail(self):
        if self.match("("):
            self.enforce
            if self.match(")"):
                return self.success
            else: return self.failed()
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
        if self.match("from", True):
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

    
    def global_statement(self):
        # if self.seq_dtype()==self.success:
        #     if self.match("Identifier"):
        #         if self.function_invocation_tail():
        #             return self.success
        #         elif self.var_or_seq_or_funcinvoc_dec_tail():
        #             return self.success
                
        #         else: return self.failed()
        # elif self.constant_declaration():
        #         return self.success
        # else: return self.failed()

        # if self.gbl_var_seq_func()==self.success: #ambiguous
        #     return self.success
        # elif self.constant_declaration()==self.success: 
        #     return self.success
        # else: return self.failed()

        if self.var_or_seq_dec()==self.success:
            return self.success
        elif self.constant_declaration()==self.success:
            return self.success
        
        else: return self.failed()
    
    # def var_or_seq_or_funcinvoc_dec_tail(self):
    #     if self.var_seq_tail()==self.success:
    #         self.match("#")
    #         return self.success
    #     else: return self.failed()

    # def function_invocation_tail(self):
    #     if self.match("("):
    #         self.inside_func_invocation()
    #         self.match(")")
    #         self.match("#")
    #         return self.success
    #     else: return self.failed()
    
    def funcproto_tail(self):
        if self.match("Identifier"):
            self.match("(")
            self.parameter()
            self.match(")")
            return self.success
        else: return self.failed()


    #deprecated
    def gbl_var_seq_func(self):
        if self.var_seq_common()==self.success:
            self.var_seq_func_tail()
            self.match("#")
            return self.success
        elif self.match("charr", True):
            self.match("text")
            self.match("Identifier")
            self.charr_gbl_tail()
            self.match("#")
            return self.success
        elif self.match("blank"):
            self.match("Identifier")
            self.var_seq_func_tail()
            self.match("#")
            return self.success
        else: return self.failed()


    
    # def function_prototype(self):
    #     if self.yeet_type()==self.success:
    #         if self.match("Identifier"):
    #             if self.match("("):
    #                 self.parameter()
    #                 if self.match(")"):
    #                     if self.func_def_tail_new()==self.success:
    #                         return self.success
    #                     elif self.match("#"):
    #                         return self.success
    #                     else: return self.failed()
    #     else: return self.failed()

    # def func_def_tail_new(self):
    #     if self.match("{"):
    #         self.statement()
    #         self.match("}")
    #         return self.success
    #     else: return self.failed()
    




    #deprecated?
    def var_seq_func_tail(self):
        if self.var_seq_def()==self.success:
            return self.success
        else: self.failed()

    #deprecated?
    def var_seq_def(self):
        if self.seq_tail()==self.success:
            return self.success
        elif self.vardec_tail()==self.success:
            return self.success
        else: return self.failed()

    #deprecated?
    def charr_gbl_tail(self):
        if self.vardec_tail()==self.success:
            return self.success
        


    @nullable
    def parameter(self):
        if self.all_dtype()==self.success:
            # self.enforce
            self.match("Identifier")
            self.more_paramtail()
            return self.success
        elif self.match("blank"):
            return self.success
        else: return self.failed()
#
    @nullable
    def more_param(self):
        if self.match(",", True):
            self.enforce()
            self.parameter()
            # self.more_paramtail()
            return self.success
        else: return self.failed()

    @nullable
    def more_paramtail(self):
        if self.more_param()==self.success:
            return self.success
        else: return self.failed()

    
    def yeet_type(self):
        if self.all_dtype()==self.success or self.match("blank", True):
            return self.success
        else:
            return self.failed()

    
    def all_dtype(self):
        # self.enforce()
        if self.seq_dtype()==self.success:
            return self.success
        elif self.match("charr"):
            self.enforce()
            if self.match("text"): #issue
                    return self.success
            else: return self.failed() 
        else:
            return self.failed()
        
    
    def seq_dtype(self):
        dtypes=["whole", "dec", "text", "sus"]
        for type in dtypes:
            if self.match(type, True):
                return self.success
        
        return self.failed()
    

    # @nullable
    # def all_literal_arg(self):
    #     if (self.all_literal()==self.success) or (self.match("blank", True)):
    #         return self.success
    #     else: return self.failed()


    def all_literal(self):
        if (self.seq_literal()==self.success):
            return self.success
        elif self.match("Charr", True):
            return self.success
        else: return self.failed()
        
    
    def seq_literal(self):
        seqlits=["Text", "Whole", "Dec", "Sus"]
        if self.match("Text", True) or self.match("Whole", True) or self.match("Dec",True) or self.match("Sus", True):
            return self.success
        else:
            return self.failed()
    
    def numeric_value(self):
        if self.peek() in ["Whole", "Dec", "Identifier"]:
            if self.match("Whole", True) or self.match("Dec", True) or (self.common_val()==self.success) :
                return self.success
            else: return self.failed()

    @require
    def sheesh_declaration(self):
        if self.match('sheesh'):
            self.match('(')
            self.match(')')
            self.match("{")
            if self.statement()!=self.success:
                self.enforce()
                self.failed()
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

    
    def single_statement(self):
        if self.allowed_in_loop()==self.success:
            return self.success
        elif self.control_flow_statement()==self.success:
            return self.success
        else: 
            # self.isnullable=False
            return self.failed()

    
    @nullable
    def allowed_in_loop(self):
        # allowed_statements = [
        #     self.var_or_seq_dec,
        #     self.looping_statement,
        #     self.yeet_statement,
        #     self.io_statement,
        #     self.seq_use_assign,
        #     self.variable_reassign,
        #     self.function_invocation
        # ]
        
        # for statement in allowed_statements:
        #     if statement() == self.success:
        #         if statement == self.variable_reassign or statement == self.function_invocation:
        #             self.match("#")
        #         return self.success
        if (self.var_or_seq_dec()==self.success) or (self.looping_statement()==self.success) or (self.yeet_statement()==self.success) or (self.io_statement()==self.success):
            return self.success
        elif self.match("Identifier", True):
            self.id_tail()
            return self.success
        else: return self.failed()
        
    def reg_body(self):
        if self.match("{"):
            self.statement()
            self.match("}")
            return self.success
        else: return self.failed()
    

    def in_loop_body(self):
        if self.match("{"):
            self.loop_body()
            self.match("}")
            return self.success
        else: return self.failed()
        
        # return self.failed()
    def id_tail(self):
        if self.match("("):
            self.func_argument()
            self.match(")")
            self.match("#")
            return self.success
        elif self.seq_one_dim()==self.success:
            self.assign_op()
            self.assign_value()
            self.match("#")
            return self.success
        elif self.assign_op()==self.success:
            self.assign_value()
            self.match("#")
            return self.success
        else: return self.failed()

    @nullable
    def more_statement(self):
        # nullable=True
        # if len(self.tokens)>0 and self.tokens[0]!="}":
            if self.statement()==self.success:
                return self.success
            else: return self.failed()

    
    def io_statement(self):
        if self.pa_mine_statement()==self.success:
            return self.success
        elif self.up_statement()==self.success:
            return self.success
        else: return self.failed()

    
    def pa_mine_statement(self):
        if self.match("pa_mine", True):
            self.enforce()
            if self.match("("):
                if self.argument():
                    if self.match(")"):
                        if self.match("#"):
                            return self.success
                        else: return self.failed()
                    else: return self.failed()
                else: return self.failed()
            else: return self.failed()
        else: return self.failed()

    
    def up_statement(self):
        if self.match("up", True):
            self.enforce()
            if self.match("("):
                if self.func_argument():
                    # self.enforce()
                    if self.match(")"):
                        if self.match("#"):
                            return self.success
        else: return self.failed()

    
    
    def var_or_seq_dec(self):
        if self.var_seq_common()==self.success:
            if self.var_seq_tail()==self.success:
                self.match("#")
                return self.success
        elif self.match("charr"):
            if self.match("text"):
                if self.match("Identifier"):
                    self.vardec_tail()
                    self.match("#")
                    return self.success
        else: return self.failed()

    def var_seq_common(self):
        if self.seq_dtype()==self.success:
            self.match("Identifier")
            return self.success
        # elif self.var_seq_def()==self.success:
        #     return self.success
        else: return self.failed()

    def var_seq_tail(self):
        if (self.vardec_tail()==self.success) or (self.seq_tail()==self.success):
            return self.success
        elif self.variable_assign()==self.success:
            self.more_vardec()
            return self.success
        else:
            return self.failed()
    


    @nullable #deprecated
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
        # self.isnullable=False
        if self.match("="):     
            self.enforce()
            self.assign_value()
            return self.success
        else: 
            return self.failed()

    @nullable
    def id_as_val(self):
        if self.match("Identifier"):
            self.id_val_tail()
            return self.success
        else: return self.failed()

    @nullable
    def id_val_tail(self):
        if self.match("(", True):
            self.func_argument()
            self.match(")")
            return self.success
        elif self.seq_one_dim()==self.success:
            return self.success
        else: return self.failed()

    #deprecated
    def variable_reassign(self):
        if self.match("Identifier", True):
            self.enforce()
            self.assign_op()
            self.assign_value()
            return self.success
        else: return self.failed()

    #deprec
    def common_val(self):
        if self.peek()=="Identifier":
            if self.match("Identifier"):
                    self.common_val_tail()
                    return self.success
            #self.match("Identifier") or 
            else: return self.failed()

    # def assign_value_tail(self):
    @nullable
    #deprec
    def common_val_tail(self):
        if self.match("("):
            self.func_argument()
            self.match(")")
            return self.success
        elif self.seq_one_dim()==self.success:
            return self.successa
        else: return self.failed()  

    @nullable
    def assign_value(self):
        if self.id_as_val()==self.success:
            self.all_op()
            return self.success
        elif self.numeric_value()==self.success:
            self.math_or_rel_expr()
            return self.success
        elif self.logical_not_expression()==self.success:
            self.logic_op()
            return self.failed()
        elif self.match("Sus", True):
            self.logic_op()
            return self.success
        elif self.match("Text"):
            self.text_op()
            return self.success
        elif self.match("Charr"):
            self.match("==")
            self.match("Charr")
        elif self.pa_mine_statement()==self.success:
            return self.success
        elif self.a_val_withparen()==self.success:
            return self.success
        else: return self.failed()
        # self.isnullable=False
        
        
        # if (self.all_literal_arg() == self.success):
        #     return self.success
        # elif (self.common_val() == self.success):
        #     return self.success 
        # elif (self.expression()==self.success):
        #     return self.success
        # elif(self.seq_use()==self.success):
        #     return self.success
        # else: 
        #     return self.failed()
        # if self.peek()=="Identifier":
        #     if (self.peek(1) in ["(", "[", ")"]):
        #         self.common_val()
        #         return self.success
        #     else:
        #         self.expression() #fixing
        #         return self.success
        
        # elif self.peek() in ["Whole", "Dec", "Text", "Sus", "Charr"]:
        #     if self.peek(1) in ["+", "-", "*", "/", "|", "&", "!", "==", ">", "<", ">=", "<=", "!=", ]:
        #         self.expression()
        #         return self.success
        #     else: 
        #         self.all_literal()
        #         return self.success

        # else: return self.failed()

        # if self.match("Identifier"):
        #     if self.peek() in ["+", "-", "*", "/", "%"]:
        #         self.arithmetic_expression()
        #         return self.success
        #     elif self.peek in ["&", "!", "|"]:
        #         self.logical_expression()
        #         return self.success
        #     elif self.peek in ["(", "[", ]:
        #         self.common_val_tail()
        #         return self.success
        #     else: return f
    
    # def common_val2(self):
    #     if self.match("Identifier"):
    #         if self.common_val_tail()==self.success:
    #             return self.success
    #         else: return self.failed()
    #     else: return self.failed()

    def a_val_withparen(self):
        if self.match("("):
            self.assign_value() 
            self.match(")")
            return self.success
    def constant_declaration(self):
        if self.match("based", True):
            self.const_type()
        else: return self.failed()

    def const_type(self):
        if self.var_seq_common()==self.success:
            self.const_tail()
            return self.success
        elif self.match("charr", True):
            self.match("text")
            self.match("Identifier")
            self.const_var_tail()
            return self.success
        else: return self.failed()
    # def const_seq(self):
    #     if self.match("based"):
    #         pass
    
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

    
    def const_var_tail(self):
        if self.match("=", True):
            self.assign_value()
            self.more_const()
            return self.success
        else: return self.failed()    

    @nullable
    def more_const(self):
        if self.match(",", True):
            self.const_var_tail()
            return self.success
        else: return self.failed()

    
    def assign_op(self): #issue
        aops=["=","+=","-=","*=","/=", "%="]
        for op in aops:
            if self.match(op):
                return self.success
        return self.failed()

    
    # def function_invocation(self):
    #     if self.match("Identifier", True):
    #         if self.match("("):
    #             self.func_argument()
    #             self.match(")")
    #         else: return self.failed()
    #         return self.success
    #     else: return self.failed()

    @nullable
    def func_argument(self):
        # nullable=True 
        if self.argument()==self.success:
            return self.success
        else: return self.failed()

    @nullable
    def argument(self):
        if self.assign_value()==self.success:
            self.more_args()
            return self.success
        else: return self.failed()

    #deprec
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

    
    def control_flow_statement(self):
        if self.match("kung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.reg_body()
            self.cond_tail()
            return self.success
        elif self.match("choose"):
            self.match("(")
            self.match("Identifier")
            self.match(")")
            self.match("{")
            self.when_statement()
            self.choose_default()
            self.match("}")
            return self.success
        else: return self.failed()

    #deprec
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


    def ehkung_statement(self):
        if self.match("ehkung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.reg_body()
            return self.success
        else: return self.failed()

    # def cond_tail(self):
    
    def deins_statement(self):
        if self.match("deins"):
            self.reg_body()
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

    
    def more_condtail(self):
        if self.cond_tail()==self.success:
            return self.success
        else: return self.failed() 

    
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

    
    def when_statement(self):
        if self.match("when"):
            self.all_literal()
            self.match("::")
            self.statement_for_choose()
            self.more_when()
            return self.success
        else: return self.failed()

    
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

    
    def looping_statement(self):
        if (self.bet_statement()==self.success) or (self.for_statement()==self.success):
            return self.success
        else: return self.failed()

    
    def bet_statement(self):
        if self.match("bet", True):
            self.in_loop_body()
            self.match("whilst")
            self.match("(")
            self.condition()
            self.match(")")
            self.match("#")
            return self.success
        else: return self.failed()
        

    
    def for_statement(self):
        if self.match("for", True):
            self.match("(")
            self.match("Identifier")
            self.match("=")
            self.for_initial_val()
            self.match("to")
            self.for_initial_val()
            self.step_statement()
            self.match(")")
            self.in_loop_body()
            return self.success
        else: return self.failed()

    #deprec
    def end_val(self):
        if self.for_initial_val()==self.success:
            return self.success
        else: return self.failed()

    def for_initial_val(self):
        if self.num_or_arithmexpr()==self.success:
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
            self.in_loop_body()
            self.in_loop_condtail()
            return self.success
        else: return self.failed()

    def loop_ehkung(self):
        if self.match("ehkung"):
            self.match("(")
            self.condition()
            self.match(")")
            self.in_loop_body()
            return self.success
        else: return self.failed()


    # deprec
    def loop_deins(self):
        if self.match("deins"):
            self.in_loop_body()
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
        if self.logicval_or_expr()==self.success:
            return self.success
        else: return self.failed()

    #deprec
    def sequence_declaration(self):
        if (self.seq_dtype()==self.success):
            self.match("Identifier")
            self.seq_tail()
            self.match("#")
            return self.success
        else: return self.failed()

    #deprec 
    def seq_tail(self):
        if (self.seq_one_dim()==self.success):
            self.seq_assign()
            return self.success
        elif (self.multi_dim()==self.success):
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

    def multi_dim(self):
        if self.seq_one_dim()==self.success:
            self.more_seqtail()
            return self.success
        else: return self.failed()

    @nullable
    def more_seq(self):
        if self.match(","):
            self.enforce()
            if self.match("Identifier"):
                self.multi_dim()
                return self.success
            else: return self.failed()
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
            self.num_or_arithmexpr()
            self.match("]")
            return self.success
        else: return self.failed()
    
    def num_or_arithmexpr(self):
        if self.arithm_term()==self.success:
            self.arithm_addtail()
            return self.success

    # deprec
    def seq_index_val(self):
        if (self.common_val()==self.success) or self.match("Whole") or (self.arithmetic_expression()==self.success):
            return self.success
        else: return self.failed()

    # deprec1
    def seq_use(self):
        if self.peek()=="Identifier" and self.peek(1)=="[":
            if self.match("Identifier") and self.tokens[1]=="[":
                self.seq_one_dim()
                return self.success
            else: return self.failed()

    # Deprec 
    def seq_use_assign(self):
        if self.seq_use()==self.success:
            self.assign_op()
            self.assign_value()
            if self.match("#"):
                return self.success
        else: return self.failed()

    # deprec
    def expression(self): #issue, sus
        # if (self.arithmetic_expression()==self.success) or (self.logical_expression()==self.success) or (self.relational_expression()==self.success) or (self.text_concat()==self.success):
        #     return self.success
        # else: return self.failed()
        if self.peek()=="Identifier" or self.peek() in ["Whole", "Dec", "Text", "Sus", "Charr"]:
            if self.peek(1) in ["+", "-", "*", "/", "%"]:
                self.arithmetic_expression()
                return self.success
            elif self.peek(1) in ["&", "!", "|"]:
                self.logical_expression()
                return self.success
            elif (self.peek()=="Text") and (self.peek(1) in ["...", ]):
                self.text_concat()
                return self.success
            elif self.peek(1) in ["==", ">", ">=", "<", "<=", "!="]:
                self.relational_expression()
                return self.success
            else: return
        elif self.peek()=="(":
            if self.peek(1)=="Identifier" or self.peek(1) in ["Whole", "Dec", "Text", "Sus", "Charr"]:
                if self.peek(2) in ["+", "-", "*", "/", "%"]:
                    self.arithmetic_expression()
                    return self.success
                elif self.peek(2) in ["&", "!", "|"]:
                    self.logical_expression()
                    return self.success
                elif self.peek(2) in ["==", ">", ">=", "<", "<=", "!="]:
                    self.relational_expression()
                    return self.success
                else: return self.failed()
        else: return self.failed()
        
    # deprec 
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
        if self.numeric_value()==self.success:
            return self.success
        elif self.id_as_val()==self.success:
            return self.success
        elif self.match("("):
            self.num_or_arithmexpr()
            self.match(")")
            return self.success
        else: return self.failed()    

    def arithm_tail(self):
        if self.add_op()==self.success:
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
        if  self.num_or_arithmexpr()==self.success:
            self.relop()
            self.num_or_arithmexpr()
            return self.success
        elif self.match("Charr"):
            self.match("==")
            self.match("Charr")
        else: return self.failed()

    # deprec 
    def relexrp_with_paren(self):
        if self.match("("):
            self.relational_expression()
            self.match(")")
            return self.success
        else: return self.failed()

    # deprec 
    def relexrp_without_paren(self):
        if self.peek() in ["Whole", "Dec", "Identifier"] and (self.peek(1) in ["==", ">", ">=", "<", "<=", "!="]):
            if (self.numeric_value()==self.success):
                self.relop()
                self.numeric_value()
                return self.success
            elif (self.charr_val()==self.success):
                self.match("==")
                self.charr_val()
                return self.success
            else: return self.failed()

    # deprec 
    def charr_val(self):
        if self.peek() in ["Charr", "Identifier"]:
            if (self.common_val()==self.success) or self.match("Charr"):
                return self.success
            else: return self.failed()

    def relop(self):
        if self.match("==") or self.match(">") or self.match(">=") or self.match("<") or self.match("<=") or self.match("!="):
            return self.success
        else: return self.failed()

    def logicval_or_expr(self):
        if self.logic_term()==self.success:
            self.logic_ortail()
            return self.success
        else: return self.failed()
    
    # deprec 
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
        if self.peek("("):
            self.match("(")
            self.logicval_or_expr()
            self.match(")")
            return self.success
        elif (self.logic_value()==self.success) or (self.logical_not_expression()==self.success):
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
        if self.match("!"):
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
            # if self.peek()=="Identifier":
            #     if self.peek(1) in ["==", ">", ">=", "<", "<=", "!="]:
            #         (self.relational_expression()==self.success)
            #         return self.success
            #     elif self.peek(1) in ["(", "["]:
            #         (self.common_val()==self.success)
            #         return self.success
            #     else: return 
            # elif self.peek() in ["Whole", "Dec", "Text", "Sus", "(", ""]:
            #     if self.peek(1) in ["==", ">", ">=", "<", "<=", "!="]:
            #         (self.relational_expression()==self.success)
            #         return self.success
            #     else:
            #         self.match("Sus", True)
            #         return self.success
            # elif self.peek()=="!":
            #         (self.logical_not_expression()==self.success)
            #         return self.success
            # else: return self.failed()
        if self.id_as_val()==self.success:
            self.rel_expr_tail()
            return self.success
        elif self.match("Sus"):
            return self.success
        elif self.relational_expression()==self.success:
            return self.success
        else: return self.failed()
            
    #deprec
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
        if self.match("Text") or self.id_as_val()==self.success:
            return self.success
        else: return self.failed()

    @nullable
    def function_definition(self):
        if self.func_def()==self.success:
            self.more_funcdef()
            return self.success
        else: return self.failed()

    
    def func_def(self):
        if self.match("def"):
            self.yeet_type()
            self.funcproto_tail()
            if self.peek()=="{":
                self.reg_body()
                return self.success
            else: 
                self.match("#")
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

    def all_op(self):
        if self.math_or_rel_expr()==self.success:
            return self.success
        elif self.logic_op()==self.success:
            return self.success
        elif self.text_op()==self.success:
            return self.success
        else: return self.failed()
    
    @nullable
    def math_or_rel_expr(self):
        if self.math_op()==self.success:
            return self.success
        elif self.rel_expr_tail()==self.success:
            return self.success
        else: return self.failed()

    def math_op(self):
        if self.add_op()==self.success:
            self.num_or_arithmexpr()
            return self.success
        elif self.mult_op()==self.success:
            self.num_or_arithmexpr()
            return self.success
        else: return self.failed()
    
    def rel_expr_tail(self):
        if self.relop()==self.success:
            self.rel_val()
            return self.success
        else: return self.failed()
    
    @nullable
    def logic_op(self):
        if self.match("|"):
            self.logicval_or_expr()
            return self.success
        elif self.match("&"):
            self.logicval_or_expr()
            return self.success
        else: return self.failed()

    @nullable
    def text_op(self):
        if self.concat_tail()==self.success:
            return self.success
        else: return self.failed()

    def rel_val(self):
        if self.numeric_value()==self.success:
            return self.success
        elif self.id_as_val()==self.success:
            return self.success
        elif self.match("Charr"):
            return self.success
        else: return self.failed()