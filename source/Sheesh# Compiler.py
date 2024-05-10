keywords = ["text", "charr","whole", "dec", "sus", "blank", "sheesh", "yeet", "based",
            "kung", "ehkung", "deins", "when", "bet", "choose","for", "to", 
            "step", "felloff", "pass", "use", "from", "nocap", "cap", "default", "up", "pa_mine", "def", "whilst"]
# import source.helper as helper
import sys
sys.path.append( '.' )
from source.SyntaxAnalyzer.Parser import SyntaxAnalyzer as parser

import customtkinter as ctk
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import constants
from tkinter import ttk
import source.LexicalAnalyzer.Lexer as lex
from source.core.compile import Compiler
# import source.LexicalAnalyzer.prepare as prep
from tkinter import filedialog
import cProfile



def highlight_reserve_word(*args):
    txt_editor_pane.tag_remove('found', '1.0', tk.END)
    txt_editor_pane.tag_remove('reserveidenti', '1.0', tk.END)
    
    text = txt_editor_pane.get('1.0', tk.END)

    in_quotes = False
    for i, char in enumerate(text):
        if char == '"':
            in_quotes = not in_quotes
        elif not in_quotes:
            for word in keywords:
                if text[i:i+len(word)] == word:
                    if i + len(word) == len(text) or not text[i+len(word)].isalnum() and text[i+len(word)] != '_':
                        start_index = f'1.0+{i}c'
                        end_index = f'1.0+{i+len(word)}c'
                        if text[i:i+len(word)].islower():
                            txt_editor_pane.tag_add('found', start_index, end_index)
                        else:
                            txt_editor_pane.tag_add('reserveidenti', start_index, end_index)

    txt_editor_pane.tag_config('found', foreground='yellow')
    txt_editor_pane.tag_config('reserveidenti', foreground='white')


def highlight_comment(*args):
    txt_editor_pane.tag_remove('comment', '1.0', tk.END)
    text = txt_editor_pane.get('1.0', tk.END)
    in_comment = False
    in_line=False
    in_block=False
    for i, char in enumerate(text):
        if char == '/' and len(text) > i+1 and text[i+1] == '/' and not in_comment:
            # in_comment = not in_comment
            in_line=not in_line
            # if len(text) > i+1 and text[i+1] == '\n':
            #     in_comment = not in_comment
        elif char=="/" and len(text) > i+1 and text[i+1] == "*" and not in_comment:
            # in_comment = not in_comment
            in_block=not in_block
            # if char == "*" and len(text) > i+1 and text[i+1] == "/" and in_comment:
            #     in_comment = not in_comment
        # elif in_comment:
        #     start_index = f'1.0+{i-1}c'
        #     end_index = f'1.0+{i}c'
        #     txt_editor_pane.tag_add('comment', start_index, end_index)
            
        elif in_line:
            if char == '\n':
                in_line=not in_line
            start_index = f'1.0+{i-1}c'
            end_index = f'1.0+{i}c'
            txt_editor_pane.tag_add('comment', start_index, end_index)
        
        elif in_block:
            if char=="*" and len(text) > i+1 and text[i+1] == "/" :
                in_block=not in_block
            start_index = f'1.0+{i-1}c'
            end_index = f'1.0+{i+2}c'
            txt_editor_pane.tag_add('comment', start_index, end_index)
    txt_editor_pane.tag_config('comment', foreground='grey')


def on_scroll(*args):
    line_numbers.yview_moveto(*args)
    txt_editor_pane.yview_moveto(*args)
    




def remove_whitespace_type(tokens):
    new_tokens = []
    for token in tokens:
        if token.type != "Whitespace" and token.type != "Block Comment" and token.type != "Inline Comment":
            new_tokens.append(token)
    return new_tokens

def run_lex():
    
    print("Lexical Analysis...")
    code = txt_editor_pane.get("1.0", END)
    compiler=Compiler(code)
    compiler.compile()
    tokens=compiler.lexer.tokens
    error=compiler.lexer.errors
    tokens=remove_eol(tokens)
    if tokens != []:
        tokens=remove_whitespace_type(tokens)
        print_lex(tokens)
        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")
    else:
        tokens=compiler.lexer.no_tokens

    if error !=[]:
        print_lex(tokens)
        print_error(error)
        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")
    else:
        print_lex(tokens)
        print_error(["Nothing to Lexically Analyze. Please input code."])
        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")


def remove_eol(tokens):
    new_tokens = []
    for token in tokens:
        if token.type == 'Newline':
            continue
        new_tokens.append(token)
    return new_tokens

