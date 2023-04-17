// Copyright (c) 2019-present, Facebook, Inc.
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.
//


#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

int min(int x, int y) { return (x < y)? x: y; }
int max(int x, int y) { return (x > y)? x: y; }
int cmpfunc (const void * a, const void * b) {return ( *(int*)a - *(int*)b );}
int len (int arr [ ]) {return ((int) (sizeof (arr) / sizeof (arr)[0]));}
void sort (int arr [ ], int n) {qsort (arr, n, sizeof(int), cmpfunc);}

int f_gold ( double p ) {
  return ceil ( sqrt ( 2 * 365 * log ( 1 / ( 1 - p ) ) ) );
}


int f_filled ( double p ) {}

int main(void) {
    int n_success = 0;
    double param0[] = {0.9303713975220877,0.48126843587453595,0.48776789524757905,0.35184405927337793,0.8000415444743662,0.3528645948885943,0.33594265260473667,0.3603861267753616,7218.247044923335,-4701.904717953173};
    for(int i = 0; i < len(param0); ++i)
    {
        if(abs(1 - (0.0000001 + abs(f_gold(param0[i])) )/ (abs(f_filled(param0[i])) + 0.0000001)) < 0.001)
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}