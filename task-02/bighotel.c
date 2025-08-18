#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int T, X, Y, i;
    scanf("%d", &T);
    for (i = 0; i < T; i++) {
        scanf("%d %d",&X,&Y);
        int rjf,rvf;
        rjf=(X-1)/10 + 1;
        rvf =(Y-1)/10 +1;
        printf("%d\n",abs(rjf-rvf));
    }

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}
