from source import helper
from source.LexicalAnalyzer.tokenclass import Token
import source.core.error_handler as err

'''
General Logic:
1. The Parser class serves as the base for all of the other non-terminal parsers.
2. Each non-terminal in the grammar has a corresponding parser class.
3. Each parser class has a parse method that returns an instance of the class.
4. The non-terminal parser breaks up each production into smaller parts and calls the corresponding parser for each part.
5. It recursively breaks down each one until it reaches the terminal symbols.
6. The parser class has a match method that checks if the current token matches the expected token.
7. If it does, it moves to the next token. If it doesn't, it raises a syntax error.
8. The parser class also has a peek method that returns the next token without moving to the next token.
9. The parser class has a move method that moves to the next token.
10. The parser class has a parse method that returns the abstract syntax tree (AST) of the program.

General Parse Algorithm:
1. Match tokens with the expected tokens in the grammar.
2. If the token matches, move to the next token.
3. If the token doesn't match with anything, raise a syntax error.
4. If the token matches, call the corresponding parser for the next part of the production.

*Each method should match its expected token and call the corresponding parser for the next part of the production.     

'''



class Parser:
    cur_tok_ptr=0
    #parser that parses from a list of token objects.
    #final output of the parser should be an abstract syntax tree.
    def __init__(self, tokens:list[Token]) -> None:
        self.tokens = tokens
        self.error=False
        self.parsed=None
        # self.arithm=self.ParseArithmOp(self.tokens)
  
    def move(self):
        Parser.cur_tok_ptr+=1
    
    def peek(self):
        try:
            return self.tokens[self.cur_tok_ptr+1]
        except IndexError:
            return None
    
    def match(self, token_type):
        if self.peek().type == token_type:
            self.move()
            print("Matched")
        else:
            self.error=True
            print("Error")

    def parse(self):
        return AbstractSyntaxTree(Program(self.tokens))
        # while not self.error:
        #     par=Program()
        #     self.parsed=par
        # else:
        #     #display error message of the syntax error; stop syntax analysis from that point onwards.
        #     error=err.SyntaxError("Syntax Error")


class Program(Parser):
    #<program>	→	<import><global_declaration><function_definition><sheesh_declaration><function_definition>

    def __init__(self, imp=None, glob_dec=None, func_def_pre=None, sheesh_dec=None, func_def_post=None ) -> None:
        super().__init__(tokens=self.tokens)
        self.imp=None
        self.glob_dec=None  
        self.func_def_pre=None
        self.sheesh_dec=None
        self.func_def_post=None

    def __repr__(self) -> str:
        return f"Program: ({self.imp}), ({self.glob_dec}), ({self.func_def_pre}), ({self.sheesh_dec}), ({self.func_def_post})"

    def parse(self):
        self.imp=Import(self.tokens).parse()
        self.glob_dec=GlobalDec(self.tokens).parse()
        self.func_def_pre=FuncDef().parse()
        self.sheesh_dec="Parsing SheeshDec"
        self.func_def_post="Parsing FuncDefPost"
        return Program(self.imp, self.glob_dec, self.func_def_pre, self.sheesh_dec, self.func_def_post)
        

class Import(Parser):
    #implement parse: import prog, next, more
    # productions: 
    # <import>	→	use <import_prog><import_next>#<more_import>
    # <import>	→	λ
    # <more_import>		<import>
    # <more_import>		λ
    # <import_prog>	→	identifier <more_importprog>
    # <more_importprog>	→	, <import_prog>
    # <more_importprog>	→	λ
    # <import_next>	→	from identifier
    # <import_next>	→	λ

    def __init__(self, tokens, import_prog, import_next=None, more_import=None) -> None:
        self.tokens=tokens
        self.use="use"
        self.import_prog=import_prog
        self.import_next=import_next
        self.hash="#"
        self.more_import=more_import
        

    def __repr__(self) -> str:
        return f"Import: ( {self.use}, ({self.import_prog}), ({self.import_next}), ({self.hash}), ({self.more_import}))"

    def parse(self):
        if self.match("use"):
            if self.peek().type== "Identifier":
                self.move()

            import_prog=self.parse_import_prog()
            import_next=self.parse_import_next()
            more_import=self.parse_more_import()
            return Import(import_prog, import_next, more_import)

