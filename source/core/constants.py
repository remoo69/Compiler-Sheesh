# Description: Contains the constants used in the compiler
# List of Keywords

class dtypes:
    charr="charr"
    whole="whole"
    dec="dec"
    text="text"
    sus="sus"
    
    blank="blank"


keywords = ["text", "charr","whole", "dec", "sus", "blank", "sheesh", "yeet", "based",
            "kung", "ehkung", "deins", "when", "bet", "choose","for", "to", #removed choice
            "step", "felloff", "pass", "use", "from", "nocap", "cap", "default", "up", "pa_mine", "def", "whilst"] # added def and whilst     

DATA_TYPES = ["text","charr", "whole", "dec", "sus", "blank"]

valid_tokens = ["Keyword", "Identifier", "Dec", "Whole", "Symbol", "Operator", "Text", "Charr", "Sus", "Whitespace"]

valid_cfg_terminals = ["Identifier", "Dec", "Whole", "Text", "Charr", "Sus", "null", "sheesh", "text_literal", "dec_literal", "whole_literal", "sus_literal",
                     "pa_mine", "up"]

operators_and_symbols = ['=', '+=', '-=', '*=', '/=', '%=', '==', '>', '>=', '<', '<=', '!=', '!', '&', 
                         '|', '+', '-', '*', '/', '%', '…', '#', '[',']', '{','}', '(',')', '/*', '*/', '//', '“', 
                         '”', '.', '::', ',', '$', '\n', '\t', '\"', '\\', '\\$']

terminals=valid_cfg_terminals
terminals.extend(operators_and_symbols)
terminals.extend(keywords)


MAX_IDEN_LENGTH=30
WHOLE_MIN=-32768
WHOLE_MAX=32767
DEC_MIN=-32768.999999
DEC_MAX=32767.999999

GBL="Global"
LOCAL="Local"

VAR="Variable"
FUNC="Function"
MOD="Module"
SEQ="Sequence"
CONST="Constant"

IMP="Imported"
PARAM="Parameter"
ARG="Argument"






class charr:
    def __init__(self, value):
        self.value=value
        self.type="char"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __add__(self, other):
        return charr(self.value+other.value)

    def __sub__(self, other):
        return charr(self.value-other.value)

    def __mul__(self, other):
        return charr(self.value*other.value)

    def __truediv__(self, other):
        return charr(self.value/other.value)

    def __mod__(self, other):
        return charr(self.value%other.value)

    def __eq__(self, other):
        return self.value==other.value

    def __ne__(self, other):
        return self.value!=other.value

    def __lt__(self, other):
        return self.value<other.value

    def __le__(self, other):
        return self.value<=other.value

    def __gt__(self, other):
        return self.value>other.value

    def __ge__(self, other):
        return self.value>=other.value

    def __and__(self, other):
        return self.value and other.value

    def __or__(self, other):
        return self.value or other.value

    def __xor__(self, other):
        return self.value ^ other.value

    def __lshift__(self, other):
        return self.value << other.value

    def __rshift__(self, other):
        return self.value >> other.value

    def __invert__(self):
        return ~self.value

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __round__(self, n):
        return round(self.value, n)

    def __floor__(self):
        return self.value.floor()

    def __ceil__(self):
        return self.value.ceil()

    def __trunc__(self):
        return self.value.trunc()

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return len(self.value)
    
class whole(int):
    def __init__(self,value=0) -> None:
        super().__init__()
        self.type="whole"

class dec(float):
    def __init__(self, value=0.0) -> None:
        super().__init__()
        self.type="dec"

class text(str):
    def __init__(self, value="") -> None:
        super().__init__()
        self.type="text"

class sus:
    def __init__(self, value) -> None:
        self.value=value
        self.type="sus"
        self.values={
            True:"nocap",
            False:"cap"
        }
    
types={
            "whole":whole,
            "dec":dec,
            "text":text,
            "sus":sus,
            "charr":charr
            }

py_types={
            "whole":int,
            "dec":float,
            "text":str,
            "sus":bool,
            "charr":charr
            }
literal_types={
            "Whole":int,
            "Decimal":float,
            "Text":str,
            "Sus":bool,
            "Charr":charr
            }

py_to_types={
            int:whole,
            float:dec,
            str:text,
            bool:sus,
            charr:charr
            }



format_spec={
            "w":int,
            "d":float,
            "t":str,
            "s":bool,
            "c":charr
            }

own_specifiers={
            "w":"whole",
            "d":"dec",
            "t":"text",
            "s":"sus",
            "c":"charr"
            }


