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

        b = 0;         
        sec = 0;        
        int possible = 1; 

        for (int j = 0; j < n; j++) {
            if (arr[j] == 1) { 
                if (b == 0) {  
                    b = 1;
                    sec = x;
                }
                if (b == 1) {
                    if (sec > 0) {
                        sec--; 
                    } else {
                        possible = 0; 
                        break;
                    }
                }
            } else { 
                if (b == 1 && sec > 0) {
                    sec--; 
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
