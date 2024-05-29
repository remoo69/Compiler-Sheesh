
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
                     int shs_compareStrings ( char * shs_role , char * shs_requiredRole ) {
int shs_i=0 ;
do {
if ( shs_role [ shs_i ] != shs_requiredRole [ shs_i ] ) {
return (-1) ;
}
shs_i += 1 ;
}
while ( shs_role [ shs_i ] == '\0' || shs_requiredRole [ shs_i ] == '\0' ) ;
if ( shs_role [ shs_i ] == '\0' && shs_requiredRole [ shs_i ] == '\0' ) {
return (-1) ;
}
return 0 ;
}
int main ( ) {
int shs_performanceScore , shs_yearsOfService ;
printf ( "Enter your performance score: " ) ;
scanf("%d", &shs_performanceScore);printf ( "Enter your years of service: " ) ;
scanf("%d", &shs_yearsOfService);printf ( "Enter your role: " ) ;
char * shs_lcl_role= (char *)malloc(100 * sizeof(char));scanf("%s", shs_lcl_role);if ( shs_performanceScore >= 80 && shs_yearsOfService >= 5 && shs_compareStrings ( shs_lcl_role , "Manager" ) == 0 ) {
printf ( "Congratulations! You are eligible for a promotion.\n" ) ;
}
else {
printf ( "Sorry, you are not eligible for a promotion based on the current criteria.\n" ) ;
}
return 0 ;
}
