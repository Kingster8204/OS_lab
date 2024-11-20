#include <stdio.h>

// Function to find the Least Recently Used (LRU) page
int findLRU(int time[], int n) {
    int i, min = time[0], pos = 0;
    // Loop to find the least recently used page
    for (i = 1; i < n; i++) {
        if (time[i] < min) {
            min = time[i];  // Update min if a smaller value is found
            pos = i;        // Update position of LRU page
        }
    }
    return pos;  // Return position of least recently used page
}

int main() {
    int frames[10], pages[30], time[10], num_frames, num_pages, i, j, k, pos, page_faults = 0;
    int counter = 0;  // Counter to track the time

    // Ask user for the number of frames available
    printf("Enter number of frames: ");
    scanf("%d", &num_frames);

    // Ask user for the number of pages
    printf("Enter number of pages: ");
    scanf("%d", &num_pages);

    // Ask user to input the page reference string
    printf("Enter page reference string: ");
    for (i = 0; i < num_pages; i++) {
        scanf("%d", &pages[i]);  // Store each page reference in the pages array
    }

    // Initialize all frames to -1 (indicating empty frames)
    for (i = 0; i < num_frames; i++) {
        frames[i] = -1;
    }

    // Loop through each page request in the reference string
    for (i = 0; i < num_pages; i++) {
        int found = 0;  // Flag to check if the page is already in the frames

        // Check if the page is already in one of the frames
        for (j = 0; j < num_frames; j++) {
            if (frames[j] == pages[i]) {
                found = 1;  // Page is found in one of the frames
                counter++;   // Increment the counter for time tracking
                time[j] = counter;  // Update the last accessed time of the page
                break;  // Exit the loop since the page is found
            }
        }

        // If the page was not found in any of the frames (page fault)
        if (found == 0) {
            // If there are empty frames, place the page in the first empty frame
            if (i < num_frames) {
                frames[i] = pages[i];  // Load the page into the frame
                counter++;  // Increment counter
                time[i] = counter;  // Update the last accessed time of the page
            }
            // If no empty frames are available, replace the least recently used page
            else {
                pos = findLRU(time, num_frames);  // Get the index of LRU page
                frames[pos] = pages[i];  // Replace the LRU page with the new page
                counter++;  // Increment counter
                time[pos] = counter;  // Update the last accessed time of the replaced page
            }
            page_faults++;  // Increment the page fault counter since a page fault occurred
        }

        // Print the current status of frames after each page request
        printf("\nFrames: ");
        for (k = 0; k < num_frames; k++) {
            printf("%d ", frames[k]);  // Print each frame's content
        }
    }

    // Print the total number of page faults
    printf("\nTotal Page Faults = %d\n", page_faults);
    return 0;
}
