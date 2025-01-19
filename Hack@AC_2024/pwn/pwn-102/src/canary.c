#include <stdio.h>
#include <unistd.h>
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
  char buf[0x18];

  setup();

  printf("1. ");
  read(0, buf, 0x100);
  puts(buf);
  printf("2. ");
  read(0, buf, 0x100);

  return 0;
}
