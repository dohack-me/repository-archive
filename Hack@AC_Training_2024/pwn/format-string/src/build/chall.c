#include <stdio.h>
#include <stdlib.h>

struct stack {
  char buffer[128];
  int target;
};

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
}

void win() {
  system("/bin/sh");
}

int main() {
  struct stack s;
  s.target = 0x1337;

  setup();

  puts("Welcome to the challenge!");
  printf("Your goal is to overwrite the value of the target variable at %p (current value is %p)\n", &s.target, s.target);
  printf("Its value should be %p\n", 0xdeadbeef);

  printf("Input > ");
  fgets(s.buffer, sizeof(s.buffer) - 1, stdin);

  printf("You entered: ");
  printf(s.buffer);

  printf("The value of the variable is now %p\n", s.target);

  if (s.target == 0xdeadbeef) {
    win();
  } else {
    puts("Try again!");
  }
  return 0;
}
