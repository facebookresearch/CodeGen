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

char f_gold [] ( int n, int k ) {
  char res [] = "";
  for ( int i = 0;
  i < k;
  i ++ ) res = res + ( char ) ( 'a' + i );
  int count = 0;
  for ( int i = 0;
  i < n - k;
  i ++ ) {
    res = res + ( char ) ( 'a' + count );
    count ++;
    if ( count == k ) count = 0;
  }
  return res;
}


char f_filled [] ( int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {60,56,16,42,55,64,68,88,64,42};
    int param1[] = {71,17,16,60,56,59,24,2,94,79};
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