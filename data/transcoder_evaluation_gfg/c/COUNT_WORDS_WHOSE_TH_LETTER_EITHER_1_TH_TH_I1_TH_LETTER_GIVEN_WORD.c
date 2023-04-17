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

int f_gold ( char str [ ], int len ) {
  int count = 1;
  if ( len == 1 ) return count;
  if ( str [ 0 ] == str [ 1 ] ) count *= 1;
  else count *= 2;
  for ( int j = 1;
  j < len - 1;
  j ++ ) {
    if ( str [ j ] == str [ j - 1 ] && str [ j ] == str [ j + 1 ] ) count *= 1;
    else if ( str [ j ] == str [ j - 1 ] || str [ j ] == str [ j + 1 ] || str [ j - 1 ] == str [ j + 1 ] ) count *= 2;
    else count *= 3;
  }
  if ( str [ len - 1 ] == str [ len - 2 ] ) count *= 1;
  else count *= 2;
  return count;
}


int f_filled ( char str [ ], int len ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"KbctqjpX","36506583562151","01010","Dr","09","110","K","04402109","010","aVHYrYmHjvnj "};
    int param1[] = {42,67,6,88,73,4,61,7,92,60};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(&param0[i].front(),param1[i]) == f_gold(&param0[i].front(),param1[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}