class GlobalDec(Parser):
    #productions:
    # <global_declaration>	→	<global_statement><global_declaration> (LEFT RECURSION)
    # <global_declaration>	→	λ
    # <global_statement>	→	<variable_declaration>
    # <global_statement>	→	<function_prototype>
    # <global_statement>	→	<constant_declaration>
    # <global_statement>	→	<sequence_declaration>
    # ~~~~ suggested: moreglobstmt -> globdec


    def __init__(self, global_stmt,more_global_dec) -> None:
        self.global_stmt=global_stmt
        self.more_global_Dec=more_global_dec
    
    def __repr__(self) -> str:
        return f"GlobalDec: ({self.global_stmt}, {self.more_global_Dec})"
    
    def parse(self):
        pass

class FuncProto(Parser):
    #productions:
    # <function_prototype>	→	<yeet_type> identifier ( <parameter> ) #
    # <parameter>	→	<data_type> identifier <more_param>
    # <parameter>	→	blank
    # <parameter>	→	λ
    # <more_param>	→	,<data_type> identifier <more_param>
    # <more_param>	→	λ
    # <yeet_type>	→	<data_type>
    # <yeet_type>	→	blank
    # <data_type>	→	whole
    # <data_type>	→	dec
    # <data_type>	→	text
    # <data_type>	→	sus
    # <data_type>	→	charr text

    def __init__(self) -> None:
        pass

class SheeshDec(Parser):
    #productions:
    # <sheesh_declaration>	→	sheesh(){<statement>}
    # <statement>	→	<single_statement><more_statement>
    # <single_statement>	→	<variable_declaration>
    # <single_statement>	→	<sequence_declaration>
    # <single_statement>	→	<function_invocation>#
    # <single_statement>	→	<control_flow_statement>
    # <single_statement>	→	<yeet_statement>
    # <single_statement>	→	<io_statement>
    # <single_statement>	→	<seq_use_assign>
    # <single_statement>	→	<variable_reassign>#
    # <more_statement>	→	<statement>
    # <more_statement>	→	λ

    def __init__(self) -> None:
        pass

class FuncDef(Parser):
    def __init__(self) -> None:
        pass

class Statement(Parser):
    #production:
    # <statement>	→	<single_statement><more_statement>
    # <more_statement>	→	<statement>
    # <more_statement>	→	λ
    def __init__(self) -> None:
        pass

class SingleStatement(Parser):
    #productions:
    # <single_statement>	→	<variable_declaration>
    # <single_statement>	→	<sequence_declaration>
    # <single_statement>	→	<function_invocation>#
    # <single_statement>	→	<control_flow_statement>
    # <single_statement>	→	<yeet_statement>
    # <single_statement>	→	<io_statement>
    # <single_statement>	→	<seq_use_assign>
    # <single_statement>	→	<variable_reassign>#
    def __init__(self) -> None:
        pass

class VariableDec(Parser):
    '''productions:
        <variable_declaration>	→	<data_type><vardec_tail>#
        <vardec_tail>	→	identifier<variable_assign><more_vardec>
        <more_vardec>	→	,<vardec_tail>
        <more_vardec>	→	λ
        <variable_assign>	→	:= <assign_value>
        <variable_assign>	→	λ
        <variable_reassign>	→	identifier <assign_op><assign_value>
    '''

    def __init__(self) -> None:
        pass

class SequenceDec(Parser):
    '''productions:
        <sequence_declaration>	→	<data_type> identifier <seq_tail>#
        <seq_tail>	→	<seq_one_dim><seq_assign>
        <seq_tail>	→	<multi_seq>
        <seq_assign>	→	:=<seq_init>
        <seq_assign>	→	λ
        <seq_init>	→	{<seq_elem>}
        <seq_elem>	→	<seq_elem_value>
        <seq_elem>	→	<seq_init><seq_two-d_init>
        <seq_two-d_init>	→	,<seq_init><seq_three-d_init>
        <seq_three-d_init>	→	,<seq_init>
        <seq_two-d_init>	→	λ
        <seq_three-d_init>	→	λ
        <seq_elem_value>	→	<literal><next_elem_value>
        <next_elem_value>	→	,<seq_elem_value>
        <next_elem_value>	→	λ
        <multi_seq>	→	<seq_one_dim><more_seq>
        <more_seq>	→	,identifier <seq_one_dim><more_seq>
        <more_seq>	→	λ
        <seq_one_dim>	→	<index><seq_two_dim>
        <seq_two_dim>	→	<index><seq_three_dim>
        <seq_three_dim>	→	<index>
        <seq_two_dim>	→	λ
        <seq_three_dim>	→	λ
        <index>	→	[<seq_index_val>]
        <seq_index_val>	→	<function_invocation>
        <seq_index_val>	→	identifier 
        <seq_index_val>	→	whole_literal 
        <seq_index_val>	→	<arithmetic_expression>
        <seq_use>	→	identifier<seq_one_dim>
        <seq_use_assign>	→	<seq_use><assign_op><assign_value>#
    '''

