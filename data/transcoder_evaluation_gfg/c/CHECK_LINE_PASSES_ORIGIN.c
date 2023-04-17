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

bool f_gold ( int x1, int y1, int x2, int y2 ) {
  return ( x1 * ( y2 - y1 ) == y1 * ( x2 - x1 ) );
}


bool f_filled ( int x1, int y1, int x2, int y2 ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {1,10,0,1,82,78,13,18,42,29};
    int param1[] = {28,0,1,1,86,86,46,29,35,17};
    int param2[] = {2,20,0,10,19,11,33,95,25,45};
    int param3[] = {56,0,17,10,4,6,33,12,36,35};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}