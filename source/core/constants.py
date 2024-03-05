# Description: Contains the constants used in the compiler
#List of Keywords
keywords = ["text", "charr","whole", "dec", "sus", "blank", "sheesh", "yeet", "based",#added charr, lit->sus, bruh->yeet, steady->based
            "kung", "ehkung", "deins", "choose", "when", "bet","for", "to", #habang->bet
            "step", "felloff", "pass", "use", "from", "nocap", "cap", "default", "up", "pa_mine"]     #added choose->choice, default, termins->felloff, gg->pass
DATA_TYPES=["text","charr", "whole", "dec", "lit", "blank"]
valid_tokens=["Keyword", "Identifier", "Dec", "Whole", "Symbol", "Operator", "Text", "Charr", "Lit", "Whitespace"]
valid_cfg_terminals=[ "Identifier", "Dec", "Whole", "Text","Charr", "Lit", "null", "sheesh", "text_literal", "dec_literal", "whole_literal", "lit_literal",
                     "pa_mine", "up"]#bigay->up, kuha->pa_mine
operators_and_symbols = ['=', '+=', '-=', '*=', '/=', '%=', '==', '>', '>=', '<', '<=', '!=', '!', '&', 
                         '|', '+', '-', '*', '/', '%', '…', '#', '[',']', '{','}', '(',')', '/*', '*/', '//', '“', 
                         '”', '.', '::', ',', '$', '\n', '\t', '\"', '\\', '\\$']
terminals=valid_cfg_terminals
terminals.extend(operators_and_symbols)
terminals.extend(keywords)


#Regular Definitions
zero = ['0']
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
abc_small = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
abc_cap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nums = zero+digits
boolean = ['nocap', 'cap']
aop = ['+', '-', '*', '/', '%']
asop = ['=', '+=', '-=', '*=', '/=', '%=']
rop1 = ['==', '!=', '<', '>', '<=', '>=']
rop2 = ['<', '>', '!', '=']
lop = ['!', '|', '&']
comma = [',']
concat = ['...']
null = None
space = [' ']
esc_seq = [r'\t', r'\n', r'\"', r'\\', r'\$']
op = aop+rop2+lop
symbols = op+comma+[ '#', '_', '.', '@', '^', '&', '(', ')', '`', '“', '~', '::', '?', '$', ';', '[', ']', '\\', '{', '}', '/', '`', '^']#space+
alph_all = abc_cap+abc_small
alph_num = alph_all+digits+zero
alph_id = alph_num+['_']
comments = alph_num+symbols
text = alph_num+esc_seq+op+comma+space+['#', '_', '.', '@', '^', '&', '(', ')', '`', '~', '::', '?', '$', ';', '[', ']', '{', '}', '/', '`', '^']
single_symbols=aop+rop2+lop
compound_symbols=['+=', '-=', '*=', '/=', '%=','==', '!=','<=', '>=']
all_op=op+asop+rop1+lop+comma+concat+rop2
non_op=comma+['#', '_', '.', '@', '^', '&', '(', ')', '`', '~', '::', '?', '$', ';', '[', ']', '{', '}', '/', '`', '^']
whitespace=space+['\n', '\t', '\t']
grouping_symbols=["{","}", "(", ")", "[", "]" ]
other_symbols=["#", "::", ]
all_symbols_nonop=grouping_symbols+other_symbols+[",", "."]
invalid_id_char=op+comma+['#', '.', '@', '^', '&', '(', ')', '`', '~', ':', '?', '$', ';', '[', ']', '{', '}', '/', '\\', '`', '^', "'", '"']
invalid_text_char=['"', ]
invalid_symbols=["@", "^", "&", "`", "~", "?", "$", ";", "'", '`',":", "\\" ]
#Delimiters used in the Transition Diagram/DFA



