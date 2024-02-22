# import re
# import tokenclass as tk
# import pandas as pd
import source.core.constants as const
import prepare as prep
import source.core.error_handler as err
import tokenclass as tkc
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
            elif result := prep.get_keyword(code):
                current_token, code = result
                tktype = "keyword"
            elif result := prep.get_identifier(code): 
                current_token, code = result
                tktype = "identifier"
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
                    token = tkc.Token(value=current_token, type=current_token, attribute=current_token, line=tkc.Token.line_num)
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

                    token = tkc.Token(value=current_token, type=tktype, line=tkc.Token.line_num)
                else:
                    token = tkc.Token(value=current_token, type=category, line=tkc.Token.line_num)
                tokens.append(token)
                current_token=''

        tkc.Token.line_num+=1
        return tokens, errors
    
    #region previous gettokens
        # # Iterate through a line of code per character and return as a list of tokens
        # # Check each character
        # tokencode = code
        # tokens = []
        # errors = []
        # current_token: str = ''
        # tktype = ''

        # while tokencode:
        #     if result := prep.get_keyword(tokencode):
        #         current_token, tokencode = result
        #         tktype = "keyword"
        #     elif result := prep.get_identifier(tokencode):
        #         current_token, tokencode = result
        #         tktype = "identifier"
        #     elif result := prep.get_text(tokencode):
        #         current_token, tokencode = result
        #         tktype = "text"
        #     elif result := prep.get_dec(tokencode):
        #         current_token, tokencode = result
        #         tktype = "dec"
        #     elif result := prep.get_whole(tokencode):
        #         current_token, tokencode = result
        #         tktype = "whole"
        #     elif result := prep.get_symbol(tokencode):
        #         current_token, tokencode = result
        #         tktype = "symbol"
        #     elif result := prep.get_operator(tokencode):
        #         current_token, tokencode = result
        #     elif result := prep.get_space(tokencode):
        #         current_token, tokencode = result
        #     else:
        #         if result := err.LexError.get_errors(tokencode):
        #             errorval, tokencode = result
        #             error = err.Error(errorval, 1, tokencode, None)
        #             errors.append(error)

        #     if current_token:
        #         token = tkc.Token(value=current_token, line=1, type="default", attribute="default", position=2)
        #         tokens.append(token)
        #         current_token = ''
        #     else:  # Handles null chars
        #         pass
        # return tokens, errors
    #endregion

    @staticmethod    
    def tokenize(codes):
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
                        block_token=tkc.Token(value=tkc.Token.block_comment_buffer, type="Block Comment", line=tkc.Token.line_num)
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
    
    #region previous err handler
    # @staticmethod    
    # def error_handler(current, tokenized, remaining):
    #     print(f"pumasok ay {current, tokenized, remaining}")
    #     error_val = current
    #     try:
                        
    #         if current=='' or current is None:
    #             return f"Type 1 Invalid Null Delimiter for \"{tokenized[-1]}\", remaining: {remaining}"
    #         # This portion is for delimiter mismatches
    #         if remaining is None and not Lexer.is_Symbol(error_val):
    #             return f"Type 2 Invalid Null Delimiter for \"{current}\""
            
    #         if not Lexer.is_Valid_Token(current):
    #             return f"{current} is not a valid Token"

    #         if Lexer.categorize(error_val) == "Error Category":
    #                 return f"{error_val} Invalid Syntax for Token"

    #         if Lexer.is_Identifier(error_val) and len(error_val)>9:
    #             return f"Type 3 Identifier {error_val} contains legal characters but is too long "
    #         # Categorize previously matched token
    #         token_prev = tokenized[-1]
    #         category = Lexer.categorize(token_prev)

    #         # Check if the delimiter is valid for the token category (prev)
    #         if category == "Keyword":
    #             if error_val not in const.keywords_delims[tokenized[-1]]:
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category == "Identifier":
    #             if error_val not in const.delimiters["id_delim"]:
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category == "Symbol":
    #             if not Lexer.is_Numeric(error_val) and not Lexer.is_Identifier(error_val) and not Lexer.is_Operator(error_val):
    #                 return f"{error_val} Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category == "Operator":
    #             if error_val not in const.delimiters["op"] and not Lexer.is_Literal(error_val) and not Lexer.is_Identifier(error_val):
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category == "Text":
    #             if error_val not in const.delimiters["txt_delim"] and error_val not in const.concat:
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category in ["Whole", "Dec"]:
    #             if error_val not in const.delimiters["n_delim"] :
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""
    #         elif category=="Whitespace":
    #             if error_val not in const.delimiters["space_delim"] or Lexer.categorize(error_val) not in const.valid_tokens:
    #                 return f"Invalid Delimiter for \"{category}\", \"{token_prev}\""

            
    #         else: #if not delim error, then could be token syntax error. 
    #             return "Invalid Token Syntax"
            
    #     except IndexError:
    #         return "Invalid Delimiter and Statement"

#endregion



# def main():
#     code = prep.file_to_string(r"C:\Users\anton\Desktop\input1.sheesh")
#     tokens = prep.prepare(code)
#     tokenized=tokenize(tokens)
#     # tokens_dict = {token.value: token.quality for token in tokens}
#     # df = pd.DataFrame(tokens_dict.items(), columns=['Token', 'Tag'])
#     # print(tabulate(df, headers='keys', tablefmt='psql'))
#     print(tokens)
#     print(tokenized)

# main()
