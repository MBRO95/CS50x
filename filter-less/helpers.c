#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all columns
    for (int i = 0; i < height; i++)
    {
        // Loop over all rows
        for (int j = 0; j < width; j++)
        {
            // Pull single pixel RGB values
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;
            // Take average of red, green, and blue
            int average = round((red + green + blue) / 3.0);

            // Update pixel values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all rows
    for (int i = 0; i < height; i++)
    {
        // Loop over all columns
        for (int j = 0; j < width; j++)
        {
            // Pull single pixel RGB values
            float red = (float) image[i][j].rgbtRed;
            float green = (float) image[i][j].rgbtGreen;
            float blue = (float) image[i][j].rgbtBlue;
            // Calculate sepia offsets
            int sepiaRed = round(.393 * red + .769 * green + .189 * blue);
            int sepiaGreen = round(.349 * red + .686 * green + .168 * blue);
            int sepiaBlue = round(.272 * red + .534 * green + .131 * blue);

            // Update pixel values
            if (sepiaRed < 255)
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            else
            {
                image[i][j].rgbtRed = 255;
            }
            if (sepiaGreen < 255)
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
            else
            {
                image[i][j].rgbtGreen = 255;
            }
            if (sepiaBlue < 255)
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
            else
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all rows
    for (int i = 0; i < height; i++)
    {
        // Loop over all columns
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    // Loop over all rows
    for (int i = 0; i < height; i++)
    {
        // Loop over all columns
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // check for valid adjacent pixels and average their values with the current pixel
    // to determine the new blurred current pixel value
    for (int i = 0; i < height; i++)
    {
        // Loop over all columns
        for (int j = 0; j < width; j++)
        {
            int sumred = 0;
            int sumgreen = 0;
            int sumblue = 0;
            int counter = 0;

            // check for adjacent rows
            for (int di = -1; di <= 1; di++)
            {
                // check for adjacent columns
                for (int dj = -1; dj <= 1; dj++)
                {
                    // set row origin (if 0, will result in -1)
                    int ni = i + di;
                    // set column origin (if 0, will result in -1)
                    int nj = j + dj;
                    // ensure pixel is within the image boundary:
                    // ni < 0 - above image;
                    // ni > height - below image;
                    // nj < 0 - left of image;
                    // nj > width - right of image
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        // pixel is valid so add the components to the running sums and
                        // increase counter since this was a valid pixel we found
                        sumred += copy[ni][nj].rgbtRed;
                        sumgreen += copy[ni][nj].rgbtGreen;
                        sumblue += copy[ni][nj].rgbtBlue;
                        counter++;
                    }
                }
            }

            // Here we set the new image to a rounded int after dividing the sum by a
            // float-casted counter integer to ensure we keep a valid remainder to
            // round up or down properly
            image[i][j].rgbtRed = round(sumred / (float) counter);
            image[i][j].rgbtGreen = round(sumgreen / (float) counter);
            image[i][j].rgbtBlue = round(sumblue / (float) counter);
        }
    }
    return;
}
