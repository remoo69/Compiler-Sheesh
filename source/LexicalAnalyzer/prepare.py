import sys
sys.path.append( '.' )
import source.core.constants  as const
import source.core.symbol_table as symb

""" 
Prepares the Input file for tokenization. Removes comments, extra newline characters, and extra spaces.
Also splits the code into lines.

"""

class LexerCheck:
    @staticmethod
    def count_chars_from_list(text, char_list):
        """
        This function counts the total occurrences of characters from a list within a string.

        Args:
            text: The string to search in.
            char_list: A list of characters to count.

        Returns:
            The total count of characters from the list found in the text.
        """
        count = 0
        for char in text:
            if char in char_list:
                count += 1
        return count
    
    @staticmethod    
    def is_Text(Token: str) -> bool:
        quotes=['"','“',"”",'"']
        quote_counts = LexerCheck.count_chars_from_list(Token, quotes)  

        if ( (Token.startswith('"') or Token.startswith('“') or Token.startswith('”') or Token.startswith('"'))) and ( (Token.endswith('"') or Token.endswith('”') or Token.endswith('“') or Token.endswith('"'))) and quote_counts%2==0 and not any(invalid in Token[1:-1] for invalid in const.invalid_text_char):
            return True
        else: return False

    @staticmethod    
    def is_Identifier(Token):
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
    def is_Whole(Token: str): 
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

    @staticmethod    
    def is_Neg_Dec(Token: str):
        return (Token.startswith('(') and Token.endswith(')') and Token[1]=="-" and LexerCheck.is_Pos_Dec(Token[2:-1]))

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
        elif Token in const.multi_charr:
            return True
        else: return False

    @staticmethod    
    def categorize(lexeme:str):
        """ 
        Categorizes each token based on their type and attribute
        Takes a list of tokenized lines 
        """
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

#region functions

