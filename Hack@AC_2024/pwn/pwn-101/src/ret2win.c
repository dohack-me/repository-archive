#include <stdio.h>
#include <stdlib.h>

void setup() {
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
}

void win() {
  system("/bin/sh");
}

int main() {
  char buf[0x10];

  setup();

  printf("1. ");
  gets(buf);

  return 0;
}
