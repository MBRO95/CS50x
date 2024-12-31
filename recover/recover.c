#include <cs50.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: recover [path to file]\n");
        return 1;
    }
    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card != NULL)
    {
        // printf("Address: %p\n", &card);
        //  Create a buffer for a block of data
        const int buffer_size = 512;
        uint8_t buffer[buffer_size];
        uint8_t pattern1 = 0xff;
        uint8_t pattern2 = 0xd8;

        // While there's still data left to read from the memory card
        int image_number = 0;
        int jpeg_count = 0;
        // Set up naming
        char name[8];
        // Do jpeg creation
        FILE *image = NULL;
        size_t bytesRead = 0;
        while ((bytesRead = fread(buffer, 1, buffer_size, card)) == buffer_size && !feof(card))
        {
            if (bytesRead != 512)
            {
                printf("Error: Could not read data\n");
                return 1;
            }
            // Create JPEGs from the data
            if (buffer[0] == pattern1 && buffer[1] == pattern2 && buffer[2] == pattern1)
            {
                if (jpeg_count == 1)
                {
                    // An image already exists so this mean a new image was found
                    // Close previous file
                    if (image != NULL)
                    {
                        fclose(image);
                        // Increment image_number
                        image_number++;
                        // Reset jpeg_count
                        jpeg_count = 0;
                    }
                }
                // Generate new name
                sprintf(name, "%03d.jpg", image_number);
                // Open new file with new name
                image = fopen(name, "w");
                if (image != NULL)
                {
                    jpeg_count++;
                }
                else
                {
                    printf("Exception: Could not open file\n");
                    return 1;
                }
            }
            // Append to file
            if (image != NULL)
            {
                size_t bytesWritten = fwrite(buffer, 1, buffer_size, image);
                if (bytesWritten != buffer_size)
                {
                    printf("Error: Could not write data\n");
                    return 1;
                }
            }
        }
        fclose(card);
        if (image != NULL)
        {
            fclose(image);
        }
    }
    else
    {
        printf("Exception: Could not open file\n");
        return 1;
    }
}
