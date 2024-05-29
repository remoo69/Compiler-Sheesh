import sys
sys.path.append(".")
from source.core.AST import AST
from source.core.symbol_table import SymbolTable, Token, Variable
from source.SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from source.core.error_types import Semantic_Errors as se



class Translator:
    def __init__(self, tree:AST,semantic:SemanticAnalyzer, debugMode) -> None:
        self.tree=tree
        self.semantic=semantic
        self.symbol_table=semantic.all_symbols()
        self.sheesh_to_c={
            
            "charr":"char",
            "whole":"int", 
            "dec":"float", 
            "sus":"bool", 
            "blank":"void", 
            "sheesh":"int main", 
            "yeet":"return", 
            "based":"const",
            "kung":"if", 
            "ehkung":"else if", 
            "deins":"else", 
            "when":"case", 
            "bet":"do", 
            "choose":"switch",
            "def":"", #NOTE - ewan
            "felloff":"break", 
            "pass":"continue", 
            
            "nocap":"true", 
            "cap":"false", 
            
            "default":"default", 
            "up":"printf", 
            "pa_mine":"scanf",   
            
            "whilst":"while",
            "#":";",
            "::": ":",
            "&":"&&",
            "|":"||",
            
            "for":"for",
    
            "text":"char *",
            }
        
        self.handling={
            # "text":self.text, 
            # "def":None, 
            # "to":self.to, 
            # "to":None, 
            # "step":None, 
            # "...":self.concat,
        }
        
        self.errors=[]
        self.other_translations={}
        self.appended=[]
        self.in_concat=False
        
    def concat(self, index, all):
        prev=all[index]
        next=all[index+2]
        
        if self.in_concat==False:    
            if prev.type=="Identifier":
                prev="shs_"+prev.value
            else:
                prev=self.text_handle(prev.value)
                
            if next.type=="Identifier":
                next="shs_"+next.value
            else:
                next=self.text_handle(next.value)
                
            self.in_concat=True
            return f"concat({prev}, {next}"
          
        elif self.in_concat ==True:
                
            if next.type=="Identifier":
                next="shs_"+next.value
            else:
                next=self.text_handle(next.value)
                
            
              
            if all[index+3].value in ["#", ")"] and self.in_concat==True:
                self.in_concat=False
                return f", {next}, NULL );"
            else:
                return f", {next}"
            
        
    def generate(self):
        with open("output.c", "w") as f:
            f.write("""
                    #include <stdio.h>
                    #include<stdlib.h>
                    #include<string.h>
                    #include<stdbool.h>
                    #include <stdarg.h>
                    """)
            f.write("""
           
                    char *concat(const char *str1, ...) {
                        va_list args;
                        char *result = NULL;
                        int total_length = 0;

                        va_start(args, str1);

                        // First pass: Calculate total length of the resulting string
                        const char *current_str = str1;
                        while (current_str != NULL) {
                            total_length += strlen(current_str);
                            current_str = va_arg(args, const char *);
                        }

                        va_end(args);

                        if (total_length > 0) {
                            // Allocate memory for the resulting string plus the final null terminator
                            result = malloc((total_length + 1) * sizeof(char));
                            if (result == NULL) {
                                return NULL; // Handle memory allocation failure
                            }
                        } else {
                            return NULL; // No valid input strings
                        }

                        // Second pass: Concatenate the strings
                        va_start(args, str1);
                        current_str = str1;
                        int current_pos = 0;
                        while (current_str != NULL) {
                            strcpy(result + current_pos, current_str);
                            current_pos += strlen(current_str);
                            current_str = va_arg(args, const char *);
                        }

                        va_end(args);

                        // Ensure the final string is null-terminated
                        result[total_length] = '\\0';

                        return result;
                    }
                    
                    char* bool_to_string(int boolean){
                        return (boolean == 1) ? "nocap": "cap";
                    }
                    """)
        self.translate(self.tree)
        f.close()

    
    def translate(self, node):
        """ 
        Traverse the tree in a depth-first manners
    
        """
        leaves=self.tree.leaves()
        with open("output.c", "a") as f:
            found_to=False
            in_for=False
            in_print=False
            if node.children:
                i=0
                while i<len(leaves):
                    

                    if leaves[i].value =="#":
                        f.write(self.sheesh_to_c[leaves[i].value]+"\n")
                        self.appended.append(self.sheesh_to_c[leaves[i].value]+"\n")
                    elif leaves[i].value=="up":
                        in_print=True
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        
                    elif leaves[i].value=="charr":
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        i+=1
                    elif leaves[i].type=="Sus" and in_print:
                        if(leaves[i].value == "nocap"):
                            f.write("bool_to_string("+"true"+")")
                            self.appended.append("bool_to_string("+"true"+")")
                        else:
                            f.write("bool_to_string("+"false"+")")
                            self.appended.append("bool_to_string("+"false"+")")

                    elif leaves[i].value == 'for': #changed no.3
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        self.appended.append(self.sheesh_to_c[leaves[i].value]+" ")
                        id_for = "shs_"+leaves[i+3].value
                    elif leaves[i].value=="to":
                        in_for=True
                        found_to=True
                        ctr = i
                        for_relop = '<'
                        while True:
                            if leaves[ctr].value == ')' and leaves[ctr+1].value == '{':
                                break
                            elif leaves[ctr].value == 'step':
                                if int(eval(leaves[ctr + 1].value)) < 0:
                                    for_relop = '>'
                                    break
                            ctr += 1

                        f.write("; "+id_for+for_relop) 
                        self.appended.append("; "+id_for+for_relop)
                        i+=1
                        j=0
                        while leaves[i+j].value !="step":
                            if leaves[i+j].value==")" and leaves[i+j+1].value=="{":
                                f.write(";"+ id_for+"+=1 )")
                                self.appended.append(";"+ id_for+"+=1 )")
                                j+=1
                                break
                            else:
                                if leaves[i+j].type=="Identifier":
                                    f.write("shs_"+leaves[i+j].value+" ")
                                    self.appended.append(leaves[i+j].value+" ")
                                else:
                                    f.write(leaves[i+j].value+" ")
                                    self.appended.append(leaves[i+j].value+" ")
                                
                            j+=1
                        i+=j-1
                        
                    elif leaves[i].value=="step":
                        f.write(";"+id_for+"+=") # change no.4
                        self.appended.append(";"+id_for+"+=")
                    elif leaves[i].value in ["{", "}"]:
                        f.write(leaves[i].value+"\n")
                        self.appended.append(leaves[i].value+"\n")
                    elif leaves[i].value in self.sheesh_to_c:
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        self.appended.append(self.sheesh_to_c[leaves[i].value]+" ")
                    elif leaves[i].value==")" and in_print and not self.in_concat:
                        in_print=False
                        f.write(leaves[i].value+" ")
                        self.appended.append(leaves[i].value+" ")
                    elif leaves[i].type=="Identifier":
                        try:
                            val=self.symbol_table.find(leaves[i].value)
                            pass
                        except KeyError as e:
                                e=str(e)[1:-1]
                                self.semantic.semantic_error(error=e, token=leaves[i], expected=se.expected[e])
                                
                        nearest_id="shs_"+leaves[i].value
                        if leaves[i+1].value=="=":
                            if leaves[i+2].value=="pa_mine":
                                if leaves[i-1].value in ["whole", "dec", "text", "sus", "charr"]:
                                    if leaves[i-1].value=="text" and leaves[i-2].value != 'charr': # change no.1
                                        f.write(nearest_id+'= (char *)malloc(100 * sizeof(char))' +";")
                                        self.appended.append(nearest_id +";")
                                        fs=leaves[i+4].value
                                        f.write(f"scanf("+self.text_handle(fs)+", "+nearest_id+");")
                                        self.appended.append("scanf(\"%d\"," +""+nearest_id+");")
                                        i+=6
                                    else:
                                        f.write(nearest_id +";")
                                        self.appended.append(nearest_id +";")   
                                        fs=leaves[i+4].value
                                        f.write(f"scanf("+self.text_handle(fs)+", &"+nearest_id+");")
                                        self.appended.append("scanf(\"%d\"," +"&"+nearest_id+");")
                                        i+=6
                                    
                                else:
                                    fs=leaves[i+4].value
                                    f.write(f"scanf({self.text_handle(fs)}, &{nearest_id});")
                                    i+=6
                            else:
                                if leaves[i-1].value=="text" and leaves[i-2].value !="charr": 
                                    f.write(nearest_id +"=")
                                    self.appended.append(nearest_id +"")
                                else:
                                    f.write("shs_"+leaves[i].value+"=")
                                    self.appended.append("shs_"+leaves[i].value+"=")
                                    nearest_id="shs_"+leaves[i].value
                                i+=1 
                        elif leaves[i+1].value=="...":
                            f.write(self.concat(i, leaves))
                            self.appended.append(self.concat(i, leaves))
                            i+=3
                        elif isinstance(val, Variable)  and in_print:
                                if val.type=="sus":
                                    ctr_i = i
                                    if(leaves[i+1].value == "["):
                                        f.write("bool_to_string("+nearest_id)
                                        self.appended.append("bool_to_string("+nearest_id)
                                        ctr_i += 1
                                        while(leaves[ctr_i].value != "]" and leaves[ctr_i+1].value != "["):
                                            print(leaves[ctr_i].value)
                                            if(leaves[ctr_i].type == "Identifier"):
                                                f.write("shs_" + leaves[ctr_i].value)
                                                self.appended.append("shs_" + leaves[ctr_i].value)
                                                ctr_i += 1
                                            else:
                                                f.write(leaves[ctr_i].value)
                                                self.appended.append(leaves[ctr_i].value)
                                                ctr_i += 1
                                        i = ctr_i
                                        f.write("])")
                                        self.appended.append("])")
                                    else:
                                        f.write("bool_to_string("+nearest_id+")")
                                        self.appended.append("bool_to_string("+leaves[i].value+")")
                                # elif val.type=="text":
                                #     f.write("&"+nearest_id)
                                #     self.appended.append("&" + nearest_id)
                                else:
                                    f.write(nearest_id)
                            
                        else:
                            f.write("shs_"+leaves[i].value+" ") 
                            self.appended.append("shs_"+leaves[i].value+" ")  
                                      
                    elif leaves[i].type=="Text":
                        
                        if leaves[i+1].value=="...":
                            f.write(self.concat(i, leaves))
                            self.appended.append(self.concat(i, leaves))
                            i+=3
                        elif leaves[i+1].value in ["#", ")"] and self.in_concat:
                            f.write(self.concat(i-2, leaves))
                            self.appended.append(self.concat(i, leaves))
                            
                        else:
                            f.write(self.text_handle(leaves[i].value)+" ")
                            self.appended.append(self.text_handle(leaves[i].value)+" ")
                    else:
                        f.write(leaves[i].value+" ")
                        self.appended.append(leaves[i].value+" ")
                    i+=1

    def text_handle(self, text):
        format_spec={
            "$w":r"%d",
            "$d":r"%f",
            "$t":r"%s",
            "$c":r"%c",
            "$s":r"%s", #NOTE - idk
        }
        
        for spec, replacement in format_spec.items():
            text = text.replace(spec, replacement)
    
        return text
    
    """  
    
             char* concat(int count, ...) {
                        va_list args;
                        int len = 1; // for null terminator
                        int i;

                        va_start(args, count);
                        for(i = 0; i < count; i++) {
                            char *str = va_arg(args, char*);
                            len += strlen(str);
                        }
                        va_end(args);

                        char* result = malloc(len);
                        result[0] = '\\0'; // initialize to empty string

                        va_start(args, count);
                        for(i = 0; i < count; i++) {
                            char *str = va_arg(args, char*);
                            strcat(result, str);
                        }
                        va_end(args);

                        return result;
                    }
    """
    
if __name__=="__main__":
    i=0
    i+=-2 
    pass
    # tree=AST("sheesh")
    # tree.add_child(AST("whole"))
    # tree.add_child(AST("shs"))
    # tree.add_child(AST("blank