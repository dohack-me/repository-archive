#include <stdio.h>
#include <stdbool.h>
#include <signal.h>

void timeout(int signum) {
    printf("Timeout!");
    exit(-1);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}


int main() {
    setup();
    char buf[128];
    while (true){
        puts("Eat");
        puts("Sleep");
        gets(buf);
        printf(buf);
    }
}
