#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int assess_complexity(float average_letters, float average_sentences);
int count_them(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");
    int complexity = count_them(text);
    if (complexity < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (complexity >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", complexity);
    }
}

int assess_complexity(float average_letters, float average_sentences)
{
    // where L (average_letters) is the average number of letters per 100 words in the text
    // where S (average_sentences) is the average number of sentences per 100 words in the text.
    int complexity = round(0.0588 * average_letters - 0.296 * average_sentences - 15.8);
    return complexity;
}

int count_them(string text)
{
    int num_words = 0;
    int num_letters = 0;
    int num_sentences = 0;
    int sentence_words = 0;
    // Return the number of letters in text
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        char character = text[i];
        if (isalpha(character))
        {
            // We found a letter, increase letter tracker
            num_letters = num_letters + 1;
        }
        else if (isblank(character))
        {
            num_words = num_words + 1;
        }
        else if (character == '.' || character == '!' || character == '?')
        {
            // We found a period/exclamation/question, for sure...
            num_sentences = num_sentences + 1;
        }
    }
    // Account for last missing space (word)
    num_words = num_words + 1;
    // printf("Number of letters: %d\nNumber of words: %d\nNumber of sentences: %d\n",
    // num_letters, num_words, num_sentences);
    float average_letters = (float) num_letters / (float) num_words * 100;
    float average_sentences = (float) num_sentences / (float) num_words * 100;
    int result = assess_complexity(average_letters, average_sentences);
    // printf("Average letters: %f\nAverage words: %f\n", average_letters, average_sentences);
    // printf("Number of words: %d\nNumber of sentences: %d\n", num_words, num_sentences);
    return result;
}
