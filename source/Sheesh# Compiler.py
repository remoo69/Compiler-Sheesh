# import source.helper as helper
import sys

from source.SyntaxAnalyzer import parser2
sys.path.append( '.' )
from tkinter import *
from tkinter import constants
from tkinter import ttk
import source.LexicalAnalyzer.lexerpy as lex
# import source.LexicalAnalyzer.prepare as prep
from tkinter import filedialog
# import source.SyntaxAnalyzer.grammar as grammar
# import source.SyntaxAnalyzer.parser1 as parser

# run error reporting
def fill_err_table():
    pass

# run lexer function
def fill_lex_table():
    pass

def on_scroll(*args):
    line_numbers.yview_moveto(args[0])
    txt_editor_pane.yview_moveto(args[0])

def remove_whitespace_type(tokens):
    for token in tokens:
        if token.type == "Whitespace" or token.type == "Block Comment" or token.type == "Inline Comment":
            tokens.remove(token)
    return tokens

def run_lex():
    print("Button pressed")
    code=txt_editor_pane.get("1.0", END)
    tokens,error=lex.Lexer.tokenize(code)
    print_lex(tokens)
    print_error(error)
    lex_table_pane.config(state="disabled")
    error_pane.config(state="disabled")

def run_parser():
    
    print("Button pressed")
    code = txt_editor_pane.get("1.0", END)
    tokens, error = lex.Lexer.tokenize(code)
    tokens = remove_whitespace_type(tokens)
    if error:
        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, "Can't Parse, Resolve Lexical Errors:\n")
        for err in error:
            error_pane.insert(constants.END, f'{err}\n')
    else:
        error_pane.config(state="disabled")
        # Continue with the rest of the code
    # Call your parser function here
    # If there is a syntax error, display it in the error pane
   
        # Call your parser function
    # If there is no syntax error, continue with the rest of the code
    # parser.syntax_analyzer(grammar.Grammar.cfg, code)
        parse=parser2.SyntaxAnalyzer(tokens)
        result, errors=parse.parse()  

        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, f'Syntax Error:\n')
        for error in errors:
            error_pane.insert(constants.END, f"{error}\n")
        error_pane.config(state="disabled")

        if len(errors) == 0:
            print("No errors")
            # print()

        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")

def print_lex(tokenlist):                      # Print Text to Lexical Pane
    print("Printing lex")
    lex_table_pane.config(state="normal")
    lex_table_pane.delete('1.0', constants.END)
    lex_table_pane.insert(constants.END, "LEXEME\t\t\tTOKEN\n\n")
    # token=prep.remove_whitespace_type(value,type)
    # j=0
    # while j < len(tokenlist):
        # if category[j]=="Keyword" or category[j]=="Symbol" or category[j]=="Operator":
        #     category[j]=char
    for i in range(len(tokenlist)):
        # if type[i] == 'Error Category' or type[i] == 'Whitespace' or type[i] == 'None':
        #     continue
        # else:  
        if tokenlist[i].type=="Whitespace":
            continue
        else:
            lex_table_pane.insert(
                constants.END, f'{str(tokenlist[i].value) if len(str(tokenlist[i].value))<=15 else str(tokenlist[i].value)[:10] + "..."}\t\t\t{str(tokenlist[i].type)}\n')


def print_error(error):
    error_pane.config(state="normal")
    error_pane.delete('1.0', constants.END)
    for err in range(len(error)):
        if err+1 == len(error):
            if error[err] != '':
                error_pane.insert(constants.END, f'{error[err]}\n')
        else:
            if error[err] != '':
                if error[err] != error[err+1]:
                    error_pane.insert(constants.END, f'{error[err]}\n')
            else:
                continue


def load_file():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r") as file:
            txt_editor_pane.delete("1.0", END)
            txt_editor_pane.insert("1.0", file.read())

# sets the tab spaces to be 4 every time it's pressed
def tab_pressed(event:Event) -> str:
    txt_editor_pane.insert("insert", " "*4)
    # Prevent the default tkinter behaviour
    return "break"

root = Tk()

root.geometry("939x634")
root.resizable(False,False)
root.title("Sheesh Compiler")

# config color collection
clr_bg = "#2D2D2D"
clr_black = "#202020"
clr_gray = "#272727"

