#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int T, N, i, j;
    scanf("%d", &T);

    for (i = 0; i < T; i++) {
        scanf("%d", &N);

        int freq[11] = {0}; 

        
        for (j = 0; j < N; j++) {
            int num;
            scanf("%d", &num);
            freq[num]++;
        }

        int maxFreq = 0;
        for (j = 1; j <= 10; j++) {
            if (freq[j] > maxFreq) {
                maxFreq = freq[j];
            }
        }

        printf("%d\n", N - maxFreq);
    }

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}
