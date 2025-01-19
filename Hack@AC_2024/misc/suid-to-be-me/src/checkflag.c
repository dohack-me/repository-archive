#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* escapeshellarg(char* str) {
    char *escStr;
    int i,
        count = strlen(str),
            ptr_size = count+3;

    escStr = (char *) calloc(ptr_size, sizeof(char));
    if (escStr == NULL) {
        return NULL;
    }
    sprintf(escStr, "'");

    for(i=0; i<count; i++) {
        if (str[i] == '\'') {
                    ptr_size += 3;
            escStr = (char *) realloc(escStr,ptr_size * sizeof(char));
            if (escStr == NULL) {
                return NULL;
            }
            sprintf(escStr, "%s'\\''", escStr);
        } else {
            sprintf(escStr, "%s%c", escStr, str[i]);
        }
    }

    sprintf(escStr, "%s%c", escStr, '\'');
    return escStr;
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
        puts("Please supply your flag!");
        return 1;
    }
    setuid(0);
    setgid(0);
    FILE *fp;
    char hash[65];
    int csize = 17 + strlen(argv[1]) + 1;
    char* command = malloc(csize);
    char* input = escapeshellarg(argv[1]);
    strcat(command, "echo ");
    strcat(command, argv[1]);
    strcat(command, " | sha256sum");
    fp = popen(command, "r");
    fgets(hash, sizeof(hash), fp);
    puts(hash);
    if (strcmp(hash, "44c3f2fba3dda36d4ea270fe407008eac157896b46e0a385c97439753af7cc37") == 0) {
        puts("Congrats! You got the flag!");
    } else {
        puts("Your flag is wrong ;-;");
    }
}
