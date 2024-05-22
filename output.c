
                    #include <stdio.h>
                    #include<stdlib.h>
                    #include<string.h>
                    #include<stdbool.h>
                    #include <stdarg.h>
                    
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
                        result[0] = '\0'; // initialize to empty string

                        va_start(args, count);
                        for(i = 0; i < count; i++) {
                            char *str = va_arg(args, char*);
                            strcat(result, str);
                        }
                        va_end(args);

                        return result;
                    }
                    
                    
                    char* bool_to_string(int boolean){
                        return (boolean == 1) ? "nocap": "cap";
                    }
                     int shs_add_two_numbers ( int shs_x , int shs_y ) {
return shs_x + shs_y ;
}
int main ( ) {
printf ( "Conditions\n==========\n" ) ;
if ( 1 == 0 ) {
printf ( "KUNG reached!\n" ) ;
}
else {
printf ( "KUNG reached!\n" ) ;
}
int shs_var=0 ;
switch ( shs_var ) {
case 0 : printf ( "correct choose!\n" ) ;
break ;
case 1 : printf ( "incorrect choose!\n" ) ;
break ;
}
printf ( "==========\n" ) ;
printf ( "Loops\n==========\n" ) ;
int shs_ctr=0 ;
do {
printf ( "ctr %d\n" , shs_ctr + 1 ) ;
shs_ctr += 1 ;
}
while ( shs_ctr < 5 ) ;
for ( int shs_i=0 ; shs_i!=5 ;shs_i+=1 ){
printf ( "*" ) ;
}
printf ( "\n==========\n" ) ;
printf ( "Function: %d\n" , shs_add_two_numbers ( 1 , 2 ) ) ;
}
