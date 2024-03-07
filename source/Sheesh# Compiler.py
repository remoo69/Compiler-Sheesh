import sys
sys.path.append( '.' )
import source.LexicalAnalyzer.lexerpy as lex
import customtkinter as ctk
import tkinter as tk
from tkextrafont import Font

from tkinter import *
from PIL import Image, ImageTk
from tkinter import constants
from tkinter import ttk
from tkinter import filedialog
from tkinter import Event
from source.core.constants import keywords
from source.SyntaxAnalyzer import parser2

def highlight_reserve_word(*args):
    txt_editor_pane.tag_remove('found', '1.0',END)
    for word in keywords:   
        idx = '1.0'
        while idx:
            idx = txt_editor_pane.search(word, idx, nocase=1, stopindex=END)
            if idx:
                lastidx = '%s+%dc' % (idx, len(word))
                if txt_editor_pane.get(idx,lastidx).islower():
                    txt_editor_pane.tag_add('found', idx, lastidx)
                else:
                    txt_editor_pane.tag_add('reserveidenti', idx, lastidx)
                idx = lastidx

    txt_editor_pane.tag_config('found', foreground='yellow')
    txt_editor_pane.tag_config('reserveidenti', foreground='white')

def on_scroll(*args):
    line_numbers.yview_moveto(args[0])
    txt_editor_pane.yview_moveto(args[0])

def remove_whitespace_type(tokens):
    new_tokens = []
    for token in tokens:
        if token.type != "Whitespace" and token.type != "Block Comment" and token.type != "Inline Comment":
            new_tokens.append(token)
    return new_tokens

def run_lex():
    
    print("Button pressed")
    code=txt_editor_pane.get("1.0", END)
    tokens,error=lex.Lexer.tokenize(code)
    # tokens=remove_whitespace_type(tokens)
    print_lex(tokens)
    print_error(error)
    lex_table_pane.config(state="disabled")
    error_pane.config(state="disabled")


def run_parser():
    
    print("Button pressed")
    code = txt_editor_pane.get("1.0", END)
    tokens, error = lex.Lexer.tokenize(code)
    tokens = remove_whitespace_type(tokens)
    print_lex(tokens)
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
        errors=parse.parse()  

        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)

        if errors==[]:
            error_pane.insert(constants.END,"No errors")
        else:
            error_pane.insert(constants.END, f'Syntax Error:\n')
            for error in errors:
                error_pane.insert(constants.END, f"{error}\n")
            error_pane.config(state="disabled")

       
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
        # if tokenlist[i].type=="Whitespace":
        #     continue
        # else:
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

root.geometry("1200x700")
root.resizable(False,False)
root.iconbitmap("source/assets/img/sheesh_logo1.ico")
root.title("Sheesh Compiler")
victor_mono = Font(file = f"source/assets/font/VictorMono-Regular.ttf", family = "Victor Mono")

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
    height=700,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

mainpane.place(x=0,y=0)

header_img_tk = ImageTk.PhotoImage(file = f'source/assets/img/header_img.png')

header_label = ctk.CTkLabel(root, image=header_img_tk, text='')
header_label.pack(side="top", fill="x")


line_numbers = Text(
                root, 
                bd=0, 
                bg=clr_black, 
                fg="#FFFFFF", 
                font=(victor_mono, 12), 
                width=4, 
                wrap="none", 
                state="disabled"
)

line_numbers.place(
                x=10,y=50,
                width=20,
                height=390,
)

# setting editor section
txt_editor_pane = Text(
    bd=0,
    bg="#282822",
    highlightthickness=0,
    fg="#FFFFFF",
    insertbackground="white",
    padx=10,
    pady=10,
    font=(victor_mono, 12,),
) 


txt_editor_pane.place(x=30, y=40, width=870, height=400)
txt_editor_pane.bind("<Tab>", tab_pressed)

lex_table_pane = Text(
    bd=0,
    bg="#323232",
    highlightthickness=0,
    fg="#FFFFFF",
    padx=10,
    pady=10,
    font=('Open Sans', 10),
    state = "disabled",)

lex_table_pane.place(
    x=900,
    y=40,
    width=300,
    height=660)

error_pane = Text(
    bd=0,
    bg="#323232",
    highlightthickness=0,
    fg="red",
    padx=10,
    pady=10,
    font=('Open Sans', 10),
    state = "disabled",)

error_pane.place(x=0,y=440,width=900,height=260)


# run lexer function button
run_lex_img = PhotoImage(file="source/assets/img/run_lex.png") 
run_syn_img = PhotoImage(file="source/assets/img/run_syntax.png") 
load_img=PhotoImage(file="source/assets/img/load.png")

lex_btn = Button(
        image=run_lex_img,
        compound=LEFT,
        bg="#282822",
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        activeforeground="#FFFFFF",
        justify="center",
        command=run_lex,
)

lex_btn.place(x=750,y=40,width=50,height=50)

load_btn=Button(
    image=load_img,
        compound=LEFT,
        bg="#282822",
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        # activeforeground="#FFFFFF",
        justify="center",
        command=load_file,

)

load_btn.place(x=850,y=40,width=50,height=50)


parse_btn = Button(
        image=run_syn_img,
        compound=LEFT,
        bg="#282822",
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        activeforeground="#FFFFFF",
        justify="center",
        command=run_parser,
)
parse_btn.place(x=800,y=40,width=50,height=50)

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
    highlight_reserve_word(*args)
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
