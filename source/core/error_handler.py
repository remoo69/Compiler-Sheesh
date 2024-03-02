import sys
sys.path.append( '.' )
import source.core.constants as const
import source.LexicalAnalyzer.prepare as prep

import source.LexicalAnalyzer.tokenclass as tkc 


#urgent todo: add kw errors, error for ::

class Error:
    errcount=0
    def __init__(self, errorval=None, remaining=None, line=0, type=None, errclass=None):
        self.errorval = errorval
        self.line=line
        self.remaining=remaining
        self.error_type=type
        self.error_class=errclass

    def __str__(self) -> str:
        return f"Line {self.line}: {self.error_type}"

class LexError:

    @staticmethod
    def get_error_symbol(tokencode):
        #error types: invalid delim for symbol, invalid symbol, invalid compound symbol
        buffer = ''
        i = 0
        errobj=Error()
        errobj.error_class="Lexical Error"
         #invalid delim error
        buffer += tokencode[i]
        
        if buffer in const.invalid_symbols:
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Symbol '{buffer}'"
            errobj.line=tkc.Token.line_num
            return errobj
        if tokencode[0:3]=="..." and i+4<len(tokencode) and tokencode[i+4] not in const.symbols_delims["..."]:
            buffer=tokencode[0:3]
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '{tokencode[i + 3]}' "
            errobj.line=tkc.Token.line_num
            return errobj
        if buffer in const.all_op or buffer in const.all_symbols_nonop:
            if i + 1 < len(tokencode):
                if buffer + tokencode[i + 1] in const.all_op:
                    buffer += tokencode[i + 1]
                    if i + 2 < len(tokencode) and buffer + tokencode[i + 2] in const.all_op:
                        buffer += tokencode[i + 2]
                        if i + 3 < len(tokencode) and buffer + tokencode[i + 3] not in const.all_op:
                            errobj.errorval=buffer
                            errobj.remaining=tokencode.replace(buffer, '', 1)
                            errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '{tokencode[i + 3]}' "
                            errobj.line=tkc.Token.line_num
                            return errobj
                    else:
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '{tokencode[i + 2]}' "
                        errobj.line=tkc.Token.line_num
                        return errobj
                else:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '{tokencode[i + 1]}' "
                    errobj.line=tkc.Token.line_num
                    return errobj
            else:
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Null Delimiter for Symbol '{buffer}' "
                errobj.line=tkc.Token.line_num
                return errobj
        # i += 1

    @staticmethod
    def get_error_keyword(tokencode):
        #error types: invalid delim for keyword, invalid keyword
        buffer = ''
        i = 0
        errobj=Error()
        errobj.error_class="Lexical Error"
        while i<len(tokencode):
            if (buffer in const.keywords) and (tokencode[i] not in const.keywords_delims[buffer]):
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Delimiter for Keyword '{buffer}', '{tokencode[i]}' "
                errobj.line=tkc.Token.line_num
                return errobj

            else:
                buffer += tokencode[i]
                i+=1
        if buffer in const.keywords and buffer not in ["bet", "deins"]:
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Keyword '{buffer}' "
            errobj.line=tkc.Token.line_num
            return errobj
    
    @staticmethod
    def get_error_identifier(tokencode):
        #error types: invalid delim, size too long, invalid char as delim, 
        buffer=''
        i=0
        errobj=Error()
        errobj.error_class="Lexical Error"

        if tokencode[0].isdigit():
            return None
        while i<len(tokencode): #invalid delim error
                if tokencode[i] not in const.delimiters["id_delim"] and tokencode[i] not in const.invalid_id_char: 
                    buffer+=tokencode[i]
                    if len(buffer)>const.MAX_IDEN_LENGTH: #size too long
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Identifier Length. Only '{buffer}' is considered an Identifier"
                        errobj.line=tkc.Token.line_num
                        return errobj
                    elif len(buffer)==len(tokencode):
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Null Delimiter for Identifier '{buffer}'"
                        errobj.line=tkc.Token.line_num
                        return errobj
                    
                    else: 
                        i+=1
                    
                    
                else: 
                    if tokencode[i] not in const.invalid_id_char:
                        if not tokencode[0].isalpha(): #invalid first char
                            errobj.errorval=buffer
                            errobj.remaining=tokencode.replace(buffer, '', 1)
                            errobj.error_type=f"Invalid First Character for Identifier"
                            errobj.line=tkc.Token.line_num
                            return errobj
                        #delim as invalid char; invalid delim
                    elif tokencode[i] in const.invalid_id_char:
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter \" {tokencode[i]} \" for Identifier \"{buffer}\""
                        errobj.line=tkc.Token.line_num
                        return errobj
                    elif tokencode[i] in const.delimiters["id_delim"]:
                        return None
            
        # if len(buffer)==len(tokencode) :
        #     errobj.errorval=buffer
        #     errobj.remaining=tokencode.replace(buffer, '', 1)
        #     errobj.error_type=f"Invalid Null Delimiter for Identifier '{buffer}'"
        #     errobj.line=tkc.Token.line_num
        # return buffer, tokencode.replace(buffer, '', 1)

    @staticmethod
    def get_error_numeric(tokencode):
        #error types for numeric: invalid delimiter, invalid size, invalid format for negative
        buffer=''
        i=0
        errobj=Error()
        errobj.error_class="Lexical Error"

        if tokencode.startswith("0") and len(tokencode)>1:
            if tokencode[1]=="0":
                buffer=tokencode[0]
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}', {tokencode[1]}"
                errobj.line=tkc.Token.line_num
                return errobj
            buffer=tokencode[0]
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[1]}' "
            errobj.line=tkc.Token.line_num
            return errobj
        if len(tokencode)==1 and tokencode.isdigit():
            buffer=tokencode
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}' "
            errobj.line=tkc.Token.line_num
            return errobj

        while i < len(tokencode):
            if tkc.LexerCheck.is_Numeric(buffer) and len(buffer) < len(tokencode):
                if tokencode[i].isdigit():
                    buffer+=tokencode[i]
                    i+=1
                try:
                    if tokencode[i] not in const.delimiters["n_delim"]:
                        # invalid delim
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[i]}' "
                        errobj.line=tkc.Token.line_num
                        return errobj
                except IndexError:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}' "
                    errobj.line=tkc.Token.line_num
                    return errobj
            elif buffer.startswith("-"):
                # invalid format for negative
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Negative Value Format. Enclose Negatives in ( ), '{buffer}'"
                errobj.line=tkc.Token.line_num
                return errobj
                
            elif tokencode.startswith("("):
                if tokencode.endswith(")"):
                    buffer=tokencode
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}'"
                    errobj.line=tkc.Token.line_num
                    return errobj
                elif len(buffer)==len(tokencode):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}'"
                    errobj.line=tkc.Token.line_num
                    return errobj
                elif (len(buffer)>=4 and buffer[1]=="-" and buffer[2:3]=="00"):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[3]}'"
                    errobj.line=tkc.Token.line_num
                    return errobj
                    # invalid size
                # elif len(buffer)>=3 and (buffer[2:-1]=="0"or int(buffer[2:-1])==0) and buffer[1]=="-":
                #     errobj.errorval=buffer
                #     errobj.remaining=tokencode.replace(buffer, '', 1)
                #     errobj.error_type=f"Illegal Negative Numeric Literal, '{buffer}'"
                #     errobj.line=tkc.Token.line_num
                #     return errobj
                elif len(buffer)>=2 and buffer[1]=="-":
                    if len(buffer)>=4 and buffer[2:3]=="00":
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[3]}'"
                        errobj.line=tkc.Token.line_num
                        return errobj
                    elif len(buffer)>=3 and buffer[2]==")":
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[3]}'"
                        errobj.line=tkc.Token.line_num
                        return errobj
                    else:
                        buffer+=tokencode[i]
                        i+=1
                
                
                elif len(buffer)>=3 and buffer[1]=="-" and buffer[2]=="0":
                    if len(buffer)>4 and (buffer[3]==")" or buffer[3]=="0"):
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[1]}"
                        errobj.line=tkc.Token.line_num
                        return errobj
                    else:
                        buffer+=tokencode[i]
                        i+=1
                    
               
                # errobj.errorval=buffer
                # errobj.remaining=tokencode.replace(buffer, '', 1)
                # errobj.error_type=f"Numeric Literal is too Large, '{buffer}'"
                # errobj.line=tkc.Token.line_num
                # return errobj
                else:
                    buffer+=tokencode[i]
                    i+=1
            else:
                buffer += tokencode[i]
                i += 1
        try:
            buffer+=tokencode[i+1]
        except IndexError:
            return None
        if len(buffer)==len(tokencode) and tkc.LexerCheck.is_Numeric(buffer):
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Numeric, '{buffer}'"
            errobj.line=tkc.Token.line_num
            return errobj
        
    @staticmethod
    def get_error_text(tokencode):
        #error types: no closing quote, invalid escape sequence, invalid delim, illegal character
        buffer=''
        i=0
        errobj=Error()
        errobj.error_class="Lexical Error"

        while i<len(tokencode):
            if tokencode.startswith('"'):
                buffer += tokencode[i]
                if tokencode[len(tokencode)-1]=='"':
                    errobj.errorval=tokencode[0:len(tokencode)-1]
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Text '{buffer}'"
                    errobj.line=tkc.Token.line_num
                    return errobj
                elif tokencode[i] not in const.delimiters["txt_delim"]:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Text Delimiter for {buffer}"
                    errobj.line=tkc.Token.line_num
                    return errobj
                elif len(buffer)==len(tokencode):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"No Closing Quote for {buffer}"
                    errobj.line=tkc.Token.line_num
                    return errobj
                i += 1
            
            else: return None

            
        # return buffer, tokencode.replace(buffer, '', 1)

    @staticmethod
    def get_errors(tokencode): #this should return the errotype as well
        if tokencode is None:
            return None
        elif LexError.get_error_numeric(tokencode):
            return LexError.get_error_numeric(tokencode)
        elif LexError.get_error_symbol(tokencode):
            return LexError.get_error_symbol(tokencode)
        elif LexError.get_error_text(tokencode):
            return LexError.get_error_text(tokencode)
        elif LexError.get_error_keyword(tokencode):
            return LexError.get_error_keyword(tokencode)
        elif LexError.get_error_identifier(tokencode):
            return LexError.get_error_identifier(tokencode)
        
        
    # @staticmethod
    # def error_type(errorval, remaining):
    #     category=tkc.LexerCheck.categorize(errorval)
    #     if category=="Keyword":
    #         return f"Invalid Delimiter for Keyword {errorval}"
    #     elif category=="Identifier":
    #         if len(errorval)>const.MAX_IDEN_LENGTH:
    #             return f"Identifier {errorval} exceeds maximum length of {const.MAX_IDEN_LENGTH}"
    #         elif errorval[0].isdigit():
    #             return f"Invalid first character for Identifier {errorval}"
    #         else:
    #             return f"Invalid Delimiter for Identifier {errorval}"
    #     elif category=="Numeric":
            
# print(LexError.get_error_identifier(test))
        
class SyntaxError:
    def __init__(self, unexpected, line, expected) -> None:
        self.unexpected=unexpected
        self.line=line
        self.expected=expected

    def __repr__(self) -> str:
        return f"Unexpected {self.unexpected} at line {self.line}, expected {self.expected}"