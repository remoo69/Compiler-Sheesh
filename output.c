
                    #include <stdio.h>
                    #include<stdlib.h>
                    #include<string.h>
                    #include<stdbool.h>
                    #include <stdarg.h>
                    
           
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
                        result[total_length] = '\0';

                        return result;
                    }
                    
                    char* bool_to_string(int boolean){
                        return (boolean == 1) ? "nocap": "cap";
                    }
                     void shs_print_avg ( int shs_avg ) {
printf ( "%d" , shs_avg) ;
}
 void shs_get_avg_seq ( int shs_size , int shs_w_seq [ ] ) {
printf ( "\nEntered Sequence: \n" ) ;
int shs_sum=0 ;
for ( int shs_k=0 ; shs_k<shs_size ;shs_k+=1 ){
printf ( "%d " , shs_w_seq[ shs_k] ) ;
shs_sum += shs_w_seq [ shs_k ] ;
}
shs_print_avg ( shs_sum / shs_size ) ;
}
int main ( ) {
printf ( "Enter n: " ) ;
int shs_n;scanf("%d", &shs_n);int shs_seq [ shs_n ] ;
for ( int shs_i=0 ; shs_i<shs_n ;shs_i+=1 ){
printf ( "Enter value %d: " , shs_i+ 1 ) ;
int shs_temp;scanf("%d", &shs_temp);shs_seq [ shs_i ] = shs_temp ;
}
shs_get_avg_seq ( shs_n , shs_seq ) ;
}
