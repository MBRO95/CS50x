// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
// Chose a balanced prime number based on research that showed that prime numbers are less prone to
// collisions http://www.cse.yorku.ca/~oz/hash.html;
// https://www.reddit.com/r/3Blue1Brown/comments/nljzi8/magic_number_33_in_djb2_hash_algorithm/;
// https://softwareengineering.stackexchange.com/questions/402542/where-do-magic-hashing-constants-like-0x9e3779b9-and-0x9e3779b1-come-from
// https://en.wikipedia.org/wiki/Balanced_prime
const unsigned int N = 1103;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int check_it = hash(word);
    node *cursor = table[check_it];
    while (cursor != NULL)
    {
        const char *word_found = cursor->word;
        if (strcasecmp(word, word_found) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Track how many words have been loaded
unsigned int num_words = 0;

// Hashes word to a number
unsigned int hash(const char *word)
{
    // We start with a magic number constant, which happens to be a balanced prime
    // https://en.wikipedia.org/wiki/Magic_number_(programming)
    // https://en.wikipedia.org/wiki/Balanced_prime
    unsigned int hash_value = 53;
    // Chosen as a balanced prime as well
    unsigned int p = 5;
    unsigned int p_pow = 1;
    // Improve this hash function
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // Ensure character is uppercase
        char c = toupper(word[i]);
        // Calculate hash value based on research.
        // This function includes weighting of both letter and position within a given word.
        // Still finding the letter offset but adding one to prevent 0 or NULL values by utilizing a
        // 1-26 mapping vs. 0-25. However, we're then multiplying by a dynamically expanding number
        // (p_pow) to provide different weighting. Modulo by number of buckets to keep within the
        // constraints; prevents overflow and ensures fit within prescribed table.
        hash_value = (hash_value + (c - 'A' + 1) * p_pow) % N;
        // This sets up a per-character weighting mechanism which increase exponentially each char.
        p_pow = (p_pow * p) % N;
    }
    // Modulo by the number of buckets, which was chosen to be prime as well to help ensure a
    // balanced distribution.
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
// bool load(const char *dictionary)
// {
//     // Open the dictionary file
//     FILE *input = fopen(dictionary, "r");
//     if (input == NULL)
//     {
//         printf("Could not open file.\n");
//         return false;
//     }
//     // Create word buffer to read in each line 1 by 1
//     char word[LENGTH + 1];
//     // Read each word in the file
//     while (fscanf(input, "%s", word) != EOF)
//     {
//         // Add each word to the hash table
//         int hashed = hash(word);
//         // Create hash table node
//         node *new_word = malloc(sizeof(node));
//         if (new_word == NULL)
//         {
//             // Memory allocation error
//             return false;
//         }
//         // Copy word into the nodes' word definition
//         strcpy(new_word->word, word);
//         // Set nodes' next definition to the computed hash
//         new_word->next = table[hashed];
//         // Set hash table location value to the new_word struct
//         table[hashed] = new_word;
//         num_words++;
//     }
//     // Close the dictionary file
//     if (input != NULL)
//     {
//         fclose(input);
//     }
//     return false;
// }
bool load(const char *dictionary)
{
    printf("Attempting to open dictionary: %s\n", dictionary);
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }
    printf("File opened successfully.\n");

    char word[LENGTH + 1];
    while (fscanf(input, "%s", word) != EOF)
    {
        int hashed = hash(word);
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            printf("Memory allocation error.\n");
            return false;
        }
        strcpy(new_word->word, word);
        new_word->next = table[hashed];
        table[hashed] = new_word;
        num_words++;
    }
    fclose(input);
    printf("Dictionary loaded successfully.\n");
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
