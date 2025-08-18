#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int t, n, x, sec, b, i;
    scanf("%d", &t);

    for (i = 0; i < t; i++) {
        scanf("%d %d", &n, &x);
        int arr[n];
        for (int j = 0; j < n; j++) {
            scanf("%d", &arr[j]);
        }

        b = 0;          // button is OFF at start
        sec = 0;        // seconds left after pressing button
        int possible = 1; // assume YES

        for (int j = 0; j < n; j++) {
            if (arr[j] == 1) { // closed door
                if (b == 0) {  // first closed door -> press button
                    b = 1;
                    sec = x;
                }
                if (b == 1) {
                    if (sec > 0) {
                        sec--; // pass through using button time
                    } else {
                        possible = 0; // button time over, door closed
                        break;
                    }
                }
            } else { // open door
                if (b == 1 && sec > 0) {
                    sec--; // still consuming time after button press
                }
            }
        }

        if (possible) {
            printf("YES\n");
        } else {
            printf("NO\n");
        }
    }
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}
