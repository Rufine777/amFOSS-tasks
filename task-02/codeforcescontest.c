#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int X,T,i=0;
    scanf("%d",&T);
    for(i=0;i<T;i++){
        scanf("%d",&X);
        (X >= 1 && X <= 10) ? printf("YES\n") : printf("NO\n");
    }
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}
