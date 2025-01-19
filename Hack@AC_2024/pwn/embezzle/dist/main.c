#include <stdio.h>
#include <stdlib.h>
#include <time.h>
char projects[][8] = {"Hack@AC", "Website", "Laptops", "CCA", "Renovate"};

void setup(double *budgets){
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    time_t currTime;
    time(&currTime);
    srand(currTime);

    for(char i = 0; i < 5; i++){
        budgets[i] = (double)(rand() % 1000000) / 100;
    }
}

void menu(){
    puts("================================");
    puts("What would you like to do?");
    puts("1) List expenditures");
    puts("2) Embezzle");
    puts("3) Exit");
    printf("> ");
}

int main(){
    int choice = 0, limit = 0;
    char i;
    double prevValue;
    double budgets[5];
    setup(budgets);

    printf("The budget breakdown for this year is out!\n");
    while(1){
        menu();   
        scanf("%d", &choice);
        switch(choice){
            case 1:
                puts("Here are all the projects!");
                for(i = 0; i < 5; i++){
                    printf("%s: %.2lf\n", projects[i], budgets[i]);
                }
                break;
            case 2:
                printf("How much will you embezzle?\n> ");
                scanf("%d", &limit);
                
                puts("(Enter -1 to exit)");
                for(i = 0; i < limit; i++){
                    printf("Enter in the new budget for ");
                    puts(projects[i]);
                    prevValue = budgets[i];
                    scanf("%lf", &budgets[i]);

                    if(budgets[i] == -1){
                        budgets[i] = prevValue;
                        break;
                    }
                }
                break;
            case 3:
                return 0;
                break;
            default:
                puts("???");
                break;
        }
    }
}