root.configure(bg=clr_bg)

# style scrollbar
style = ttk.Style()
style.theme_use("clam")  
style.configure("Vertical.TScrollbar", troughcolor=clr_black, background=clr_black, gripcount=0, gripcolor=clr_black)



# setting main layout
mainpane = Canvas(
    root,
    bg=clr_black,
    height=634,
    width=939,
    bd=0,
    highlightthickness=0,
    relief="ridge")

mainpane.place(x=0,y=0)


line_numbers = Text(root, bd=0, bg=clr_black, fg="#FFFFFF", font=('Open Sans', 11), width=4, wrap="none", state="disabled")
line_numbers.place(x=5,y=50,width=20,height=390)

# setting editor section
txt_editor_pane = Text(
    bd=0,
    bg=clr_gray,
    # highlightcolor=
    highlightthickness=0,
    fg="#FFFFFF",
    insertbackground="white",
    padx=10,
    pady=10,
    font=('Open Sans', 11,),) 


txt_editor_pane.place(x=30,y=40,
                      width=600,height=390)
txt_editor_pane.bind("<Tab>", tab_pressed)
# txt_editor_pane.pack(side="left", fill="both", expand=True)

# scrollbar = Scrollbar(root, command=on_scroll)
# scrollbar.pack(side="right", fill="y")
# line_numbers.configure(yscrollcommand=scrollbar.set)
# txt_editor_pane.configure(yscrollcommand=scrollbar.set)

# setting lexer output section
lex_table_pane = Text(
    bd=0,
    bg=clr_gray,
    highlightthickness=0,
    fg="#FFFFFF",
    padx=10,
    pady=10,
    font=('Open Sans', 10),
    state = "disabled",)

lex_table_pane.place(
    x=640,
    y=40,
    width=300,
    height=565)

# header section
header_pane = Text(
    bd = 0,
    bg = clr_gray,
    padx = 10,
    pady = 10,
    font = ('Open Sans', 10),
)

header_pane.place(
    x=0,
    y=10,
    width=939,
    height=25,
)

# title = mainpane.create_text(
#     10, 20,
#     text="Sheesh",
#     font=('Open Sans ExtraBold', 20),
#     fill="#211B36",
# )

# setting lexer output section
error_pane = Text(
    bd=0,
    bg=clr_gray,
    highlightthickness=0,
    fg="#FFFFFF",
    padx=10,
    pady=10,
    font=('Open Sans', 10),
    state = "disabled",)

error_pane.place(x=30,y=435,
               width=600,height=170)


# run lexer function button
run_img = PhotoImage(file="source/assets/run.png") 
load_img=PhotoImage(file="source/assets/load.png")
lex_btn = Button(
        image=run_img,
        compound=LEFT,
        bg=clr_gray,
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        activeforeground="#FFFFFF",
        justify="center",
        command=run_lex,
)
lex_btn.place(x=15,y=10,width=25,height=25)
load_btn=Button(
    image=load_img,
        compound=LEFT,
        bg=clr_gray,
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        # activeforeground="#FFFFFF",
        justify="center",
        command=load_file,

)
load_btn.place(x=50,y=10,width=25,height=25)


parse_btn = Button(
        image=run_img,
        compound=LEFT,
        bg=clr_gray,
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        activeforeground="#FFFFFF",
        justify="center",
        command=run_parser,
)
parse_btn.place(x=80,y=10,width=25,height=25)

scrollbar = ttk.Scrollbar(
    txt_editor_pane, 
    orient='vertical',
    command=txt_editor_pane.yview,
)
scrollbar.pack(side=RIGHT, fill=Y)
line_numbers.configure(yscrollcommand=scrollbar.set)
txt_editor_pane.configure(yscrollcommand=scrollbar.set)
# txt_editor_pane['yscrollcommand'] = scrollbar.set


def update_line_numbers(*args):
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    lines = txt_editor_pane.get("1.0", "end").count("\n")
    line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, lines + 1)))
    line_numbers.config(state="disabled")

def update_line_numbers_on_scroll(*args):
    update_line_numbers()
    on_scroll(*args)

txt_editor_pane.bind("<KeyRelease>", update_line_numbers)
txt_editor_pane.bind("<MouseWheel>", update_line_numbers_on_scroll)

root.mainloop()
