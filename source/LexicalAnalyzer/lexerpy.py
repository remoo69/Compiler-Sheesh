# import re
# import tokenclass as tk
# import pandas as pd
import sys
sys.path.append( '.' )
import source.core.constants as const
import source.LexicalAnalyzer.prepare as prep
import source.core.error_handler as err
import source.LexicalAnalyzer.tokenclass as tkc
from typing import Tuple, List

# This lexer follows the principle of longest match. It will match the longest possible token at each step.

# Say for example that a token dec15# is passed. The lexer will detect the token line by line until a delimiter is found. Thus, 
# Even if dec is a reserved word, the lexer will not detect it as such because it will be detected as an identifier due to the delimiter # being after the 15 value.
# If dec were to be used as a keyword, the syntax should be: dec identifier=15#. Here, dec is detected as a keyword due to the delimiter {space}

# Each function checks if a token is within a valid token type based on their respective regular expressions and delimiters.
# As such, the delimiter of the token should be passed along with the token itself. Do note that the delimiter itself should be considered a token.

# Update: Let the inputs be a list of tokens per line. This way the lexer can check each token while keeping track of its delimiter while not having to include the delimiter itself in the detection.
# This is so the lexer can detect the token type of the delimiters themselves.


class Lexer:
    @staticmethod
    def gettokens(code: str) -> tuple[list[tkc.Token], list[err.Error]]:
        tokens = []
        errors = []
        current_token: str = ''
        tktype = ''
        block_comment_buffer=''
        tkc.Token.tok_num=1
        # if tkc.Token.in_comment:
        #     if result:=prep.get_block_comments(code, tkc.Token.in_comment):
        #         current_token, code=result
        # else:
        while code:
            
            if result:=prep.get_block_comments(code):
                current_token, code=result
                tkc.Token.block_start_line=tkc.Token.line_num
                if tkc.Token.in_comment:
                    break
            elif result:=prep.get_inline_comments(code):
                current_token, code=result
            # elif result:=prep.get_sus(code):
            #     current_token, code=result
            elif result := prep.get_keyword(code):
                current_token, code = result
                tktype = "keyword"
            elif result := prep.get_identifier(code): 
                current_token, code = result
                tktype = "identifier"
            elif result:=prep.get_charr(code):
                current_token, code = result
                tktype = "charr"
            elif result := prep.get_text(code):
                current_token, code = result
                tktype = "text"
            elif result := prep.get_dec(code):
                current_token, code = result
                tktype = "dec"
            elif result := prep.get_whole(code):
                current_token, code = result
                tktype = "whole"
            elif result := prep.get_symbol(code):
                current_token, code = result
                tktype = "symbol"
            elif result := prep.get_operator(code):
                current_token, code = result
            elif result := prep.get_space(code):
                current_token, code = result
            else:
                if result := err.LexError.get_errors(code):
                    error = result
                    code = result.remaining if result.remaining is not None else ''
                    errors.append(error)
            

            if current_token:
                category=tkc.LexerCheck.categorize(current_token)
                if category == "Keyword" or category =="Operator" or category=="Symbol":
                    if current_token=="cap" or current_token=="nocap":
                        token=tkc.Token(value=current_token, type="Sus", attribute=current_token, line=tkc.Token.line_num, position=tkc.Token.tok_num)
                    else:
                        token = tkc.Token(value=current_token, type=current_token, attribute=current_token, line=tkc.Token.line_num, position=tkc.Token.tok_num)
                elif category=="Identifier":
                    try:
                        if current_token in tkc.Token.id_dict:
                            tktype=tkc.Token.id_dict[current_token]
                        else:
                            tkc.Token.id_dict[current_token]=f"Identifier {tkc.Token.idnum}"
                            tktype=f"Identifier {tkc.Token.idnum}"
                            tkc.Token.idnum+=1
                    except KeyError:
                        tktype=tkc.Token.id_dict[current_token]
                        print("tktype is ", tktype)

                    token = tkc.Token(value=current_token, type="Identifier", attribute=tktype, line=tkc.Token.line_num, position=tkc.Token.tok_num)
                else:
                    if category in ["Whole", "Dec"]:
                        token = tkc.Token(value=current_token, type=category, line=tkc.Token.line_num, position=tkc.Token.tok_num, numerical_value=float(current_token))
                    else:
                        token = tkc.Token(value=current_token, type=category, line=tkc.Token.line_num, position=tkc.Token.tok_num,)
                tkc.Token.tok_num+=1    
                tokens.append(token)
                current_token=''
        tokens.append(tkc.Token(value="EOL", type="Newline", line=tkc.Token.line_num, position=tkc.Token.tok_num))

        tkc.Token.line_num+=1
        return tokens, errors


    @staticmethod    
    def tokenize(codes):
        tkc.Token.tok_num=1
        tkc.Token.idnum=1
        tkc.Token.id_dict={}
        tkc.Token.block_comment_buffer=''
        tkc.Token.in_comment=False
        tkc.Token.line_num=1

        lines = prep.prepare(codes)
        tokens = []
        errors = []
        tkc.Token.line_num=1
        comment_buffer=''
        for line in lines:

            if tkc.Token.in_comment:
                if result:=prep.get_block_comments(line):
                    current_token, linecopy=result
                    if tkc.Token.in_comment:
                        continue
                    else:
                        block_token=tkc.Token(value=tkc.Token.block_comment_buffer, type="Block Comment", line=tkc.Token.line_num, position=tkc.Token.tok_num)
                        tokens.append(block_token)
                        tkc.Token.in_comment=False
                        tkc.Token.block_comment_buffer=''
                        if linecopy:
                            tkc.Token.line_num-=1
                            lexemes, error = Lexer.gettokens(linecopy)
                            errors.extend(error)
                            tokens.extend(lexemes)
            else:
                lexemes, error = Lexer.gettokens(line)
                errors.extend(error)
                tokens.extend(lexemes)  # Use extend instead of append to add the lexemes to the list

        # error=error_handler
        if tkc.Token.in_comment:
            error=err.Error(type= f"Invalid Block Comment", line=tkc.Token.block_start_line, errorval=tkc.Token.block_comment_buffer, remaining=None)
            errors.append(error)
        return tokens, errors
    



if __name__=="__main__":
    print(Lexer.gettokens("    up(“The speed of the fluid is: $d m/s\n\", v2)#"))
