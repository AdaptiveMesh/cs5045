#include <stdio.h>

int main() {
    int scores[] = {62, 75, 88, 91, 54, 70};
    int threshold = 70;
    int count = 0, total = 0;

    for (int i = 0; i < 6; i++) {
        if (scores[i] >= threshold) {
            count++;
            total += scores[i];
        }
    }

    printf("Students at or above %d: %d\n", threshold, count);
    printf("Sum of their scores: %d\n", total);
    return 0;
}
