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

char f_gold [] ( char str [] ) {
  char mx [] = "";
  for ( int i = 0;
  i < strlen(str);
  ++ i ) mx = max ( mx, str . substr ( i ) );
  return mx;
}


char f_filled [] ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"HCoAefoaan","80336005","01111111110","qIH","4210598472796","10101","imqmKdatcgXjs","950509666021","10111101101","wasqgYFvz"};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i]) == f_gold(param0[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}