class FuncInvoc(Parser):
    '''
    productions:
        <function_invocation>	→	identifier ( <func_argument> )
        <func_argument>	→	<argument>
        <func_argument>	→	λ
        <argument>	→	<args_value><more_args>
        <args_value>	→	<assign_value>
        <more_args>	→	, <argument>
        <more_args>	→	λ

    '''
    def __init__(self) -> None:
        pass

class ControlFlow(Parser):
    '''
    productions:
        <control_flow_statement>	→	<kung_statement><more_control_flow>
        <control_flow_statement>	→	<choose_statement>
        <control_flow_statement>	→	<looping_statement>
        <kung_statement>	→	kung ( <condition> ) { <statement> }
        <ehkung_statement>	→	ehkung ( <condition> ) { <statement> }
        <deins_statement>	→	deins { <statement>}
        <more_control_flow>	→	<ehkung_statement><more_control_flow>
        <more_control_flow>	→	<deins_statement>
        <more_control_flow>	→	λ
        <choose_statement>	→	choose ( identifier ) {<when_statement><choose_default>}
        <when_statement>	→	when <literal> :: <statement_for_choose><more_when>
        <statement_for_choose>	→	<statement>
        <statement_for_choose>	→	felloff#
        <more_when>	→	<when_statement>
        <more_when>	→	λ
        <choose_default>	→	default :: <statement_for_choose>
        <choose_default>	→	λ
        <looping_statement>	→	<bet_statement>
        <looping_statement>	→	<for_statement>
        <habang_statement>	→	bet { <within_loop_statement> } kung(<condition>)#
        <for_statement>	→	for( identifier = <for_initial_val> to <end_val> <step_statement> ) { <within_loop_statement> }
        <for_initial_val>	→	whole_literal
        <for_initial_val>	→	<common_val>
        <for_initial_val>	→	<arithmetic_expression>
        <for_initial_val>	→	<seq_use>
        <step_statement>	→	step <for_initial_val>
        <step_statement>	→	λ
        <within_loop_statement>	→	<kung_statement><loop_more_control_flow>
        <within_loop_statement>	→	<ehkung_statement><loop_more_control_flow>
        <within_loop_statement>	→	<deins_statement>
        <within_loop_statement>	→	λ
        <loop_kung>	→	kung ( <condition> ) { <has_loop_control>}
        <loop_ehkung>	→	ehkung ( <condition> ) {<has_loop_control>}
        <loop_deins>	→	deins { <has_loop_control>}
        <loop_more_control_flow>	→	<loop_ehkung><more_control_flow>
        <loop_more_control_flow>	→	<loop_deins>
        <loop_more_control_flow>	→	λ
        <has_loop_control>	→	<statement>
        <has_loop_control>	→	<loop_control_statement><more_statement>
        <loop_control_statement>	→	felloff#
        <loop_control_statement>	→	pass#
        <loop_control_statement>	→	λ
        <condition>	→	<relational_expression>
        <condition>	→	<logical_expression>
        <condition>	→	lit_literal
        <condition>	→	<common_val>
        <condition>	→	<function_invocation>
    '''

    def __init__(self) -> None:
        pass

class Yeet(Parser):
    '''
    productions:
        <yeet_statement>	→	yeet <return_value>#
        <yeet_statement>	→	λ
    '''

    def __init__(self) -> None:
        pass

class IOStatement(Parser):
    '''
    <io_statement>	→	<pa_mine_statement>
    <io_statement>	→	<up_statement>
    <pa_mine_statement>	→	pa_mine(<argument>)#
    <up_statement>	→	up(<func_argument>)#
    '''
    def __init__(self) -> None:
        pass

class SeqUseAssign(Parser):
    '''
    <seq_use_assign>	→	<seq_use><assign_op><assign_value>#
    '''
    def __init__(self) -> None:
        pass

class VariableReassign(Parser):
    '''
    <variable_reassign>	→	identifier <assign_op><assign_value>
    '''
    def __init__(self) -> None:
        pass




class Expression(Parser):
    def __init__(self, expr, op, expr2) -> None:
        self.expr=expr
        self.op=op
        self.expr2=expr2

    def parseExpr(self):
        pass

class AbstractSyntaxTree:
    #Attach the root (program) to the instance of this AST class. Printing this AST should recursively print 
    # the children within the nodes
    def __init__(self, root:Program ) -> None:
        self.root=root

    def __repr__(self) -> str:
        return f"AST: {self.root}"
        
   
# def main():
#     tokens=[Token("use", "use"), Token("identifier", "identifier")]
#     test=Parser(tokens)
#     test.match("use")
#     print(test.current)

# main()
