

def assess_complexity(average_letters, average_sentences):
    # where L (average_letters) is the average number of letters per 100 words in the text
    # where S (average_sentences) is the average number of sentences per 100 words in the text.
    complexity = round(0.0588 * average_letters - 0.296 * average_sentences - 15.8)
    return complexity


def count_them(text):
    num_words = 0
    num_letters = 0
    num_sentences = 0
    sentence_words = 0
    # Return the number of letters in text
    for i in range(0, len(text)):
        character = text[i]
        if character.isalpha():
            # We found a letter, increase letter tracker
            num_letters += 1
        elif character.isspace():
            num_words += 1
        elif (character == "." or character == "!" or character == "?"):
            # We found a period/exclamation/question, for sure...
            num_sentences += 1
    # Account for last missing space (word)
    num_words += 1
    # print("Number of letters: ", num_letters, " Number of words: ", num_words, " Number of sentences: ", num_sentences)
    average_letters = float(num_letters) / float(num_words) * 100
    average_sentences = float(num_sentences) / float(num_words) * 100
    result = assess_complexity(average_letters, average_sentences)
    # print("Average letters: ", average_letters, " Average words: ", average_sentences)
    # print("Number of words: ", num_words, " Number of sentences: ", num_sentences)
    return result


# Prompt the user for some text
text = input("Text: ")
complexity = count_them(text)
if complexity < 1:
    print("Before Grade 1")
elif complexity >= 16:
    print("Grade 16+")
else:
    print("Grade ", complexity)
