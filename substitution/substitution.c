#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool check_phrase(string keyphrase);
string encrypt(string message, string keyphrase);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Too few or too many arguments!\n");
        return 1;
    }
    else
    {
        // Get substitution key from command line arg
        string keyphrase = argv[1];
        if (check_phrase(keyphrase))
        {
            string message = get_string("plaintext: ");
            string ciphertext = encrypt(message, keyphrase);
            printf("ciphertext: %s\n", ciphertext);
            // https://www.freecodecamp.org/news/malloc-in-c-dynamic-memory-allocation-in-c-explained
            free(ciphertext);
            return 0;
        }
        else
        {
            return 1;
        }
    }
}

bool check_phrase(string keyphrase)
{
    if (strlen(keyphrase) != 26)
    {
        printf("Invalid keyphrase - Length!\n");
        return false;
    }

    // https://stackoverflow.com/questions/4142745/initialize-a-string-in-c-to-empty-string
    // https://stackoverflow.com/questions/55821717/how-do-i-convert-a-character-array-to-a-string
    char checked[27];
    checked[0] = '\0';

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(keyphrase[i]))
        {
            printf("Invalid keyphrase - Not Alpha!\n");
            return false;
        }

        char letter = tolower(keyphrase[i]);
        if (strchr(checked, letter) != NULL)
        {
            printf("Invalid keyphrase - Repeat!\n");
            return false;
        }
        else
        {
            int len = strlen(checked);
            checked[len] = letter;
            checked[len + 1] = '\0';
        }
    }
    return true;
}

string encrypt(string message, string keyphrase)
{
    // Build char array to populate with substituted characters; Add one for term char '\0'
    int length = strlen(message);
    // https://www.freecodecamp.org/news/malloc-in-c-dynamic-memory-allocation-in-c-explained
    char *encrypted = malloc(length + 1);

    for (int i = 0; i < length; i++)
    {
        // Check if not alphabetical
        if (!isalpha(message[i]))
        {
            encrypted[i] = message[i];
        }
        else
        {
            // Check if uppercase
            if (isupper(message[i]))
            {
                // Using positional subtraction due to A character and subsequent letter having
                // sequential numbering in the ASCII map
                encrypted[i] = toupper(keyphrase[message[i] - 'A']);
            }
            // Check if lowercase
            else if (islower(message[i]))
            {
                // Using positional subtraction due to A character and subsequent letter having
                // sequential numbering in the ASCII map
                encrypted[i] = tolower(keyphrase[message[i] - 'a']);
            }
        }
    }
    // https://stackoverflow.com/questions/4142745/initialize-a-string-in-c-to-empty-string
    // https://stackoverflow.com/questions/55821717/how-do-i-convert-a-character-array-to-a-string
    encrypted[length] = '\0';
    return encrypted;
}
