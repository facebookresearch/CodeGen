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

int f_gold ( int r ) {
  if ( r <= 0 ) return 0;
  int result = 4;
  for ( int x = 1;
  x < r;
  x ++ ) {
    int ySquare = r * r - x * x;
    int y = sqrt ( ySquare );
    if ( y * y == ySquare ) result += 4;
  }
  return result;
}


int f_filled ( int r ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {34,56,90,47,36,63,21,76,18,75};
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