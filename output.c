
                    #include <stdio.h>
                    #include<stdlib.h>
                    #include<string.h>
                    #include<stdbool.h>
                    #include <stdarg.h>
                    
           
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
                    int main ( ) {
printf ( "Enter number: " ) ;
int shs_input;scanf("%d", &shs_input);int shs_num1=0 ;
printf ( "%d " , shs_num1 ) ;
int shs_num2=1 ;
printf ( "%d " , shs_num2 ) ;
int shs_num3=shs_num1 + shs_num2 ;
printf ( "%d " , shs_num3 ) ;
for ( int shs_k=0 ; shs_k!=shs_input ;shs_k+=1 ){
shs_num1=shs_num2 ;
shs_num2=shs_num3 ;
shs_num3=shs_num1 + shs_num2 ;
printf ( " %d " , shs_num3 ) ;
}
}

