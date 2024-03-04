# import re
#Prepares the Input file for tokenization. Removes comments, extra newline characters, and extra spaces.
#Also splits the code into lines.
# import source.core.constants as const
# import LexicalAnalyzer.lexerpy as lex
# import sys
# sys.path.append(r"C:\Users\anton\Desktop\College Stuff Files\Compiler-Sheesh\source")
# print(sys.path)
import sys
sys.path.append( '.' )
# from compiler_sheesh.source.core import constants as const
import source.core.constants  as const
# from ..core import constants as const
import source.LexicalAnalyzer.tokenclass as tkc
# import source.core.constants as const


#region functions

def file_to_string(file):
    try:
        with open(file, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        print("File not found.")
        return None

def get_charr(token):
    token_cpy=''
    temp_token=''
    for char in token:
        if char in const.delimiters["txt_delim"] and tkc.LexerCheck.is_Charr(temp_token):
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

# def get_block_comments(input_code):
#     output_code = ""
#     in_block_comment = False

#     i = 0
#     while i < len(input_code):
#         if input_code[i:i+2] == '/*' and not in_block_comment:
#             in_block_comment = True
#             i += 2
#         elif input_code[i:i+2] == '*/' and in_block_comment:
#             in_block_comment = False
#             i += 2
#         elif not in_block_comment:
#             output_code += input_code[i]
#             i += 1
#         else:
#             i += 1

#     return output_code
def get_block_comments(text:str):
    i = 0
    comment_buffer=''
    if tkc.Token.in_comment:
        while i<len(text):
            if text[i:i+2]=="*/":
                comment_buffer+=text[i:i+2]
                tkc.Token.block_comment_buffer+=text[i:i+2]
                tkc.Token.in_comment=False
                # comment_buffer=tkc.Token.block_comment_buffer
                # tkc.Token.block_comment_buffer=''
                return comment_buffer, text.replace(comment_buffer, '', 1)
            
            else:
                comment_buffer+=text[i]
                tkc.Token.block_comment_buffer+=text[i]
                i+=1
            
    else:
        while i<len(text):
            if text[0:2]=="/*" : #and not tkc.Token.in_comment
                tkc.Token.in_comment=True
                comment_buffer+=text[i]
                tkc.Token.block_comment_buffer+=text[i]
                # comment_buffer=tkc.Token.block_comment_buffer
                i+=1
                if text[i:i+2]=="*/":
                    comment_buffer+=text[i:i+2]
                    tkc.Token.block_comment_buffer+=text[i:i+2]
                    tkc.Token.in_comment=False
                    # comment_buffer=tkc.Token.block_comment_buffer
                    # tkc.Token.block_comment_buffer=''
                    print("end detected")
                    return comment_buffer, text.replace(comment_buffer, '', 1)
            
            else: return None
        tkc.Token.line_num+=1
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

# def remove_comments(code):
#     # Remove block comments
#     code = remove_block_comments(code)
#     # Remove inline comments
#     code = remove_inline_comments(code)
#     return code
    
def remove_whitespace_type(tokens, category):
    new_tokens = []
    new_category = []
    for i in range(len(tokens)):
        if category[i] != "Whitespace":
            new_tokens.append(tokens[i])
            new_category.append(category[i])
    return new_tokens, new_category

def getlines(code):
    #Splits the code into lines
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
        # if char is None:
        #     print("charnone")
        #     return '',token
        if char in const.delimiters["n_delim"] and tkc.LexerCheck.is_Whole(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char
    
def get_dec(token):
    token_cpy=''
    temp_token=''
    dec_detected=False
    for char in token:
        if char in const.delimiters["n_delim"] and tkc.LexerCheck.is_Dec(temp_token):
            # token_cpy=re.sub(re.escape(temp_token), '',token, count=1)
            token_cpy=token.replace(temp_token, '', 1) 
            return temp_token, token_cpy       
        else:
            temp_token+=char

# def get_lit(token):
#     if get_keyword(token)==const.boolean:
#         return 

def get_keyword(token):
    token_cpy=''
    temp_token=''
    keyword_detected=False
    for i,char in enumerate(token):
        if temp_token is None:
            return '',token
        elif ((temp_token in const.keywords) and (char in const.keywords_delims[temp_token])) or (temp_token=="when" and token[i:i+1]=="::"):
            # token_cpy=re.sub(temp_token, '',token, count=1)
            token_cpy=token.replace(temp_token, '', 1)
            keyword_detected=True
            return temp_token, token_cpy
               
        else:
            temp_token+=char
   
def get_identifier(token):
    token_cpy=''
    temp_token=''
    for char in token:
        if char in const.delimiters["id_delim"] and tkc.LexerCheck.is_Identifier(temp_token) and temp_token not in const.keywords:
            # token_cpy=re.sub(temp_token, '',token, count=1)
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
                # token_cpy=tokencode.replace(token, '', 1)
                # return f"Invalid Delimiter {tokencode[position]}", token_cpy    
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
        elif token[i] in const.all_symbols_nonop and token[i+1] in const.symbols_delims[token[i]]:
            symbol_buffer+=token[i]
            return token[i], token.replace(token[i], '', 1)
        elif token[i:2]=="::" and len(token)==2: 
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
        # if re.match(space, char):
        #     token_cpy=re.sub(space, '',token, count=1)
        #     return char, token_cpy       
        if char==" ":
            token_cpy=token.replace(char, '', 1)
            return char, token_cpy
        else:return None
    
def get_text(token):
    #Returns the text token and the remaining code
    token_cpy=''
    temp_token=''
    text_detected=False
    for i,char in enumerate(token):
        try:
            check_concat=char+token[i+1]+token[i+2]
        except IndexError:
            check_concat=''
        if (char in const.delimiters["txt_delim"] or check_concat=="...") and tkc.LexerCheck.is_Text(temp_token):

            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char

def get_next_char(input_string, current_index):
    if current_index < len(input_string)-1:
        return input_string[current_index+1]
    else:
        return None
        
def get_lit(token):
    token_cpy=''
    temp_token=''
    for char in token:
        if char in const.delimiters["n_delim"] and tkc.LexerCheck.is_Literal(temp_token):
            token_cpy=token.replace(temp_token, '', 1)
            return temp_token, token_cpy       
        else:
            temp_token+=char


#endregion


def prepare(code):
#Prepares the code for tokenization. Removes comments, extra newline characters, and extra spaces.
# Returns each line of code as a list of strings; ignores empty lines.
    templines=getlines(code) #remove_comments(
    lines=[] 
    for i in range(len(templines)):
        # if templines[i]=="": #Skips empty lines
        #     continue
        lines.append(templines[i])
    return lines

