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

char f_gold [] ( char s [], int n ) {
  char s1 [] = s;
  for ( int i = 1;
  i < n;
  i ++ ) s += s1;
  return s;
}


char f_filled [] ( char s [], int n ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"LPWsaI","9037515104","00100010010111","SbwipuE","574314109","1101","f","068","000011001","BWbUtIkC"};
    int param1[] = {41,72,95,27,5,70,91,50,38,79};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i]) == f_gold(param0[i],param1[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}