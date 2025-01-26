#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>

struct player {
  char name[30];
  void *inv[30];
  int sizes[30];

  int hp; int ap; int dp; int gold;
  int completed;
};

struct player p;

int read_str(char *buf, int len) {
  int i;
  for (i = 0; i <= len; i++) {
    if (!read(0, buf + i, 1)) {
      return i;
    }
    if (buf[i] == '\n') {
      buf[i] = '\0';
      return i;
    }
  }
  return i;
}

int read_int() {
  char buf[10];
  read_str(buf, 10);
  return atoi(buf);
}

int view_inventory(struct player *p) {
  printf(
    "----------------------------------------\n"
    "|%16cInventory%16c|\n"
    "----------------------------------------\n",
    ' ', ' '
  );
  int count = 0;
  for (int i = 0; i < 30; i++) {
    if (p->inv[i] != NULL) {
      count++;
      printf("%d: %s\n", i, p->inv[i]);
    }
  }
  if (count == 0) {
    printf("Your inventory is empty\n");
  }
  printf("\n");
  return count;
}

void use_item(struct player *p) {
  if (!view_inventory(p)) {
    return;
  }

  printf("Which item do you want to use? > ");
  int idx = read_int();
  if (idx < 0 || idx >= 30 || p->inv[idx] == NULL) {
    printf("Invalid item\n");
    return;
  }

  if (strstr(p->inv[idx], "Health potion") != NULL) {
    printf("💉 You ate a %s and gained 10 HP!\n", p->inv[idx]);
    p->hp += 10;
  } else if (strstr(p->inv[idx], "Attack potion") != NULL) {
    printf("💪 You ate a %s and gained 5 AP!\n", p->inv[idx]);
    p->ap += 5;
  } else if (strstr(p->inv[idx], "Shield") != NULL) {
    printf("🛡️ You ate a %s and gained 5 DP!\n", p->inv[idx]);
    p->dp += 5;
  } else if (strstr(p->inv[idx], "Poison") != NULL) {
    printf("💀 You ate a %s and lost 10 HP!\n", p->inv[idx]);
    p->hp -= 10;
  } else if (strstr(p->inv[idx], "Sleeping pill") != NULL) {
    printf("💤 You ate a %s and fell asleep\n", p->inv[idx]);
    for (int i = 0; i < 3; i++) {
      printf("z");
      sleep(1);
    }
    printf("\n");
  } else if (strstr(p->inv[idx], "NeuroSynthoQuantaXenithron 5000") != NULL) {
    printf("🏃 You ate a %s and feel like you can run faster!\n", p->inv[idx]);
    printf("(might be a placebo tho)\n");
  } else if (strstr(p->inv[idx], "Big mac") != NULL) {
    printf("🍔 You ate a %s and gained 0.5kg!\n", p->inv[idx]);
  } else {
    printf("🤢 You ate a %s and had a tummy ache\n", p->inv[idx]);
  }

  free(p->inv[idx]);
  p->inv[idx] = NULL;
  p->sizes[idx] = 0;
  return;
}

void shop(struct player *p) {
  char buf[0x1000];
  int len = 0;

  printf(
    "----------------------------------------\n"
    "|%17cShop%17c|\n"
    "----------------------------------------\n"
    "\n",
    ' ', ' '
  );
  printf("You have %d gold\n", p->gold);
  printf(
    "1. Brew potion (20 gold)\n"
    "2. Rebrew potion (10 gold)\n"
    "3. Wishing well (1 gold)\n"
    "4. Exit\n"
    "> "
  );
  int choice = read_int();
  switch (choice) {
    case 1:
      if (p->gold < 20) {
        printf("You don't have enough gold\n");
        break;
      }

      printf("Brew your potion (eg. for a HP pot, enter \"Health potion\"):\n");
      printf("> ");
      len = read_str(buf, 0x1000);
      for (int i = 0; i < 30; i++) {
        if (p->inv[i] == NULL) {
          p->inv[i] = malloc(len);
          p->sizes[i] = len;
          strcpy(p->inv[i], buf);
          p->gold -= 20;
          break;
        }
      }
      break;
    case 2:
      if (p->gold < 10) {
        printf("You don't have enough gold\n");
        break;
      }

      if (!view_inventory(p)) {
        break;
      }

      printf("Select an item to rebrew\n");
      printf("> ");

      int idx = read_int();
      if (idx < 0 || idx >= 30 || p->inv[idx] == NULL) {
        printf("Invalid item\n");
        break;
      }

      printf("Rebrew your potion (eg. for a HP pot, enter \"Health potion\"):\n");
      printf("> ");
      read_str(p->inv[idx], p->sizes[idx]);
      p->gold -= 20;
      break;
    case 3:
      if (p->gold < 1) {
        printf("You don't have enough gold\n");
        break;
      }

      printf("You threw a gold coin into the well\n");

      int i = 0;
      for (i = 0; i < 30; i++) {
        if (p->inv[i] == NULL) {
          p->inv[i] = malloc(0);
          p->sizes[i] = 0;
          p->gold -= 1;
          break;
        }
      }
      sleep(1);
      printf("Nothing happens...");
      printf("(check your inventory at index %d)\n", i);
      break;
    default:
      printf("You left the shop\n");
      break;
  }
}