def run_parser():
    
    print("Parsing...")
    code = txt_editor_pane.get("1.0", END)
    compiler=Compiler(code)
    compiler.compile()
    # print_lex(remove_eol(tokens))
    lex_errors=compiler.lex_errors
    syntax_errors=compiler.syntax_errors
    # semantic_errors=compiler.semantic_errors
    output=compiler.output

    if lex_errors:
        error_pane.config(state="normal")
        error_pane.config(foreground= yellow)
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, "Can't Parse, Resolve Lexical Errors:\n")
        for err in lex_errors:
            error_pane.insert(constants.END, f'{err}\n')
    else:
        error_pane.config(state="disabled")

        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)
        if output==[]:
            error_pane.config(foreground= green)
            error_pane.insert(constants.END, "No Output\n")
        else:
            error_pane.config(foreground= green)
            error_pane.insert(constants.END, f'Output:\n')
            for out in output:
                error_pane.insert(constants.END, f"{out}\n")
            # error_pane.config(state="disabled")

        if syntax_errors==[] :
            error_pane.config(foreground= green)
            error_pane.insert(constants.END, "\nNo Syntax Errors\n")
            
        else:
            error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nSyntax Error:\n')
            for error in syntax_errors:
                error_pane.insert(constants.END, f"{error}\n")
            # error_pane.config(state="disabled")


        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")



def run_semantic():

    print("Semantic Analysis...")
    code = txt_editor_pane.get("1.0", END)
    compiler=Compiler(code)
    compiler.compile()
    # print_lex(remove_eol(tokens))
    lex_errors=compiler.lex_errors
    syntax_errors=compiler.syntax_errors
    semantic_errors=compiler.semantic_errors
    output=compiler.output

    if lex_errors:
        error_pane.config(state="normal")
        error_pane.config(foreground= yellow)
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, "Can't Parse, Resolve Lexical Errors:\n")
        for err in lex_errors:
            error_pane.insert(constants.END, f'{err}\n')
    else:
        error_pane.config(state="disabled")

        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)

        if syntax_errors==[] :
            error_pane.config(foreground= green)
            error_pane.insert(constants.END, "\nNo Syntax Errors\n")
            
        else:
            error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nSyntax Error:\n')
            for error in syntax_errors:
                error_pane.insert(constants.END, f"{error}\n")
            # error_pane.config(state="disabled")
    
        if semantic_errors==[]:
            error_pane.config(foreground= green)
            error_pane.insert(constants.END, "\nNo Semantic Errors\n") 
        else:
            error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nSemantic Errors:\n')
            for serr in semantic_errors:
                error_pane.insert(constants.END, f"{serr}\n")
            error_pane.config(state="disabled")

    

        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")

    
def compile():

    
    print("Compiling...")
    code = txt_editor_pane.get("1.0", END)
    compiler=Compiler(code)
    compiler.compile()
    # print_lex(remove_eol(tokens))
    lex_errors=compiler.lex_errors
    syntax_errors=compiler.syntax_errors
    semantic_errors=compiler.semantic_errors
    runtime_errors=compiler.runtime_errors
    output=compiler.output


    error_tag = "error_text"
    normal_tag = "normal_text"
    emphasis= "emphasis_text"

    error_pane.tag_configure(error_tag, foreground="yellow")
    error_pane.tag_configure(normal_tag, foreground="green")
    error_pane.tag_configure(emphasis, foreground=green)

    if lex_errors:
        error_pane.config(state="normal")
        # error_pane.config(foreground= yellow)
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, "Can't Parse, Resolve Lexical Errors:\n", error_tag)
        for err in lex_errors:
            error_pane.insert(constants.END, f'{err}\n', error_tag)
    else:
        error_pane.config(state="disabled")

        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)


        if runtime_errors==[]:

            if output==[]:
                # error_pane.config(foreground= yellow)
                error_pane.insert(constants.END, "No Output\n", normal_tag)
            else:
                # error_pane.config(foreground= green)
                error_pane.insert(constants.END, f'Output:\n', emphasis)
                for out in output:
                    repeat=output[out]
                    for i in range(repeat):
                        error_pane.insert(constants.END, f"{out}\n", emphasis)
                # error_pane.config(state="disabled")
        else:
            # error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nRuntime Error:\n', error_tag)
            for rerr in runtime_errors:
                error_pane.insert(constants.END, f"{rerr}\n", error_tag)
            error_pane.config(state="disabled")

        if syntax_errors==[] :
            # error_pane.config(foreground= green)
            error_pane.insert(constants.END, "\nNo Syntax Errors\n", normal_tag)
            
        else:
            # error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nSyntax Error:\n', error_tag)
            for error in syntax_errors:
                error_pane.insert(constants.END, f"{error}\n", error_tag)
            # error_pane.config(state="disabled")
    
        if semantic_errors==[]:
            # error_pane.config(foreground= green)
            error_pane.insert(constants.END, "\nNo Semantic Errors\n", normal_tag) 
        else:
            # error_pane.config(foreground= yellow)
            error_pane.insert(constants.END, f'\nSemantic Errors:\n', error_tag)
            for serr in semantic_errors:
                error_pane.insert(constants.END, f"{serr}\n", error_tag)
            error_pane.config(state="disabled")

    

        lex_table_pane.config(state="disabled")
        error_pane.config(state="disabled")

