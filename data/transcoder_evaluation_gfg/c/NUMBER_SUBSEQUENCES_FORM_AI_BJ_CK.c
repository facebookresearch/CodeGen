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

int f_gold ( char s [] ) {
  int aCount = 0;
  int bCount = 0;
  int cCount = 0;
  for ( unsigned int i = 0;
  i < len(s);
  i ++ ) {
    if ( s [ i ] == 'a' ) aCount = ( 1 + 2 * aCount );
    else if ( s [ i ] == 'b' ) bCount = ( aCount + 2 * bCount );
    else if ( s [ i ] == 'c' ) cCount = ( bCount + 2 * cCount );
  }
  return cCount;
}


int f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"","abbc","abcabc","agsdbkfdc","ababab","aaaaaaa","aabaaabcc","19","1001100","DtAnuQbU"};
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