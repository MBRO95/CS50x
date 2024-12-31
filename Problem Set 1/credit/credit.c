#include <cs50.h>
#include <math.h>
#include <stdio.h>

string validate_card(long n);
int long_length(long n);
long read_card(void);

int main(void)
{
    long card = get_long("Number: ");
    // printf("Card Number: %13ld\n", card);
    int length = long_length(card);
    if (card < 0 || length < 13 || length > 16)
    {
        if (length < 13)
        {
            // printf("Too short, try again\n");
        }
        else if (length > 16)
        {
            // printf("Too long, try again\n");
        }
        // i = get_long("Number: ");
        // length = long_length(i);
        printf("INVALID\n");
    }
    else
    {
        printf("%s", validate_card(card));
    }
}

string validate_card(long card)
{
    int length = long_length(card);
    int evens = 0;
    int odds = 0;
    long number = card;
    int count = 0;
    int first_num = 0;
    int second_num = 0;
    while (number != 0)
    {
        int remainder = number % 10;
        if (count % 2 != 0)
        {
            int product = remainder * 2;
            if (product < 10)
            {
                odds = odds + product;
            }
            else
            {
                int p_remainder = product % 10;
                odds = odds + p_remainder + 1;
            }
        }
        else
        {
            evens = evens + remainder;
        }
        if (count == length - 2)
        {
            second_num = remainder;
            // printf("Second: %i\n", second_num);
        }
        if (count == length - 1)
        {
            first_num = number;
            // printf("First: %i\n", first_num);
        }
        number = number / 10;
        count = count + 1;
    }
    // printf("Evens: %i; Odds: %i\n", evens, odds);
    int sum = evens + odds;
    // printf("Sum: %i\n", sum);
    int is_zero = sum % 10;
    if (is_zero == 0)
    {
        if (first_num == 4 && (length == 13 || length == 16))
        {
            return "VISA\n";
        }
        else if (first_num == 3)
        {
            if ((second_num == 4 || second_num == 7) && length == 15)
            {
                return "AMEX\n";
            }
        }
        else if (first_num == 5)
        {
            if ((second_num == 1 || second_num == 2 || second_num == 3 || second_num == 4 ||
                 second_num == 5) &&
                length == 16)
            {
                return "MASTERCARD\n";
            }
        }
        return "INVALID\n";
    }
    return "INVALID\n";
}

int long_length(long n)
{
    int result = floor(log10(n)) + 1;
    // printf("Length: %i\n", result);
    return result;
}