def print_lex(tokenlist):                      # Print Text to Lexical Pane
    print("Printing lex...")
    lex_table_pane.config(state="normal")
    lex_table_pane.delete('1.0', constants.END)
    lex_table_pane.insert(constants.END, "LEXEME\t\t\tTOKEN\n\n")
    for i in range(len(tokenlist)):
            lex_table_pane.insert(
                constants.END, f'{str(tokenlist[i].value) if len(str(tokenlist[i].value))<=15 else str(tokenlist[i].value)[:10] + "..."}\t\t\t{str(tokenlist[i].type)}\n')


def print_error(error):
    if error==[]:
        error_pane.config(state="normal")
        error_pane.config(foreground= green)
        error_pane.delete('1.0', constants.END)
        error_pane.insert(constants.END, "No Lexical Errors")
    else:
        error_pane.config(state="normal")
        error_pane.delete('1.0', constants.END)
        error_pane.config(foreground= yellow)
        error_pane.insert(constants.END, "Lexical Errors:\n")
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
def multiple_yview(*args):
    line_numbers.yview(*args)
    txt_editor_pane.yview(*args)

def multiple_yview_scroll(*args):
    line_numbers.yview_scroll(int(-1*(args[0].delta/120)), "units")
    txt_editor_pane.yview_scroll(int(-1*(args[0].delta/120)), "units")




root = Tk()

root.geometry("1200x700")
root.resizable(False,False)
root.iconbitmap("source/assets/sheesh_logo1.ico")
root.title("Sheesh Compiler")

# config color collection
yellow="#FFF700"
green="#1BFC06"
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
    relief="ridge")

mainpane.place(x=0,y=0)

# header_img_tk = ImageTk.PhotoImage(file = f'source/assets/header_img.png')
header_img_tk = ctk.CTkImage(Image.open(f'source/assets/header_img.png'),size=(1200, 40))
header_label = ctk.CTkLabel(root, image=header_img_tk, text='')
header_label.pack(side="top", fill="x")




# setting editor section
txt_editor_pane = Text(
    bd=0,
    bg="#282822",
    highlightthickness=0,
    fg="#FFFFFF",
    insertbackground="white",
    padx=10,
    pady=10,
    font=('Open Sans', 12,),) 


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
    fg=yellow,
    padx=10,
    pady=10,
    font=('Open Sans', 10),
    state = "disabled",)

error_pane.place(x=0,y=440,width=900,height=260)

# input_pane=tk.StringVar()
# user_input_entry=tk.Entry(error_pane, textvariable=input_pane, width=50)
# user_input_entry.pack()




# run lexer function button
run_lex_img = PhotoImage(file="source/assets/run_lex.png") 
run_syn_img = PhotoImage(file="source/assets/run_syntax.png") 
load_img=PhotoImage(file="source/assets/load.png")
run_sem_img=PhotoImage(file="source/assets/run.png")

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
parse_btn.place(x=700,y=40,width=50,height=50)

semantic_btn = Button(
        image=run_sem_img,
        compound=LEFT,
        bg="#282822",
        borderwidth=0,
        highlightthickness=0,
        activebackground="#AAAAAA",
        fg="#079AD2",
        activeforeground="#FFFFFF",
        justify="center",
        command=compile,
)
semantic_btn.place(x=800,y=40,width=50,height=50)
line_numbers = Text(bd=0, bg=clr_black, fg="#FFFFFF", font=('Open Sans', 12), width=4, wrap="none", state="disabled")
line_numbers.place(x=5,y=50,width=20,height=390)
scrollbar = ttk.Scrollbar(
    txt_editor_pane,
    orient='vertical',
    command=multiple_yview,
)
scrollbar.pack(side=RIGHT, fill=Y)

line_numbers.configure(yscrollcommand=scrollbar.set)
txt_editor_pane.configure(yscrollcommand=scrollbar.set)
# txt_editor_pane['yscrollcommand'] = scrollbar.set


def update_line_numbers(*args):
    highlight_reserve_word(*args)
    highlight_comment(*args)
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    lines = txt_editor_pane.get("1.0", "end").count("\n")
    line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, lines + 1)))
    line_numbers.config(state="disabled")

def update_line_numbers_on_scroll(*args):
    update_line_numbers()
    on_scroll(*args)



txt_editor_pane.bind("<KeyRelease>", update_line_numbers)
txt_editor_pane.bind_all("<MouseWheel>", multiple_yview_scroll)

root.mainloop()
