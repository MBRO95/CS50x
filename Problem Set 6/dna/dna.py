import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Please include 2 arguments: 1) Name of CSV file and 2) Name of text file")
        exit()
    # TODO: Read database file into a variable
    rows = []
    headers = []
    with open(sys.argv[1]) as file1:
        reader = csv.DictReader(file1)
        for header in reader.fieldnames:
            headers.append(header)
        headers.remove("name")
        for row in reader:
            rows.append(row)
    # print("Rows: " + str(rows))
    # print("Headers: " + str(headers))
    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file2:
        lines = file2.readlines()
        file_content = ''.join(lines)
        # print("FC: " + file_content)
    # TODO: Find longest match of each STR in DNA sequence
    dna_logger = {}
    for header in headers:
        dna_logger[header] = longest_match(file_content, header)
    # print("DNA Log: " + str(dna_logger))
    # TODO: Check database for matching profiles
    match_found = False
    for row in rows:
        # print(row)
        counter = 0
        for header in headers:
            # print(header)
            # print(dna_logger[header])
            # print(row[header])
            if (int(dna_logger[header]) == int(row[header])):
                # print("Match Found")
                counter += 1
            if (counter == len(headers)):
                print(row["name"])
                match_found = True
    if (match_found == False):
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
