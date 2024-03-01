# from source import helper
import sys
sys.path.append( '.' )
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
        if Parser.cur_tok_ptr<len(self.tokens)-1:
            Parser.cur_tok_ptr+=1
        else:
            print("Length")
    
    def peek(self):
        try:
            return self.tokens[self.cur_tok_ptr+1].type
        except IndexError:
            return None

    def match(self, token_type):
        #matches first token seen.
        if self.tokens[self.cur_tok_ptr].type == token_type:
            self.move()
            return True
        else:
            return False

    def current(self):
        return self.tokens[self.cur_tok_ptr]
    
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

    def __init__(self, parser:Parser=None, imp=None, glob_dec=None, func_def_pre=None, sheesh_dec=None, func_def_post=None ) -> None:
        self.tokens=parser.tokens
        self.cur_tok_ptr=parser.cur_tok_ptr
        self.imp=imp
        self.glob_dec=glob_dec  
        self.func_def_pre=func_def_pre
        self.sheesh_dec=sheesh_dec
        self.func_def_post=func_def_post

    def __repr__(self) -> str:
        return f"Program: ({self.imp}), ({self.glob_dec}), ({self.func_def_pre}), ({self.sheesh_dec}), ({self.func_def_post})"

    def parse(self):
        self.imp="Import in Development" #Import(self.parser)
        self.glob_dec="Global Dec in Development" #GlobalDec()
        self.func_def_pre="Func Def in Development" #FuncDef()
        self.sheesh_dec=SheeshDeclaration(self)
        self.func_def_post="Func Def in Development" #FuncDef()
        # return Program(self.imp, self.glob_dec, self.func_def_pre, self.sheesh_dec, self.func_def_post)
        

class Import(Parser):

    def __init__(self, parser: Parser=None,use=None, import_prog=None, import_next=None, hash=None, more_import=None) -> None:
        self.tokens=parser.tokens
        self.cur_tok_ptr=parser.cur_tok_ptr
        self.use=use
        self.import_prog=import_prog
        self.import_next=import_next
        self.hash=hash
        self.more_import=more_import
        

    def __repr__(self) -> str:
        return f"Import: ( {self.use}, ({self.import_prog}), ({self.import_next}), ({self.hash}), ({self.more_import}))"
        # return f"Parsing Import"

    def parse(self):
        '''
        to parse:
        1. Match terminal token "use"
        2. If match, proceed to next token/production, else, check if there is no import statement
        '''
        buffer=None
        if self.match("use"):
            self.use="use"
            self.import_prog=ImportProg(self.parser)
            self.import_next=ImportNext(self.parser)
            self.hash="#"
            self.more_import=MoreImport(self.parser)
        else: return None #no import statement

            # return Import(import_prog, import_next, more_import)


