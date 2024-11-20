#include <stdio.h>

int main() {
    int frames[10], pages[30], num_frames, num_pages, i, j, k, page_faults = 0;
    int oldest = 0;

    // Input for number of frames and pages
    printf("Enter number of frames: ");
    scanf("%d", &num_frames);

    printf("Enter number of pages: ");
    scanf("%d", &num_pages);

    printf("Enter page reference string: ");
    for (i = 0; i < num_pages; i++) {
        scanf("%d", &pages[i]);
    }

    // Initialize frames as empty (with -1 representing empty frames)
    for (i = 0; i < num_frames; i++) {
        frames[i] = -1;
    }

    // Start processing pages
    for (i = 0; i < num_pages; i++) {
        int found = 0;

        // Check if the page is already in any of the frames
        for (j = 0; j < num_frames; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                break;
            }
        }

        // If the page is not found in frames, it's a page fault
        if (!found) {
            // Replace the oldest page (FIFO)
            frames[oldest] = pages[i];

            // Update the 'oldest' to point to the next frame for the next replacement
            oldest = (oldest + 1) % num_frames;

            // Increment page fault count
            page_faults++;
        }

        // Print the current state of frames
        printf("\nFrames: ");
        for (k = 0; k < num_frames; k++) {
            printf("%d ", frames[k]);
        }
    }

    // Print the total page faults
    printf("\nTotal Page Faults = %d\n", page_faults);
    return 0;
}
