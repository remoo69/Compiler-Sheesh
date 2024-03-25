import sys
sys.path.append( '.' )
import source.core.constants as const
from dataclasses import dataclass

@dataclass
class Token:
    value: str
    type: str
    attribute: str= 'default'
    line: int=0
    position: int= 0

    idnum=1
    tok_num=1
    line_num=1
    in_comment=False
    block_comment_buffer=''
    id_dict={}
    block_start_line=0
    
    # def __init__(self, type=None, value=None, line=None, position=None, attribute=None):
    #     self.value = value
    #     self.type = type
    #     self.attribute=attribute
    #     self.line = line
    #     self.position = position
    #     self.state= "Start" #States are start, active, end, and error
        # self.transitions={
        #     "Operators":{
        #         'start': {'+': 'plus', '-': 'minus', '*': 'multiply', '/': 'divide', '=': 'equal', '%':'modulo', 'other': 'invalid'},
        #         'plus': {'=': 'plus_equal', const.symbols_delims['+']:'final', 'other': 'invalid'},
        #         'minus': {'=': 'minus_equal', const.symbols_delims['-']:'final','other': 'invalid'},
        #         'multiply': {'=': 'multiply_equal', const.symbols_delims['*']:'final', 'other': 'invalid'},
        #         'divide': {'=': 'divide_equal',const.symbols_delims['/']:'final', 'other': 'invalid'},
        #         'equal': {'=':'equal_equal', const.symbols_delims['=']:'final','other': 'invalid'},
        #         'modulo': {'=':'modulo_equal', const.symbols_delims['%']:'final','other': 'invalid'},
        #         'plus_equal': {const.symbols_delims['+=']:'final','other': 'invalid'},
        #         'minus_equal': {const.symbols_delims['-=']:'final','other': 'invalid'},
        #         'multiply_equal': {const.symbols_delims['*=']:'final','other': 'invalid'},
        #         'divide_equal': {const.symbols_delims['/=']:'final','other': 'invalid'},
        #         'modulo_equal': {const.symbols_delims['%=']:'final','other': 'invalid'},
        #         'equal_equal':{const.symbols_delims['==']:'final','other': 'invalid'},
        #         'invalid': {'other': 'invalid'},
        #         'final':{'None':'final'}
        #     }
        # }

        # self.accepting_states={}

    # def transition(self, inputval):
    #     if self.state=="Start":
    #         if inputval in const.StartStates and self.state=="Start":
    #             self.value=inputval
    #             self.state="Active"
    #         if inputval in const.ActiveStates and self.state=="Active":
    #             self.add_value(inputval)
    #         if inputval in const.FinalStates
    #         else:
    #             self.set_state("Error")

    # def set_state(self, newstate):
    #     self.state=newstate

    # def set_value(self, newvalue):
    #     self.value=newvalue

    # def add_value(self, addvalue):
    #     self.value+=addvalue

    # def set_type(self, newtype):
    #     self.type=newtype
    
    # def set_attribute(self, newattr):
    #     self.attribute=newattr

    # def set_start(self):
    #     self.state="Start"

    # def set_active(self):
    #     self.state="Active"

    # def is_valid(self):
    #     pass

    # def simulate(self, inputval):
    #     pass

    # def reset(self):
    #     self.set_start

