import sys
sys.path.append( '.' )
import source.LexicalAnalyzer.Prepare as prep
import source.core.error_handler as err
import source.core.symbol_table as symb

# This lexer follows the principle of longest match. It will match the longest possible token at each step.

# Say for example that a token dec15# is passed. The lexer will detect the token line by line until a delimiter is found. Thus, 
# Even if dec is a reserved word, the lexer will not detect it as such because it will be detected as an identifier due to the delimiter # being after the 15 value.
# If dec were to be used as a keyword, the syntax should be: dec identifier=15#. Here, dec is detected as a keyword due to the delimiter {space}

# Each function checks if a token is within a valid token type based on their respective regular expressions and delimiters.
# As such, the delimiter of the token should be passed along with the token itself. Do note that the delimiter itself should be considered a token.

# Update: Let the inputs be a list of tokens per line. This way the lexer can check each token while keeping track of its delimiter while not having to include the delimiter itself in the detection.
# This is so the lexer can detect the token type of the delimiters themselves.


class Lexer:

    def __init__(self, code: str):
        
        self.code=code
        self.tokens=[]
        self.errors=[]
        self.no_tokens=[symb.Token(value="NO TOKENS", type= "NO TOKENS")]


    @staticmethod
    def gettokens(code: str) -> tuple[list[symb.Token], list[err.Error]]:
        tokens = []
        errors = []
        current_token: str = ''
        tktype = ''
        block_comment_buffer=''
        symb.Token.tok_num=1
        # if symb.Token.in_comment:
        #     if result:=prep.get_block_comments(code, symb.Token.in_comment):
        #         current_token, code=result
        # else:
        while code:
            
            if result:=prep.get_block_comments(code):
                current_token, code=result
                symb.Token.block_start_line=symb.Token.line_num
                if symb.Token.in_comment:
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
                category=prep.LexerCheck.categorize(current_token)
                if category == "Keyword" or category =="Operator" or category=="Symbol":
                    if current_token=="cap" or current_token=="nocap":
                        token=symb.Token(value=current_token, type="Sus", attribute=current_token, line=symb.Token.line_num, position=symb.Token.tok_num)
                    else:
                        token = symb.Token(value=current_token, type=current_token, attribute=current_token, line=symb.Token.line_num, position=symb.Token.tok_num)
                elif category=="Identifier":
                    try:
                        if current_token in symb.Token.id_dict:
                            tktype=symb.Token.id_dict[current_token]
                        else:
                            symb.Token.id_dict[current_token]=f"Identifier {symb.Token.idnum}"
                            tktype=f"Identifier {symb.Token.idnum}"
                            symb.Token.idnum+=1
                    except KeyError:
                        tktype=symb.Token.id_dict[current_token]
                        print("tktype is ", tktype)

                    token = symb.Token(value=current_token, type="Identifier", attribute=tktype, line=symb.Token.line_num, position=symb.Token.tok_num)
                else:
                    if category in ["Whole", "Dec"]:
                        try:
                            token = symb.Token(value=current_token, type=category, line=symb.Token.line_num, position=symb.Token.tok_num, numerical_value=float(current_token))
                        except ValueError:
                            token = symb.Token(value=current_token, type=category, line=symb.Token.line_num, position=symb.Token.tok_num, numerical_value=float(current_token[1:-1]))
                    else:
                        token = symb.Token(value=current_token, type=category, line=symb.Token.line_num, position=symb.Token.tok_num,)
                symb.Token.tok_num+=1    
                tokens.append(token)
                current_token=''
        tokens.append(symb.Token(value="EOL", type="Newline", line=symb.Token.line_num, position=symb.Token.tok_num))

        symb.Token.line_num+=1
        return tokens, errors


    def tokenize(self):
        symb.Token.tok_num=1
        symb.Token.idnum=1
        symb.Token.id_dict={}
        symb.Token.block_comment_buffer=''
        symb.Token.in_comment=False
        symb.Token.line_num=1

        lines = prep.prepare(self.code)
        tokens = []
        errors = []
        symb.Token.line_num=1
        comment_buffer=''
        for line in lines:

            if symb.Token.in_comment:
                if result:=prep.get_block_comments(line):
                    current_token, linecopy=result
                    if symb.Token.in_comment:
                        continue
                    else:
                        block_token=symb.Token(value=symb.Token.block_comment_buffer, type="Block Comment", line=symb.Token.line_num, position=symb.Token.tok_num)
                        tokens.append(block_token)
                        symb.Token.in_comment=False
                        symb.Token.block_comment_buffer=''
                        if linecopy:
                            symb.Token.line_num-=1
                            lexemes, error = Lexer.gettokens(linecopy)
                            errors.extend(error)
                            tokens.extend(lexemes)
            else:
                lexemes, error = Lexer.gettokens(line)
                errors.extend(error)
                tokens.extend(lexemes)  # Use extend instead of append to add the lexemes to the list

        # error=error_handler
        if symb.Token.in_comment:
            error=err.Error(type= f"Invalid Block Comment", line=symb.Token.block_start_line, errorval=symb.Token.block_comment_buffer, remaining=None)
            errors.append(error)
        
        self.errors=errors
        self.tokens=tokens
    



if __name__=="__main__":
    print(Lexer.gettokens("    up(“The speed of the fluid is: $d m/s\n\", v2)#"))
