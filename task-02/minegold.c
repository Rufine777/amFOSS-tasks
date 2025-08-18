#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int T,N,X,Y,i;
    scanf("%d",&T);
    for(i=0;i<T;i++){
        scanf("%d %d %d",&N,&X,&Y);
        ((N+1)*Y>=X)?printf("YES\n"):printf("NO\n");
    }

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}