delimiters = {
    "op": op,
    "comma": comma,
    "alph_num": alph_num,
    "alph_all": alph_all,
    "concat": concat,
    "delim1": " ",
    "delim2": [" ","#", ")", "|"],
    "delim3": ["(", " ", '{', None],
    "delim4": [" ","\\","{"],
    "delim5": alph_num+[" ","("],
    "delim6": alph_num+[" ", "{"],
    "delim7": [" ","}", ""],
    "delim8": [" ", ""],
    "delim9": alph_num+[" ","(","{", "!", '"', "'"],#added "
    "delim10": alph_all+[" ","(","!"],
    "delim11": alph_num+[" ","(","!"],
    "delim12": op+comma+[" ","#","[",")" ],
    "delim13": alph_num+[" ","\\","(", "{",None],
    "delim14": alph_all+[" ","#","}",",",None],
    "delim15": alph_num+[" ", "!","(", ")", '"', "-", "'"],#added ); added -; added "
    "delim16": op+comma+[" ", "#", ")", "{","}", ":"],#added {
    "delim17": alph_num+[" ", '"', "\\", "'"],
    "delim20": ['"', "'"],
    "delim21": [" ", ":","::"],
    "delim22": [" ","("],
    "txt_delim": comma+[" ", "#", ")", "}", ":"], #removed concat
    "blk_delim": [" ", "\\",None],
    "id_delim": op+comma+[" ", "#", "(",")", "[", "]", "{", "}",".", ":"],
    "n_delim": op+comma+[" ", "#", "(", ")", ":", "]", "}",","],
    "space_delim": alph_num+[" ", "#", "(", ")", ":", "}", "]", ","]
}   
keywords_delims={"text":delimiters["delim1"], 
                 "charr":delimiters["delim1"], #added
                 "whole":delimiters["delim1"], 
                 "dec": delimiters["delim1"], 
                 "sus":delimiters["delim1"], #added "
                 "lit":delimiters["delim1"], 
                 "blank":delimiters["delim1"], 
                 "sheesh":delimiters["delim3"], 
                 "yeet":delimiters["delim2"], 
                 "based":delimiters["delim1"],
                 "kung":delimiters["delim3"], 
                 "ehkung":delimiters["delim3"], 
                 "deins":delimiters["delim4"], 
                 "choose":delimiters["delim3"], #from choice to choose
                 "when":delimiters["delim1"], 
                 "bet":delimiters["delim3"], 
                 "for":delimiters["delim22"], 
                 "to":delimiters["delim1"], 
                 "step":delimiters["delim1"], 
                 "felloff":delimiters["delim2"], 
                 "pass":delimiters["delim2"], 
                 "use":delimiters["delim1"], 
                 "from":delimiters["delim1"],
                 "cap":delimiters["delim2"],
                 "nocap":delimiters["delim2"],
                 "up":delimiters["delim3"],
                 "pa_mine":delimiters["delim3"],
                 "sheesh":delimiters["delim3"],
                 "default":delimiters["delim21"]}

symbols_delims={
#------------------------------------- Operators ------------------------------------------------------    
                "+":delimiters["delim5"],
                "+=":delimiters["delim5"],
                "-":delimiters["delim5"],
                "-=":delimiters["delim5"],
                "*":delimiters["delim5"],
                "*=":delimiters["delim5"],
                "/":delimiters["delim5"],
                "/=":delimiters["delim5"],
                "%":delimiters["delim5"],
                "%=":delimiters["delim5"],
                "=":delimiters["delim9"],
                "==":delimiters["delim6"],
                ">":delimiters["delim5"],
                ">=":delimiters["delim5"],
                "<":delimiters["delim5"],
                "<=":delimiters["delim5"],
                "!":delimiters["delim10"],
                "!=":delimiters["delim5"],
                "&":delimiters["delim11"],
                "|":delimiters["delim11"],
                "...": ['"'," "],
#------------------------------------- Symbols ------------------------------------------------------
                "[":delimiters["delim5"],
                "]":delimiters["delim12"],
                "{":delimiters["delim13"],
                "}":delimiters["delim14"],
                "(":delimiters["delim15"],
                ")":delimiters["delim16"],
                ",":delimiters["delim6"],
                "#":delimiters["delim7"],
                # ":":delimiters["delim8"],
                "::":delimiters["delim8"],
                r"\n":delimiters["delim17"],
                r"\"":delimiters["delim17"],
                r"\t":delimiters["delim17"],
                r"\$":delimiters["delim17"],
                
                ' ': delimiters["space_delim"], 
                ".": alph_all}

RE_Literals={"text": r'^\"(?:(?!(?<!\\)").|\\")*\"$',
              "whole": r"^(0|([1-9]\d{0,4})|\(-[1-9]\d{0,4}\))$", 
              "pos_dec":   r'^(?:[0-9]\d{0,4}|0)\.\d{1,6}$', 
              "neg_dec": r'^\(-(?!0+(\.0+)?)\d{1,5}\.\d{1,6}\)$',
              "lit": boolean}

RE_Identifier=r'[a-zA-Z][a-zA-Z0-9_]*$' #removed {0,8}
RE_BlockComment=r'/\*.*?\*/'
RE_InlineComment=r'//.*?\n'

MAX_IDEN_LENGTH=30
WHOLE_MIN=-32768
WHOLE_MAX=32767
DEC_MIN=-32768.999999
DEC_MAX=32767.999999
