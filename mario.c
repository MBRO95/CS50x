#include <cs50.h>
#include <stdio.h>

void brick_builder(int n);
void print_space(int n);
void print_brick(int n);

int main(void)
{
    int i = -1;
    while (i <= 0 || i > 8)
    {
        i = get_int ("Please enter a positive height value between 0-8: ");
    }
    //printf("Height: %i\n", i);
    brick_builder(i);
}

void brick_builder(int n){
    for(int i = 1; i <= n; i++)
    {
        print_space(n - i);
        print_brick(i);
        printf("  ");
        print_brick(i);
        printf("\n");
    }
}

void print_space(int n){
    for(int i = 0; i < n; i++)
    {
        printf(" ");
    }
}

void print_brick(int n){
    for(int i = 0; i < n; i++)
    {
        printf("#");
    }
}