#region Regular Definitions
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
esc_seq = [r'\t', r'\n', r'\"', r'\\']
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
whitespace=space+['\n', '\t']
grouping_symbols=["{","}", "(", ")", "[", "]" ]
other_symbols=["#", "::", ]
all_symbols_nonop=grouping_symbols+other_symbols+[",", "."]
invalid_id_char=op+comma+['#', '.', '@', '^', '&', '(', ')', '`', '~', ':', '?', '$', ';', '[', ']', '{', '}', '/', '\\', '`', '^', "'", '"', '“', '"', '”']
invalid_text_char=[] #['"', '“', '"', '”', ]
invalid_symbols=["@", "^", "&", "`", "~", "?", "$", ";", "'", '`',":", "\\"]
multi_charr=[r"'\0'", r"'\n'", r"'\t'",]

#endregion


# region Delimiters used in the Transition Diagram/DFA

delimiters = {
    "op": op,
    "comma": comma,
    "alph_num": alph_num,
    "alph_all": alph_all,
    "concat": concat,
    "delim1": " ",
    "delim2": [" ","#"],
    "delim3": ["(", " "],
    "delim4": [" ","\\","{"],
    "delim5": alph_num+[" ","(", "]", "["],
    "delim6": alph_num+[" ", "(", "{", "\"", "\'"],             # added: (,{,",'}
    "delim7": [" ","\\","}", ""],
    "delim8": [" ","\\", ""],
    "delim9": alph_num+[" ","(","{", "!", '"', '“', '"', '”', "\'"],           # added '
    "delim10": alph_all+[" ","(","!"],
    "delim11": alph_num+[" ","(","!", "\'"],
    "delim12": all_op+comma+[" ","#","[","]",")" ],
    "delim13": alph_num+[" ","\\","(", "{", "\"", None],
    "delim14": alph_all+comma+[" ","#", "}",None],
    "delim15": alph_num+[" ", "!","(", ")", '"', '“', '"', '”', "-", "\'"],    # added '
    "delim16": op+comma+[" ", "#", ")", "}", "{", ":", "]", "."], # added ] and : and .
    "delim17": alph_num+[" ", '"', '“', '"', '”', "\\"],
    "delim18": comma+[" ","#",")","|", "&","}"],                 # added delim18 for nocap and cap
    "delim19": alph_num+[" ", "(", "\'"],
    "delim20": alph_num+[" ","\""],     
    "delim21": alph_num+op+comma+[" ","#","(",")","{","}","\"","\'"],
    "delim22": [" ", ":","::"],                                 # added delim22 for default
    "delim23": [" ", ")"],             # added delim23 for whole
    "charr_delim": comma+[" ","#","=",")",":","::"],
    "txt_delim": comma+[" ", "#", ")", "}", ":", '=', ],
    "blk_delim": [" ", "\\",None],
    "id_delim": op+comma+[" ", "#", "(",")", "[", "]", "{", ".", ":"],
    "n_delim": op+comma+[" ", "#", "(", ")", ":", "]", "}"],
    "space_delim": alph_num+[" ", "#", "(", ")", ":", "}", "]", ","]
}  

keywords_delims={
                "based":delimiters["delim1"],
                "bet":delimiters["delim4"],   
                "blank":delimiters["delim23"], 
                "cap":delimiters["delim18"],   
                "charr":delimiters["delim1"], 
                "choose":delimiters["delim3"],
                "dec":delimiters["delim1"],   
                "def": delimiters["delim1"],
                "deins":delimiters["delim4"], 
                "default":delimiters["delim22"], 
                "ehkung":delimiters["delim3"],
                "felloff":delimiters["delim2"],
                "for":delimiters["delim3"],       
                "from":delimiters["delim1"],  
                "kung":delimiters["delim3"],  
                "nocap":delimiters["delim18"], 
                "pa_mine":delimiters["delim3"],
                "pass":delimiters["delim2"],  
                "sheesh":delimiters["delim3"],
                "step":delimiters["delim1"],  
                "sus":delimiters["delim1"],   
                "text":delimiters["delim1"],  
                "to":delimiters["delim1"],    
                "up":delimiters["delim3"],    
                "use":delimiters["delim1"],   
                "when":delimiters["delim1"],  
                "whole":delimiters["delim1"],
                "whilst": delimiters["delim3"], 
                "yeet":delimiters["delim2"],
}

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
                "...": ['"', '“', '"', '”'," ",]+alph_all, #added alph_all
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

#endregion



