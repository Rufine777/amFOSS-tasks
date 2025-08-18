#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int T,X,Y,i;
    scanf("%d",&T);
    for(i=0;i<T;i++){
        scanf("%d %d",&X,&Y);
        (Y>=X)?printf("%d\n",X):printf("%d\n",Y);
    }

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
    return 0;
}

