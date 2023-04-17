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

int f_gold ( int n ) {
  int result = 0;
  for ( int i = 1;
  i <= 9;
  i ++ ) {
    stack < int > s;
    if ( i <= n ) {
      s . push ( i );
      result ++;
    }
    while ( ! s . empty ( ) ) {
      int tp = s . top ( );
      s . pop ( );
      for ( int j = tp % 10;
      j <= 9;
      j ++ ) {
        int x = tp * 10 + j;
        if ( x <= n ) {
          s . push ( x );
          result ++;
        }
      }
    }
  }
  return result;
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {69,72,88,7,66,34,23,37,33,21};
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