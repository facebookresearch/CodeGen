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

int f_gold ( int num, int divisor ) {
  if ( divisor == 0 ) {
    printf("Error: divisor can't be zero 
");
    return - 1;
  }
  if ( divisor < 0 ) divisor = - divisor;
  if ( num < 0 ) num = - num;
  int i = 1;
  int product = 0;
  while ( product <= num ) {
    product = divisor * i;
    i ++;
  }
  return num - ( product - divisor );
}


int f_filled ( int num, int divisor ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {34,63,15,56,63,28,54,2,94,82};
    int param1[] = {55,22,26,58,94,45,97,58,91,40};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i]) == f_gold(param0[i],param1[i]))
        {
            n_success+=1;
        }
    }
    printf("Error: divisor can't be zero 
");
    return 0;
}