def get_charr(token):
    token_cpy=''
    temp_token=''
    for char in token:
        if char in const.delimiters["txt_delim"] and LexerCheck.is_Charr(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char
    

def remove_comments(code):
    output_code = ""
    in_block_comment = False
    in_inline_comment = False

    i = 0
    while i < len(code):
        if code[i:i+2] == '/*' and not in_block_comment and not in_inline_comment:
            in_block_comment = True
            i += 2
        elif code[i:i+2] == '*/' and in_block_comment:
            in_block_comment = False
            i += 2
        elif code[i:i+2] == '//' and not in_block_comment and not in_inline_comment:
            in_inline_comment = True
            i += 2
        elif code[i] == '\n' and in_inline_comment:
            in_inline_comment = False
            output_code += '\n'
            i += 1
        elif not in_block_comment and not in_inline_comment:
            output_code += code[i]
            i += 1
        else:
            i += 1

    return output_code


def get_block_comments(text:str):
    i = 0
    comment_buffer=''

    if symb.Token.in_comment:
        while i<len(text):

            if text[i:i+2]=="*/":
                comment_buffer+=text[i:i+2]
                symb.Token.block_comment_buffer+=text[i:i+2]
                symb.Token.in_comment=False
                return comment_buffer, text.replace(comment_buffer, '', 1)
            
            else:
                comment_buffer+=text[i]
                symb.Token.block_comment_buffer+=text[i]
                i+=1
            
    else:
        while i<len(text):

            if text[0:2]=="/*" : 
                symb.Token.in_comment=True
                comment_buffer+=text[i]
                symb.Token.block_comment_buffer+=text[i]
                i+=1

                if text[i:i+2]=="*/":
                    comment_buffer+=text[i:i+2]
                    symb.Token.block_comment_buffer+=text[i:i+2]
                    symb.Token.in_comment=False
                    return comment_buffer, text.replace(comment_buffer, '', 1)  
                
            else: return None

        symb.Token.line_num+=1
        return comment_buffer, text.replace(comment_buffer, '', 1)

def get_inline_comments(input_code):
    token = ""
    in_inline_comment = False

    i = 0
    while i < len(input_code):
        if input_code[i:i+2] == '//' and not in_inline_comment:
            in_inline_comment = True
            token+=input_code[i:i+2]
            i += 2
        if input_code[i] is (None or '\n') and in_inline_comment:
            in_inline_comment = False
            break
        if in_inline_comment:
            token += input_code[i]
            i += 1
        else: return None
    return token, input_code.replace(token, '', 1)


    
def remove_whitespace_type(tokens, category):
    new_tokens = []
    new_category = []
    for i in range(len(tokens)):
        if category[i] != "Whitespace":
            new_tokens.append(tokens[i])
            new_category.append(category[i])
    return new_tokens, new_category

def getlines(code):
    """ Splits the code into lines """
    lines=[]
    lines=code.split("\n")
    return lines

def get_delim_key(delim_char):
    for key, value in const.delimiters.items():
        if delim_char in value:
            return key
    return None


def get_whole(token):
    token_cpy=''
    temp_token=''

    for char in token:

        if char in const.delimiters["n_delim"] and LexerCheck.is_Whole(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char
    
def get_dec(token):
    token_cpy=''
    temp_token=''
    dec_detected=False
    for char in token:
        if char in const.delimiters["n_delim"] and LexerCheck.is_Dec(temp_token):
            token_cpy=token.replace(temp_token, '', 1) 
            return temp_token, token_cpy       
        else:
            temp_token+=char

def get_keyword(token):
    token_cpy=''
    temp_token=''
    keyword_detected=False

    for i,char in enumerate(token):

        if temp_token is None:
            return '',token
        
        elif ((temp_token in const.keywords) and (char in const.keywords_delims[temp_token])) or (temp_token=="when" and token[i:i+1]=="::"):
            token_cpy=token.replace(temp_token, '', 1)
            keyword_detected=True
            return temp_token, token_cpy
               
        else:   
            temp_token+=char
   
def get_identifier(token):
    token_cpy=''
    temp_token=''

    for char in token:

        if char in const.delimiters["id_delim"] and LexerCheck.is_Identifier(temp_token) and temp_token not in const.keywords:
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        
        else:
            temp_token+=char
            
def is_combined_op(curr, next):
    return curr+next in const.compound_symbols
    
def get_operator(tokencode:str):
    position=0
    token=''
    token_cpy=''
   
    char=tokencode[position]

    if char==".": #isolated case for ...
        token+=char

        if tokencode[position+1]==".":
            token+=tokencode[position+1]
            if tokencode[position+2]==".":
                token+=tokencode[position+2]
                if tokencode[position+3] in const.symbols_delims["..."]:
                    token_cpy=tokencode.replace(token, '', 1)
                    return token, token_cpy
                
    elif char in const.single_symbols:
        token+=char

        try:
            if tokencode[position+1] in const.symbols_delims[char]:
                token_cpy=tokencode.replace(char, '', 1)
                return char, token_cpy
            
        except IndexError:
            return None
        
        else: #else, it should be compound
            position+=1
            token+=tokencode[position]   

            if token not in const.compound_symbols:
                return None

            else:
                position+=1
                token_cpy=tokencode.replace(token, '', 1)

                if tokencode[position] in const.symbols_delims[token]: #if valid delim for compound symbol  
                    return token, token_cpy
                
                else:
                    return None
                
def get_symbol(token):
    try:
        size=len(token)
        i=0
        symbol_buffer=''
        if token[i]=="#" and len(token)==1:
            return token, token.replace(token, '', 1)
        elif token[i]==")" and len(token)==1:
            return token, token.replace(token, '', 1)
        elif token[i] in const.all_symbols_nonop and token[i+1] in const.symbols_delims[token[i]]:
            symbol_buffer+=token[i]
            return token[i], token.replace(token[i], '', 1)
        elif token[i:2]=="::" and (len(token)==2 or token[i+2] in const.symbols_delims["::"]): 
                return "::", token.replace("::", '', 1)
        
    except IndexError:
        if token in const.grouping_symbols and None in const.symbols_delims[token]:
            return token, token.replace(token, '', 1)

def get_space(token):
    token_cpy=token
    temp_token=''
    space_detected=False
    space=" "
    for char in token:

        if char==" " or char=="\t" or char==' ':
            token_cpy=token.replace(char, '', 1)
            symb.Token.tok_num-=1
            return char, token_cpy
        else:return None
    
def get_text(token):
    """ Returns the text token and the remaining code """
    token_cpy=''
    temp_token=''
    text_detected=False
    for i,char in enumerate(token):

        try:
            check_concat=char+token[i+1]+token[i+2]
        except IndexError:
            check_concat=''

        if (char in const.delimiters["txt_delim"] or check_concat=="...") and LexerCheck.is_Text(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy      
         
        else:
            temp_token+=char

    if (char in const.delimiters["txt_delim"] or check_concat=="...") and LexerCheck.is_Text(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy   
    

def get_next_char(input_string, current_index):
    if current_index < len(input_string)-1:
        return input_string[current_index+1]
    else:
        return None
        
def get_lit(token):
    token_cpy=''
    temp_token=''
    for char in token:
        if char in const.delimiters["n_delim"] and LexerCheck.is_Literal(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char


#endregion


def prepare(code):
    """ 
    Prepares the code for tokenization. Removes comments, extra newline characters, and extra spaces.
    Returns each line of code as a list of strings; ignores empty lines. 
    """
    templines=getlines(code) #remove_comments(
    lines=[] 
    for i in range(len(templines)):
        lines.append(templines[i])
    return lines