int menu(struct player *p) {
  printf(
    "----------------------------------------\n"
    "| %s's stats\n"
    "| 💓 HP: %3d\n"
    "| 🤜 AP: %3d\n"
    "| 🛡️ DP: %3d\n"
    "| 🪙 Gold: %3d\n"
    "| Campaign progress: %d/3\n"
    "----------------------------------------\n",
    p->name, p->hp, p->ap, p->dp, p->gold, p->completed
  );
  printf(
    "1. Enter Level %d\n"
    "2. Purchase items\n"
    "3. View inventory\n"
    "4. Use item\n"
    "> ",
    p->completed + 1
  );
  return read_int();
}

void level(struct player *p, int lvl) {
  char enemy_name[0x1000];
  char enemy_icon[16];
  int enemy_hp = 0;
  int enemy_ap = 0;
  int enemy_dp = 0;

  if (lvl == 1) {
    strcpy(enemy_name, "Lvl 1 Slime");
    strcpy(enemy_icon, "😱");
    enemy_hp = 30;
    enemy_ap = 10;
    enemy_dp = 0;
  } else if (lvl == 2) {
    strcpy(enemy_name, "Lvl 20 Continuous Robotic List");
    strcpy(enemy_icon, "🤖");
    enemy_hp = 100;
    enemy_ap = 30;
    enemy_dp = 10;
  } else if (lvl == 3) {
    strcpy(enemy_name, "Lvl 300 Algorithm of Semi-Intransient Matrix of Overseer Network");
    strcpy(enemy_icon, "👾");
    enemy_hp = 150;
    enemy_ap = 300;
    enemy_dp = 50;
  }

  int width = 35 - strlen(p->name);
  printf(
    "----------------------------------------\n"
    "|%15cLevel %d%16c|\n"
    "----------------------------------------\n"
    "\n",
    ' ', lvl, ' '
  );
  if (lvl == 3) {
    printf("FINAL BOSS FIGHT❗❗\n");
  }

  int dmg = 0;
  while (p->hp > 0 && enemy_hp > 0) {
    printf(
      "🤓%35c%s\n"
      "%s %*c %s\n"
      "HP: %3d %28c HP: %3d\n"
      "AP: %3d %28c AP: %3d\n"
      "DP: %3d %28c DP: %3d\n"
      "\n",
      ' ',
      enemy_icon,
      p->name, width, ' ', enemy_name,
      p->hp, ' ', enemy_hp,
      p->ap, ' ', enemy_ap,
      p->dp, ' ', enemy_dp
    );
    printf(
      "1. Attack\n"
      "2. Use item\n"
      "3. Run\n"
      "4. Do nothing\n"
    );
    printf("> ");

    int choice = read_int();
    switch (choice) {
      case 1:
        dmg = p->ap - enemy_dp;
        enemy_hp -= dmg;
        printf("💢 You attacked the %s for %d damage!\n", enemy_name, dmg);
        break;
      case 2:
        use_item(p);
        break;
      case 3:
        printf("🏃 You ran away\n");
        return;
      default:
        printf("😪 You took a short nap\n");
        break;
    }

    if (enemy_hp <= 0) {
      printf("\n");
      break;
    }

    dmg = enemy_ap - p->dp;
    p->hp -= dmg;
    printf("😣 The %s attacked you for %d damage!\n", enemy_name, dmg);
    printf("\n");
  }

  if (p->hp <= 0) {
    printf("😭\n");
    printf("You died...\n");
    exit(0);
  } else if (enemy_hp <= 0) {
    printf("😤\n");
    printf("You defeated the %s!\n", enemy_name);

    if (lvl == 1) {
      printf("(+2^10 gold)\n");
      p->gold += 1 << 10;
    } else if (lvl == 2) {
      printf("(+2^15 gold)\n");
      p->gold += 1 << 15;
    } else if (lvl == 3) {
      printf("(+2^20 gold)\n");
      p->gold += 1 << 20;
    }
    p->completed++;
  }

}

void setup(struct player *p) {
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);

  p->hp = 100;
  p->ap = 10;
  p->gold = 100;
  p->completed = 0;
  memset(p->inv, 0, sizeof(p->inv));
}

int main() {
  setup(&p);

  printf(
    "------------------------\n"
    "|  安心 丨爪卩卂匚ㄒ~  |\n"
    "------------------------\n"
  );
  printf("Welcome adventurer!\n");
  printf("What is your name?\n");
  printf("> ");
  read_str(p.name, 0x20);

  while (1) {
    int choice = menu(&p);
    switch (choice) {
      case 1:
        level(&p, p.completed + 1);
        break;
      case 2:
        shop(&p);
        break;
      case 3:
        view_inventory(&p);
        break;
      case 4:
        use_item(&p);
        break;
      default:
        printf("Invalid choice\n");
        break;
    }
    if (p.completed == 3) {
      printf("Congrats!\n");
      printf("Check out our other games: 世界 丨爪卩卂匚ㄒ, 世界: Star Rail!");
      break;
    }
  }
  return 0;
}
