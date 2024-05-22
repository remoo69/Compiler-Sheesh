import sys
sys.path.append(".")
from source.core.AST import AST
from source.core.symbol_table import SymbolTable, Token
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
            
            "for":"for",
            # "to":"; {id}<=",
            # "step":";{id}++{step}",
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
        
        self.errors=["test"]
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
                return f", {next} )"
            else:
                return f", {next}"
            
        
        
        
        
    # def to_(self, remaining):
    #     final=""
    #     while remaining[0].value!=")":
    #         if remaining [0].value=="to":
    #             final+="; {}"
    #             remaining=remaining[1:]
    #         else:
    #             final+=remaining[0].value+" "
    #             remaining=remaining[1:]
    #         final+=remaining[0].value+" "
    #         remaining=remaining[1:]
        
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
                        int total_length = 0; // Start with 0 length

                        va_start(args, str1);

                        // Iterate through arguments to calculate total length
                        char *current_str = (char *)str1;
                        while (current_str != NULL) {
                            total_length += strlen(current_str) + 1; // Add string length + null terminator
                            current_str = va_arg(args, char *);
                        }

                        va_end(args);

                        if (total_length > 0) { // Allocate memory if there are strings
                            result = malloc(total_length * sizeof(char));
                            if (result == NULL) {
                                return NULL; // Handle memory allocation failure
                            }
                        }

                        // Concatenate strings into the result
                        va_start(args, str1);
                        current_str = (char *)str1;
                        int current_pos = 0;
                        while (current_str != NULL) {
                            strcpy(result + current_pos, current_str);
                            current_pos += strlen(current_str) + 1; // Update position after copying and null terminator
                            current_str = va_arg(args, char *);
                        }

                        va_end(args);

                        return result;
                    }
                    
                    char* bool_to_string(int boolean){
                        return (boolean == 1) ? "nocap": "cap";
                    }
                    """)
        self.translate(self.tree)
        f.close()
        # return self.errors
    
    # def translate(self, node):
    #     """ 
    #     Traverse the tree in a depth-first manners
    
    #     """
    #     with open("output.c", "a") as f:
    #         if node.children:
    #             for child in node.children:
    #                 if isinstance(child, AST):  # Check if the child is an AST
    #                     if child.root in self.other_translations:
    #                         self.other_translations[child.root](child, f)
    #                     else:
    #                          self.translate(child)
    #                 if isinstance(child, Token):
    #                     token_value = child.value 
    #                     translated_value = self.sheesh_to_c.get(token_value, token_value)
    #                     f.write(translated_value + ' ')
    
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
                    # if leaves[i].value=="text":
                    #     f.write("char"+" ")

                    #     if leaves[i+1].type=="Identifier":
                    #         nearest_id="shs_"+leaves[i].value
                    #         f.write("shs_"+leaves[i].value+"[]")
                    #         self.appended.append("shs_"+leaves[i].value+"[]")
                    #         i+=1
                    elif leaves[i].value=="up":
                        in_print=True
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        
                    elif leaves[i].value=="charr":
                        f.write(self.sheesh_to_c[leaves[i].value]+" ")
                        i+=1
                    elif leaves[i].type=="Sus" and in_print:
                        f.write("bool_to_string("+nearest_id+")")
                        self.appended.append("bool_to_string("+leaves[i].value+")")
                        
                    elif leaves[i].value=="to":
                        in_for=True
                        found_to=True
                        f.write("; "+nearest_id+"!=")
                        self.appended.append("; "+nearest_id+"<=")
                        i+=1
                        j=0
                        while leaves[i+j].value !="step":
                            if leaves[i+j].value==")" and leaves[i+j+1].value=="{":
                                f.write(";"+ nearest_id+"+=1 )")
                                self.appended.append(";"+ nearest_id+"+=1 )")
                                j+=1
                                break
                            else:
                                f.write(leaves[i+j].value+" ")
                                self.appended.append(leaves[i+j].value+" ")
                            j+=1
                        i+=j-1
                        
                    elif leaves[i].value=="step":
                        f.write(";"+nearest_id+"+=")
                        self.appended.append(";"+nearest_id+"+=")
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
                        except KeyError as e:
                                e=str(e)[1:-1]
                                self.semantic.semantic_error(error=e, token=leaves[i], expected=se.expected[e])
                                
                        nearest_id="shs_"+leaves[i].value
                        if leaves[i+1].value=="=":
                            if leaves[i+2].value=="pa_mine":
                                if leaves[i-1].value in ["whole", "dec", "text", "sus", "charr"]:
                                    f.write(nearest_id +";")
                                    
                                fs=leaves[i+4].value
                                f.write(f"scanf("+self.text_handle(fs)+", &"+nearest_id+");")
                                self.appended.append("scanf(\"%d\"," +"&"+nearest_id+");")
                                i+=6
                            else:
                                f.write("shs_"+leaves[i].value+"=")
                                self.appended.append("shs_"+leaves[i].value+"=")
                                nearest_id="shs_"+leaves[i].value
                                i+=1 
                        elif leaves[i+1].value=="...":
                            f.write(self.concat(i, leaves))
                            self.appended.append(self.concat(i, leaves))
                            i+=3
                        elif val.type=="sus" and in_print:
                                    f.write("bool_to_string("+nearest_id+")")
                                    self.appended.append("bool_to_string("+leaves[i].value+")")
                            
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
            # If the node has no children or no AST children, go up the tree to find the next sibling
            # while node.parent:
            #     sibling_index = node.parent.children.index(node) + 1
            #     if sibling_index < len(node.parent.children):
            #         for sibling in node.parent.children[sibling_index:]:
            #             if isinstance(sibling, AST):  # Check if the sibling is an AST
            #                 return sibling
            #     node = node.parent
            # # If we've reached the root and there are no more siblings, the tree has been fully traversed
            # return None
      
    
    
    # def translate(self):

    #     if not hasattr(self, 'sheesh_to_c'):
    #         raise Exception("Translation dictionary 'sheesh_to_c' not found")

    #     try:
    #         with open("output.c", "w") as f:
    #             for node in self.traverse(self.tree):
    #                 if node is not None:
    #                     if hasattr(node, 'root'):
    #                         token_value = node.root
    #                         translated_value = self.sheesh_to_c.get(token_value, token_value)
    #                         f.write(translated_value + ' ')
    #                     else:
    #                         raise Exception(f"Node {node} does not have a 'root' attribute")
    #     except IOError:
    #         raise Exception("Could not open 'output.c' for writing")
    
    
    
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