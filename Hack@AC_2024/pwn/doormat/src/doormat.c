#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

struct house {
  char *doormat;
  char *art;
};

struct house *houses[3];

char letters[3][8];

void setup() {
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);

  for (int i = 0; i < 3; i++) {
    houses[i] = malloc(0x20);
  }

  houses[0]->doormat = "House of Prime";
  houses[0]->art = "  _m_   \n"
                   "/\\___\\\n"
                   "|_|\"\"|\n";

  houses[1]->doormat = "House of Mind";
  houses[1]->art = " _____\n"
                   "| \" \" |--\n"
                   "| \" \" |\" \\\n"
                   "[  -  ]  |\n";

  houses[2]->doormat = "House of Force";
  houses[2]->art = "     ~~\n"
                   "   ~\n"
                   " _u__\n"
                   "/____\\\n"
                   "|[][]|\n"
                   "|[]..|\n"
                   "'--'''\n";
}

void view_house() {
  char buf[32];
  int idx;
  printf("Index: ");
  fgets(buf, 32, stdin);
  idx = atoi(buf);
  printf("%s", houses[idx]->art);
  printf("Letter: %s\n", letters[idx]);
  printf("(stop reading other ppl's letters...)\n");
}

void leave_letter() {
  char buf[32];
  int idx;
  printf("Index: ");
  fgets(buf, 32, stdin);
  idx = atoi(buf);

  fgets(letters[idx], 8, stdin);
  printf("\nLetter sent to %p.\n", letters[idx]);
}

void leave() {
  printf("Goodbye!\n");
  exit(0);
}

void menu() {
  char buf[32];
  int choice;

  printf("-----------\n");
  printf("1. View house\n");
  printf("2. Leave letter\n");
  printf("3. Leave\n");
  printf("> ");

  fgets(buf, 32, stdin);
  choice = atoi(buf);

  switch (choice) {
  case 1:
    view_house();
    break;
  case 2:
    leave_letter();
    break;
  case 3:
    leave();
    break;
  default:
    printf("Invalid choice\n");
    break;
  }
}

int main() {
  setup();
  while (1) {
    menu();
  }
}
