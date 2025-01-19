#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
}

void menu() {
  puts("1. Create");
  puts("3. Read");
  puts("3. Update");
  puts("4. Delete");
}

size_t SIZE = 0x20;
size_t target = 0x1337;

void *chunks[0x10] = {};

void alloc() {
  int index;
  printf("Index: ");
  scanf("%d", &index);
  if (chunks[index] != NULL) {
    puts("Chunk already allocated");
    return;
  }
  chunks[index] = malloc(SIZE - 0x10);
  printf("Data: ");
  read(0, chunks[index], SIZE - 0x10);
}

void view() {
  int index;
  printf("Index: ");
  scanf("%d", &index);
  if (chunks[index] == NULL) {
    puts("Chunk not allocated");
    return;
  }
  printf("Data: %s\n", chunks[index]);
}

void edit() {
  int index;
  printf("Index: ");
  scanf("%d", &index);
  if (chunks[index] == NULL) {
    puts("Chunk not allocated");
    return;
  }
  printf("Data: ");
  read(0, chunks[index], SIZE - 0x10);
}

void delete() {
  int index;
  printf("Index: ");
  scanf("%d", &index);
  if (chunks[index] == NULL) {
    puts("Chunk not allocated");
    return;
  }
  free(chunks[index]);
}

int main() {
  int choice;

  setup();

  puts("Welcome to the challenge!");
  printf("Your goal is to overwrite the value of %p to 0xdeadbeef (current "
         "value is %p)",
         &target, target);

  while (1) {
    menu();
    printf("> ");
    scanf("%d", &choice);
    switch (choice) {
    case 1:
      alloc();
      break;
    case 2:
      view();
      break;
    case 3:
      edit();
      break;
    case 4:
      delete();
      break;
    default:
      puts("Invalid choice");
      break;
    }
    if (target == 0xdeadbeef) {
      system("/bin/sh");
    }
  }
}
