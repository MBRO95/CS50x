#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int score_it(string word);

int main(void)
{
    // Prompt the user for two words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Compute the score of each word
    int score1 = score_it(word1);
    int score2 = score_it(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int score_it(string word)
{
    // Compute and return score
    int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    // Keep track of score
    int score = 0;

    // Compute score for each character
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // Check if uppercase
        if (isupper(word[i]))
        {
            // Using positional subtraction due to A character and subsequent letter having
            // sequential numbering in the ASCII map
            score += POINTS[word[i] - 'A'];
        }
        // Check if lowercase
        else if (islower(word[i]))
        {
            // Using positional subtraction due to A character and subsequent letter having
            // sequential numbering in the ASCII map
            score += POINTS[word[i] - 'a'];
        }
    }

    return score;
}