class MoreImport(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing More Import"
    
    def parse(self):
        pass


class ImportProg(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Import Prog"
    
    def parse(self):
        pass


class MoreImportProg(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing More Import Prog"
    
    def parse(self):
        pass


class ImportNext(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Import Next"
    
    def parse(self):
        pass


class GlobalDeclaration(Parser):
    #productions:
    # <global_declaration>	→	<global_statement><global_declaration> (LEFT RECURSION)
    # <global_declaration>	→	λ
    # <global_statement>	→	<variable_declaration>
    # <global_statement>	→	<function_prototype>
    # <global_statement>	→	<constant_declaration>
    # <global_statement>	→	<sequence_declaration>
    # ~~~~ suggested: moreglobstmt -> globdec


    def __init__(self, global_stmt=None, more_global_dec=None) -> None:
        self.global_stmt=global_stmt
        self.more_global_Dec=more_global_dec
        
    
    def __repr__(self) -> str:
        # return f"GlobalDec: ({self.global_stmt}, {self.more_global_Dec})"
        return f"Parsing Global Declaration"
    
    def parse(self):
        pass


class MoreGlobalDec(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing More Global Dec"
    
    def parse(self):
        pass


class GlobalStatement(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Global Statement"
    
    def parse(self):
        pass


class FunctionPrototype(Parser):
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

    def __repr__(self) -> str:
        return f"Parsing Function Prototype"
    
    def parse(self):
        pass


class Parameter(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Parameter"
    
    def parse(self):
        pass


class MoreParam(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing More Param"
    
    def parse(self):
        pass


class MoreParamTail(Parser):

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing More Param Tail"
    
    def parse(self):
        pass


class AllDType(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AllDType"

    def parse(self):
        pass


class SeqDType(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqDType"

    def parse(self):
        pass


class AllLiteral(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AllLiteral"

    def parse(self):
        pass


class SeqLiteral(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqLiteral"

    def parse(self):
        pass


class NumericValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing NumericValue"

    def parse(self):
        pass


class SheeshDeclaration(Parser):
    current=''
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

    def __init__(self, parser:Parser=None, sheesh=None, oparen=None, cparen=None, obrack=None, statement=[], cbrack=None ) -> None:
        self.tokens=parser.tokens
        # self.tokens=parser.tokens
        self.sheesh=sheesh
        self.oparen=oparen
        self.cparen=cparen
        self.obrack=obrack
        self.statement=statement
        self.cbrack=cbrack
 


    def __repr__(self) -> str:
        return f"Sheesh Declaration: ({self.sheesh}) ({self.oparen}) ({self.cparen}) ({self.obrack}) ({self.statement}) ({self.cbrack})"

    def parse(self):
        

        """
        algorithm: look for sheesh, if match, continue matching next. 
        else, no sheesh matched; sytnax error. 
        
        """
        # expected=None
        # if self.match():
        #     expected
        #     self.sheesh="sheesh"
        #     if self.match("("):
        #         self.oparen="("
        #         if self.match(")"):
        #             self.cparen=")"
        #             if self.match("{"):
        #                 self.obrack="{"
        #                 self.statement=Statement(self.parser)
        #                 if self.match("}"):
        #                     self.cbrack="}"

        #                 #parse statement
        #             else: err.SyntaxError(self.tokens[0], self.tokens[0].line, exptected)
        expected=["sheesh", "(", ")", "{", "text", "}"]
        cur=self.current()
        if self.match("sheesh"):
            self.sheesh="sheesh"
            if self.match("("):
                self.oparen="("
                if self.match(")"):
                    self.cparen=")"
                    if self.match("{"):
                        self.obrack="{"
                        while cur!="}":
                            statement=Statement(self)
                            statement.parse()
                            self.statement.append(statement)
                            self.move()
                            statement=''
                        if self.match("}"):
                            self.cbrack="}"
                        else:
                            print(err.SyntaxError(self.tokens[self.cur_tok_ptr].type, self.tokens[self.cur_tok_ptr].line, "}"))
                            return
                    else:
                        print(err.SyntaxError(self.tokens[self.cur_tok_ptr].type, self.tokens[self.cur_tok_ptr].line, "{"))
                        return
                else:
                    print(err.SyntaxError(self.tokens[self.cur_tok_ptr].type, self.tokens[self.cur_tok_ptr].line, ")"))
                    return
            else:
                print(err.SyntaxError(self.tokens[self.cur_tok_ptr].type, self.tokens[self.cur_tok_ptr].line, "("))
                return
        else:
            print(err.SyntaxError(self.tokens[self.cur_tok_ptr].type, self.tokens[self.cur_tok_ptr].line, "sheesh"))
            return
    


    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing All DType"
    
    def parse(self):
        pass            


class Statement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Statement"

    def parse(self):
        pass


class SingleStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SingleStatement"

    def parse(self):
        pass


class AllowedInLoop(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AllowedInLoop"

    def parse(self):
        pass


class MoreStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreStatement"

    def parse(self):
        pass


class IOStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing IOStatement"

    def parse(self):
        pass


class PaMineStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing PaMineStatement"

    def parse(self):
        pass


class UpStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing UpStatement"

    def parse(self):
        pass


class VariableDeclaration(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing VariableDeclaration"

    def parse(self):
        pass


class VarDecTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing VarDecTail"

    def parse(self):
        pass


class MoreVarDec(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreVarDec"

    def parse(self):
        pass


class VariableAssign(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing VariableAssign"

    def parse(self):
        pass


class VariableReassign(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing VariableReassign"

    def parse(self):
        pass


class CommonVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing CommonVal"

    def parse(self):
        pass


class AssignValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AssignValue"

    def parse(self):
        pass


class ConstantDeclaration(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConstantDeclaration"

    def parse(self):
        pass


class ConstSeq(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConstSeq"

    def parse(self):
        pass


class ConstVar(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConstVar"

    def parse(self):
        pass


class ConstTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConstTail"

    def parse(self):
        pass


class MoreConst(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreConst"

    def parse(self):
        pass


class AssignOp(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AssignOp"

    def parse(self):
        pass


class FunctionInvocation(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing FunctionInvocation"

    def parse(self):
        pass


class FuncArgument(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing FuncArgument"

    def parse(self):
        pass


class Argument(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Argument"

    def parse(self):
        pass


class ArgsValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArgsValue"

    def parse(self):
        pass


class MoreArgs(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreArgs"

    def parse(self):
        pass


class ControlFlowStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ControlFlowStatement"

    def parse(self):
        pass


class KungStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing KungStatement"

    def parse(self):
        pass


class EhkungStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing EhkungStatement"

    def parse(self):
        pass


class DeinsStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing DeinsStatement"

    def parse(self):
        pass


class CondTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing CondTail"

    def parse(self):
        pass


class MoreCondTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreCondTail"

    def parse(self):
        pass


class ChooseStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ChooseStatement"

    def parse(self):
        pass


class WhenStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing WhenStatement"

    def parse(self):
        pass


class StatementForChoose(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing StatementForChoose"

    def parse(self):
        pass


class MoreWhen(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreWhen"

    def parse(self):
        pass


class ChooseDefault(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ChooseDefault"

    def parse(self):
        pass


class LoopingStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopingStatement"

    def parse(self):
        pass


class BetStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing BetStatement"

    def parse(self):
        pass


class ForStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ForStatement"

    def parse(self):
        pass


class EndVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing EndVal"

    def parse(self):
        pass


class ForInitialVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ForInitialVal"

    def parse(self):
        pass


class StepStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing StepStatement"

    def parse(self):
        pass


class LoopBody(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopBody"

    def parse(self):
        pass


class LoopBodyStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopBodyStatement"

    def parse(self):
        pass


class MoreLoopBody(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreLoopBody"

    def parse(self):
        pass


class LoopKung(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopKung"

    def parse(self):
        pass


class LoopEhkung(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopEhkung"

    def parse(self):
        pass


class LoopDeins(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopDeins"

    def parse(self):
        pass


class InLoopCondTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing InLoopCondTail"

    def parse(self):
        pass


class MoreInLoopCondTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreInLoopCondTail"

    def parse(self):
        pass


class LoopChoose(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopChoose"

    def parse(self):
        pass


class LoopWhen(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopWhen"

    def parse(self):
        pass


class InLoopWhen(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing InLoopWhen"

    def parse(self):
        pass


class LoopDefault(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopDefault"

    def parse(self):
        pass


class LoopControlStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LoopControlStatement"

    def parse(self):
        pass


class Condition(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Condition"

    def parse(self):
        pass


class SequenceDeclaration(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SequenceDeclaration"

    def parse(self):
        pass


class SeqTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqTail"

    def parse(self):
        pass


class SeqAssign(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqAssign"

    def parse(self):
        pass


class SeqInit(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqInit"

    def parse(self):
        pass


class SeqElem(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqElem"

    def parse(self):
        pass


class SeqTwoDInit(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqTwoDInit"

    def parse(self):
        pass


class SeqThreeDInit(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqThreeDInit"

    def parse(self):
        pass


class SeqElemValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqElemValue"

    def parse(self):
        pass


class NextElemValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing NextElemValue"

    def parse(self):
        pass


class MultiSeq(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MultiSeq"

    def parse(self):
        pass


class MoreSeq(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreSeq"

    def parse(self):
        pass


class MoreSeqTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreSeqTail"

    def parse(self):
        pass


class SeqOneDim(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqOneDim"

    def parse(self):
        pass


class SeqTwoDim(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqTwoDim"

    def parse(self):
        pass


class SeqThreeDim(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqThreeDim"

    def parse(self):
        pass


class Index(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Index"

    def parse(self):
        pass


class SeqIndexVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqIndexVal"

    def parse(self):
        pass


class SeqUse(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqUse"

    def parse(self):
        pass


class SeqUseAssign(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing SeqUseAssign"

    def parse(self):
        pass

class Expression(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Expression"

    def parse(self):
        pass


class ArithmeticExpression(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmeticExpression"

    def parse(self):
        pass


class ArithmTerm(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmTerm"

    def parse(self):
        pass


class ArithmFactor(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmFactor"

    def parse(self):
        pass


class ArithmTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmTail"

    def parse(self):
        pass


class ArithmAddTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmAddTail"

    def parse(self):
        pass


class ArithmTermTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmTermTail"

    def parse(self):
        pass


class ArithmMultTerm(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ArithmMultTerm"

    def parse(self):
        pass


class AddOp(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing AddOp"

    def parse(self):
        pass


class MultOp(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MultOp"

    def parse(self):
        pass


class RelationalExpression(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing RelationalExpression"

    def parse(self):
        pass


class RelexrpWithParen(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing RelexrpWithParen"

    def parse(self):
        pass


class RelexrpWithoutParen(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing RelexrpWithoutParen"

    def parse(self):
        pass


class CharrVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing CharrVal"

    def parse(self):
        pass


class Relop(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing Relop"

    def parse(self):
        pass


class LogicalExpression(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicalExpression"

    def parse(self):
        pass


class LogicTerm(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicTerm"

    def parse(self):
        pass


class LogicFactor(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicFactor"

    def parse(self):
        pass


class LogicTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicTail"

    def parse(self):
        pass


class LogicOrTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicOrTail"

    def parse(self):
        pass


class LogicTermTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicTermTail"

    def parse(self):
        pass


class LogicAndTerm(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicAndTerm"

    def parse(self):
        pass


class LogicalNotExpression(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicalNotExpression"

    def parse(self):
        pass


class LogicNotTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicNotTail"

    def parse(self):
        pass


class LogicNot(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicNot"

    def parse(self):
        pass


class LogicValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing LogicValue"

    def parse(self):
        pass


class TextConcat(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing TextConcat"

    def parse(self):
        pass


class ConcatTail(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConcatTail"

    def parse(self):
        pass


class MoreConcat(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreConcat"

    def parse(self):
        pass


class ConcatVal(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ConcatVal"

    def parse(self):
        pass


class FunctionDefinition(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing FunctionDefinition"

    def parse(self):
        pass


class FuncDef(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing FuncDef"

    def parse(self):
        pass


class MoreFuncDef(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing MoreFuncDef"

    def parse(self):
        pass


class YeetStatement(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing YeetStatement"

    def parse(self):
        pass


class ReturnValue(Parser):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Parsing ReturnValue"

    def parse(self):
        pass


class FuncDef(Parser):
    def __init__(self) -> None:
        pass
    def __repr__(self) -> str:
        return f"Parsing Function Definition"


class Statement(Parser):
    #production:
    # <statement>	→	<single_statement><more_statement>
    # <more_statement>	→	<statement>
    # <more_statement>	→	λ
    def __init__(self, parse: Parser, single_statement=None, more_statement=None) -> None:
        self.parse=parse
        self.tokens=parse.tokens
        self.cur_tok_ptr=parse.cur_tok_ptr
        self.single_statement=single_statement
        self.more_statement=more_statement  

    def __repr__(self) -> str:
        return f"Parsing Statement"
    
    def parse(self):
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

    def __repr__(self) -> str:
        return f"Parsing Single Statement"


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

    def __repr__(self) -> str:
        return f"Parsing Variable Declaration"


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
