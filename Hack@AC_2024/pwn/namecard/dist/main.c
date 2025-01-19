#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char savedCanary[8];
int initialised = 0;

void initiateCanary(char *canary){
    if(!initialised){
        FILE *fd = fopen("/dev/urandom", "r");
        fread(savedCanary, 1, 8, fd);
        initialised = 1;
    }
    strncpy(canary, savedCanary, 8);
}

int main(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    // idk why it only works when i put canary before all the variables
    char canary[8];
    char namecard[128], name[16], company[32], address[16], format[128];

    initiateCanary(canary);

    // I thought the stack grew down not up??? wtv
    if(canary < format){
        printf("Canary not initialised properly! Contact an admin\n");
        exit(-1);
    }

    printf("Welcome to my namecard printing service!\n");
    printf("Please enter in your name: ");
    fgets(name, 16, stdin);
    printf("Please enter in your company: ");
    fgets(company, 32, stdin);
    printf("Please enter in your address: ");
    fgets(address, 16, stdin);
    printf("Enter in your namecard format (we support format strings): ");
    fgets(format, 128, stdin);

    printf("Generating your namecard...\n");
    sprintf(namecard, format, name, company, address);

    puts(namecard);
    printf("Goodbye!\n");
    if(strncmp(canary, savedCanary, 8)){
        printf("stack smashing detected!!!\n");
        exit(-1);
    }
}