#include <stdio.h>

int main(int argc, char *argv[]){

    if(argc == 3){
        printf("The number of argumnts are exact. (arg-0, arg-1, arg-2) = (string, string, int)\n ");

    }else if(argc < 3){
        printf("Less number of arguments");
    }else{
        printf("too many arguments");
    }

    file *fptr;
    fptr = fopen("filename.txt", "r"); // "w+"
    fscanf(fptr, "%s %s %s %d", str1, str2, str3, &year);
    fscanf(read_string, num_of_bytes, 1, fptr );
    



}