class LexerCheck:
    @staticmethod    
    def is_Text(Token: str) -> bool: #rewritten with gpt
        if not Token.startswith('"') and not Token.endswith('"'):
            return False

        if Token.count('"') != 2:
            return False
        elif any(invalid in Token[1:-1] for invalid in const.invalid_text_char):
            return False
        else: return True
        # escaped = False
        # for char in Token[1:-1]:
        #     if escaped:
        #         escaped = False
        #     elif char == '\\':
        #         escaped = True
        #     elif char == '"':
        #         return False

        # return not escaped
    @staticmethod    
    def is_Identifier(Token): #rewritten
        try:
            if Token[0].isalpha() and all(char.isalnum() or char == '_' for char in Token[1:]):
                if len(Token)<=const.MAX_IDEN_LENGTH:
                    return True
                else: return False
            else:
                return False
        except IndexError:
            if Token.isalpha():
                return True
            else:
                return False
    @staticmethod    
    def is_Whole(Token: str): #rewritten; might contain problems
        if Token=="0" or ((Token.isdigit() and const.WHOLE_MIN<= int(Token)<=const.WHOLE_MAX)and not Token.startswith("0")) or (Token.startswith('(') and Token.endswith(')') and (Token[1]=="-" and Token[2:-1].isdigit() and Token[2]!="0")):
            return True
        else:
            return False

    @staticmethod    
    def is_Dec(Token: str):
        if LexerCheck.is_Neg_Dec(Token) or LexerCheck.is_Pos_Dec(Token):
            return True
        else:
            return False
    @staticmethod    
    def is_Pos_Dec(Token: str):
        if "." in Token:
            parts=Token.split(".")
            return (len(parts)==2 and ((parts[0].isdigit() and int(parts[0])!=0) or (parts[0]=="0")) and parts[1].isdigit() and const.DEC_MIN <= float(Token) <= const.DEC_MAX)
            
        # return Token == '0' or (Token.isdigit() and '.' in Token and 0 <= float(Token) <= 99999.999999)
    @staticmethod    
    def is_Neg_Dec(Token: str):
        return (Token.startswith('(') and Token.endswith(')') and Token[1]=="-" and LexerCheck.is_Pos_Dec(Token[2:-1]))

    #Needs further work
    @staticmethod    
    def keyword_type(Token, delimiter):
        #This function already returns the tokentype, 
        for i in const.keywords:
            pass
            # if Token==and delimiter in const.delimiters["delim3"]:
            # return True

            # else:
            #     return False

    #Might run into problems here because delimiters include characters as well, not just symbols
    @staticmethod    
    def is_Operator(Token):
        if Token in const.all_op:
            return True
        else:
            return False
        
    @staticmethod        
    def is_Symbol(Token):
        if Token in const.non_op:
            return True
        else:
            return False

    @staticmethod    
    def is_Keyword(Token):
        if Token in const.keywords:
            return True
        else: return False       

    @staticmethod    
    def is_Numeric(Token):
        if LexerCheck.is_Whole(Token) or LexerCheck.is_Dec(Token):
            return True
        else: return False

    @staticmethod    
    def is_Literal(Token):
        if LexerCheck.is_Text(Token) or LexerCheck.is_Numeric(Token):
            return True
        else: return False

    @staticmethod
    def is_Inline_Comment(Token):
        if Token.startswith("//"):
            return True
        else: return False

    @staticmethod
    def is_Charr(Token):
        if (Token.startswith("'") and Token.endswith("'")) and (((len(Token)==3 and ((Token[1:-1] ) or Token[1:-1].isalpha())) or (len(Token)==2 and Token=="''")) or (len(Token)==4 and (Token[1:-1] in const.esc_seq))):
            return True
        else: return False

    @staticmethod    
    def categorize(lexeme:str):
        #Categorizes each token based on their type and attribute
        #Takes a list of tokenized lines
        if LexerCheck.is_Keyword(lexeme):
            return "Keyword"
        elif LexerCheck.is_Identifier(lexeme) and len(lexeme)<=const.MAX_IDEN_LENGTH:
            return "Identifier"
        elif LexerCheck.is_Operator(lexeme):
            return "Operator"
        elif LexerCheck.is_Symbol(lexeme):
            return "Symbol"
        elif LexerCheck.is_Text(lexeme):
            return "Text"
        elif LexerCheck.is_Charr(lexeme):
            return "Charr"
        elif LexerCheck.is_Whole(lexeme):
            return "Whole"
        elif LexerCheck.is_Dec(lexeme):
            return "Dec"
        elif LexerCheck.is_Inline_Comment(lexeme):
            return "Inline Comment"
        elif lexeme in const.boolean:
            return "Lit"
        elif lexeme is None:
            return "None"
        elif lexeme.startswith("/*") and lexeme.endswith("*/"):
            return "Block Comment"
        elif lexeme in const.whitespace:
            return "Whitespace"
        else:
            return "Error Category"

    @staticmethod                   
    def is_Valid_Token(Token:str):
        if LexerCheck.is_Numeric(Token) or (LexerCheck.is_Identifier(Token) and len(Token)<=10) or LexerCheck.is_Keyword(Token) or LexerCheck.is_Literal(Token) or LexerCheck.is_Symbol(Token) or LexerCheck.is_Operator(Token):
            return True
        else: return False


test='"'
print(LexerCheck.is_Text(test))