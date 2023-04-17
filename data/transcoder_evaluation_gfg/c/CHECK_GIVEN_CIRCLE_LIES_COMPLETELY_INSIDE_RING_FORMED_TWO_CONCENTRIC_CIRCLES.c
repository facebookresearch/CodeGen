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

bool f_gold ( int r, int R, int r1, int x1, int y1 ) {
  int dis = sqrt ( x1 * x1 + y1 * y1 );
  return ( dis - r1 >= R && dis + r1 <= r );
}


bool f_filled ( int r, int R, int r1, int x1, int y1 ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {8,400,1,61,60,88,60,26,33,70};
    int param1[] = {4,1,400,40,49,10,79,88,65,57};
    int param2[] = {2,10,10,2,68,69,92,75,57,77};
    int param3[] = {6,74,74,50,77,71,29,84,21,52};
    int param4[] = {0,38,38,0,71,26,38,10,61,87};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i],param4[i]) == f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}