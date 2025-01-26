#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct item {
  long long price;
  char name[0x30];
};

struct cart {
  struct item **items;
};

struct info {
  int edits;
  int wallet;
  char name[0x50];
};

struct item items[] = {
    {.price = 1, .name = "USB drive"},
    {.price = 2, .name = "Room temp. semiconductor"},
    {.price = 3, .name = "Apple"},
};

struct cart cart;

struct info info = {
    .edits = 1,
    .name = "",
    .wallet = 100,
};

void setup() {
  cart = (struct cart){.items = calloc(10, 8)};
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void menu() {
  printf("\nBalance: $%d\n", info.wallet);
  printf("1. Add item to cart\n");
  printf("2. View cart\n");
  printf("3. Buy items in cart\n");
  printf("4. Set name\n");
  printf("Select an option: ");
}

void add_item() {
  char buf[0x20];
  int idx;
  int i;

  printf("\nItems:\n");

  for (i = 0; i < 3; i++) {
    printf("%d: %s ($%lld)\n", i, items[i].name, items[i].price);
  }

  printf("Select an item: ");
  fgets(buf, sizeof(buf), stdin);
  idx = atoi(buf);

  for (i = 0; i < 10; i++) {
    if (cart.items[i] == 0) {
      cart.items[i] = malloc(sizeof(struct item));
      memcpy(cart.items[i], &items[idx], sizeof(struct item));
      break;
    }
    if (i == 9) {
      printf("Cart is full\n");
    }
  }
}

void view_cart() {
  int i;
  printf("\nYour cart:\n");
  for (i = 0; i < 10; i++) {
    if (cart.items[i] == 0) {
      printf("%d: <empty>\n", i);
    } else {
      printf("%d: %s ($%lld)\n", i, cart.items[i]->name, cart.items[i]->price);
    }
  }
}

void buy_items() {
  char buf[0x20];
  int idx;
  int i;

  for (i = 0; i < 10; i++) {
    if (cart.items[i] == 0) {
      break;
    }
    info.wallet -= cart.items[i]->price;
    free(cart.items[i]);
  }
}

void replace_item() {
  char buf[0x20];
  int idx;

  if (info.edits <= 0) {
    printf("Shopee caught you trying to pwn them and banned you\n");
    exit(0);
  }

  info.edits--;
  view_cart();

  printf("Item to replace: ");
  fgets(buf, sizeof(buf), stdin);
  idx = atoi(buf);

  if (idx < 0 || idx > 9) {
    printf("Invalid index\n");
    return;
  }

  printf("Item to replace with: ");
  fgets(buf, sizeof(buf), stdin);
  memcpy(cart.items[idx], &items[atoi(buf)], sizeof(struct item));
}

void set_name() {
  char buf[sizeof(info.name)];
  memset(buf, 0, sizeof(buf));

  printf("\nName: ");
  fgets(buf, sizeof(buf), stdin);
  memcpy(info.name, buf, sizeof(buf));
}

int main() {
  char buf[0x50];
  int idx;

  setup();

  while (1) {
    menu();
    fgets(buf, sizeof(buf), stdin);
    idx = atoi(buf);

    switch (idx) {
    case 1:
      add_item();
      break;
    case 2:
      view_cart();
      break;
    case 3:
      buy_items();
      break;
    case 4:
      set_name();
      break;
    case 1337:
      replace_item();
      break;
    }
  }
}
