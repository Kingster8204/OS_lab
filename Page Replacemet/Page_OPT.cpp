#include <stdio.h>

// Function to find the optimal page to replace
int findOptimal(int pages[], int n, int frames[], int m, int currIndex) {
    int farthest = -1, indexToReplace = -1;
    
    // Loop through each frame to find the optimal page to replace
    for (int i = 0; i < m; i++) {
        int found = 0;
        
        // Look ahead to find the next occurrence of the page in the frames
        for (int j = currIndex + 1; j < n; j++) {
            if (frames[i] == pages[j]) {
                found = 1;
                // Update farthest if this page is used later than previous ones
                if (j > farthest) {
                    farthest = j;
                    indexToReplace = i;
                }
                break;
            }
        }
        
        // If the page is not found in future, replace this frame
        if (found == 0) {
            return i; // Page not found in future, so replace this frame
        }
    }
    
    return indexToReplace; // Return index of the page to replace
}

int main() {
    int pages[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3}; // Page reference string
    int n = sizeof(pages) / sizeof(pages[0]); // Number of pages
    int frames[3]; // Frame size (3 frames)
    int m = sizeof(frames) / sizeof(frames[0]); // Number of frames
    int pageFaults = 0; // Page fault counter

    // Initialize frames to -1 (empty)
    for (int i = 0; i < m; i++) {
        frames[i] = -1;
    }

    // Traverse through the page reference string
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        int found = 0;

        // Check if the page is already in the frames
        for (int j = 0; j < m; j++) {
            if (frames[j] == page) {
                found = 1; // Page found in frames, no page fault
                break;
            }
        }

        // If the page is not found in the frames, a page fault occurs
        if (!found) {
            pageFaults++;
            // Find the optimal page to replace using the Optimal Page Replacement algorithm
            int replaceIndex = findOptimal(pages, n, frames, m, i);
            frames[replaceIndex] = page; // Replace the page at the selected frame index
        }

        // Display the current status of frames
        printf("Frame status after page %d: ", page);
        for (int j = 0; j < m; j++) {
            printf("%d ", frames[j]);
        }
        printf("\n");
    }

    // Display the total number of page faults
    printf("Total page faults: %d\n", pageFaults);

    return 0;
}
