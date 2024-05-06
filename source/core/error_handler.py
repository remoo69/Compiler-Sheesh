import sys
sys.path.append( '.' )
import source.core.constants as const
import source.LexicalAnalyzer.prepare as prep
import source.core.symbol_table as symb

class Error:
    errcount=0
    def __init__(self, errorval=None, remaining=None, line=0, toknum=0, type=None, errclass=None):
        self.errorval = errorval
        self.line=line
        self.toknum=toknum
        self.remaining=remaining
        self.error_type=type
        self.error_class=errclass

    def __str__(self) -> str:
        return f"Line {self.line}, Token {self.toknum}: {self.error_type}"

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
            errobj.error_type=f"Invalid Symbol '{buffer}', expected {const.all_op} or {const.all_symbols_nonop} "
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
            
            return errobj
        if tokencode[0:3]=="..." and i+4<len(tokencode) and tokencode[i+4] not in const.symbols_delims["..."]:
            buffer=tokencode[0:3]
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '[{tokencode[i + 3]}]', expected {const.symbols_delims[buffer]} "
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
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
                            errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '[{tokencode[i + 3]}]', expected {const.symbols_delims[buffer]} "
                            errobj.line=symb.Token.line_num
                            errobj.toknum=symb.Token.tok_num
                            return errobj
                    else:
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '[{tokencode[i + 2]}]', expected {const.symbols_delims[buffer]} "
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                else:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Delimiter for Symbol '{buffer}', '[{tokencode[i + 1]}]', expected {const.symbols_delims[buffer]} "
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
            else:
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Null Delimiter for Symbol '{buffer}', expected {const.symbols_delims[buffer]} "
                errobj.line=symb.Token.line_num
                errobj.toknum=symb.Token.tok_num
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
                errobj.error_type=f"Invalid Delimiter for Keyword '{buffer}', '[{tokencode[i]}]', expected {const.keywords_delims[buffer]} "
                errobj.line=symb.Token.line_num
                errobj.toknum=symb.Token.tok_num
                return errobj

            else:
                buffer += tokencode[i]
                i+=1
        if buffer in const.keywords and buffer not in ["bet", "deins"]:
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Keyword '{buffer}', expected {const.keywords_delims[buffer]} "
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
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
                        errobj.error_type=f"Invalid Identifier Length [{tokencode[i]}]. Only '{buffer}' is considered an Identifier"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    elif len(buffer)==len(tokencode):
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Null Delimiter for Identifier '{buffer}', expected {const.delimiters['id_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    
                    else: 
                        i+=1
                    
                    
                else: 
                    if tokencode[i] not in const.invalid_id_char:
                        if not tokencode[0].isalpha(): #invalid first char
                            errobj.errorval=buffer
                            errobj.remaining=tokencode.replace(buffer, '', 1)
                            errobj.error_type=f"Invalid First Character for Identifier"
                            errobj.line=symb.Token.line_num
                            errobj.toknum=symb.Token.tok_num
                            return errobj
                        #delim as invalid char; invalid delim
                    elif tokencode[i] in const.invalid_id_char:
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter [\" {tokencode[i]} \"] for Identifier \"{buffer}\" , expected {const.delimiters['id_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    elif tokencode[i] in const.delimiters["id_delim"]:
                        return None

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
                errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[1]}]', expected {const.delimiters['n_delim']}"
                errobj.line=symb.Token.line_num
                errobj.toknum=symb.Token.tok_num
                return errobj
            buffer=tokencode[0]
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[1]}]', expected {const.delimiters['n_delim']} "
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
            return errobj
        if len(tokencode)==1 and tokencode.isdigit():
            buffer=tokencode
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}', expected {const.delimiters['n_delim']} "
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
            return errobj

        while i < len(tokencode):
            if prep.LexerCheck.is_Numeric(buffer) and len(buffer) < len(tokencode):
                if tokencode[i].isdigit():
                    buffer+=tokencode[i]
                    i+=1
                try:
                    if tokencode[i] not in const.delimiters["n_delim"]:
                        # invalid delim
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[i]}]', expected {const.delimiters['n_delim']} "
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                except IndexError:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}', expected {const.delimiters['n_delim']} "
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
            elif buffer.startswith("-"):
                # invalid format for negative
                errobj.errorval=buffer
                errobj.remaining=tokencode.replace(buffer, '', 1)
                errobj.error_type=f"Invalid Negative Value Format. Enclose Negatives in ( ), '{buffer}'"
                errobj.line=symb.Token.line_num
                errobj.toknum=symb.Token.tok_num
                return errobj
                
            elif tokencode.startswith("("):
                if tokencode.endswith(")"):
                    buffer=tokencode
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}', expected {const.delimiters['n_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                elif len(buffer)==len(tokencode):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Numeric '{buffer}', expected {const.delimiters['n_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                elif (len(buffer)>=4 and buffer[1]=="-" and buffer[2:3]=="00"):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[3]}]', expected {const.delimiters['n_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj

                elif len(buffer)>=2 and buffer[1]=="-":
                    if len(buffer)>=4 and buffer[2:3]=="00":
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[3]}]', expected {const.delimiters['n_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    elif len(buffer)>=3 and buffer[2]==")":
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '[{tokencode[3]}]', expected {const.delimiters['n_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    else:
                        buffer+=tokencode[i]
                        i+=1
                
                
                elif len(buffer)>=3 and buffer[1]=="-" and buffer[2]=="0":
                    if len(buffer)>4 and (buffer[3]==")" or buffer[3]=="0"):
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Numeric '{buffer}', '{tokencode[1]} , expected {const.delimiters['n_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    else:
                        buffer+=tokencode[i]
                        i+=1
                    
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
        if len(buffer)==len(tokencode) and prep.LexerCheck.is_Numeric(buffer):
            errobj.errorval=buffer
            errobj.remaining=tokencode.replace(buffer, '', 1)
            errobj.error_type=f"Invalid Null Delimiter for Numeric, '{buffer}', expected {const.delimiters['n_delim']}"
            errobj.line=symb.Token.line_num
            errobj.toknum=symb.Token.tok_num
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
                    errobj.error_type=f"Invalid Null Delimiter for Text '{buffer}', expected {const.delimiters['txt_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                elif tokencode[i] not in const.delimiters["txt_delim"]:
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Text [{tokencode[i]}] Delimiter for {buffer}, expected {const.delimiters['txt_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                elif len(buffer)==len(tokencode):
                    errobj.errorval=buffer
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"No Closing Quote for {buffer}, expected {const.delimiters['txt_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                i += 1
            
            else: return None

    @staticmethod
    def get_error_charr(tokencode):
        #error types: no closing quote, invalid escape sequence, invalid delim, illegal character
        buffer=''
        i=0
        errobj=Error()
        errobj.error_class="Lexical Error"

        while i<len(tokencode):
            if tokencode.startswith("'"):
                buffer += tokencode[i]
                if tokencode[len(tokencode)-1]=="'":
                    errobj.errorval=tokencode[0:len(tokencode)-1]
                    errobj.remaining=tokencode.replace(buffer, '', 1)
                    errobj.error_type=f"Invalid Null Delimiter for Charr '{buffer}', expected {const.delimiters['txt_delim']}"
                    errobj.line=symb.Token.line_num
                    errobj.toknum=symb.Token.tok_num
                    return errobj
                elif buffer.startswith("'") and buffer.endswith("'"):
                    if len(buffer)<len(tokencode) and prep.LexerCheck.is_Charr(buffer) and tokencode[i+1] not in const.delimiters["txt_delim"] :
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Delimiter for Charr ({buffer}): [' {tokencode[i+1]} '], expected {const.delimiters['txt_delim']}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    elif len(buffer)==len(tokencode):
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"No Closing Quote for {buffer}"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                    elif len(buffer)>3 and buffer[-1]=="'":
                        errobj.errorval=buffer
                        errobj.remaining=tokencode.replace(buffer, '', 1)
                        errobj.error_type=f"Invalid Charr Length"
                        errobj.line=symb.Token.line_num
                        errobj.toknum=symb.Token.tok_num
                        return errobj
                i += 1
            
            else: return None

    @staticmethod
    def get_errors(tokencode): #this should return the errotype as well
        if tokencode is None:
            return None
        elif LexError.get_error_charr(tokencode):
            return LexError.get_error_charr(tokencode)
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
        
class SyntaxError:
    def __init__(self, unexpected, line ,toknum,value, expected) -> None:
        self.unexpected=unexpected
        self.line=line
        self.toknum=toknum
        self.expected=expected
        self.value=value

    def __repr__(self) -> str:
        return f"Line {self.line}, Token {self.toknum}: Unexpected \"{self.value}\" [{self.unexpected}], expected -> {self.expected}"

class SemanticError:
    def __init__(self, *, error, line, toknum, value, expected) -> None:
        self.error=error
        self.line=line
        self.toknum=toknum
        self.expected=expected
        self.value=value


    def __repr__(self) -> str:
            return f"Line {self.line}, Token {self.toknum}: {self.error} for \"{self.value}\", expected -> {self.expected}"
    

class RuntimeError:
    def __init__(self, *, error,  token, expected) -> None:
        self.error=error
        self.line=token.line
        self.toknum=token.position
        self.expected=expected


    def __repr__(self) -> str:
            return f"Line {self.line}, Token {self.toknum}: {self.error}, expected -> {self.expected}"