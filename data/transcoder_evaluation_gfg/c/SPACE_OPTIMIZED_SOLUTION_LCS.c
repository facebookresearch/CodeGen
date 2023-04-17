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

int f_gold ( string & X, string & Y ) {
  int m = strlen(X), n = strlen(Y);
  int L [ 2 ] [ n + 1 ];
  bool bi;
  for ( int i = 0;
  i <= m;
  i ++ ) {
    bi = i & 1;
    for ( int j = 0;
    j <= n;
    j ++ ) {
      if ( i == 0 || j == 0 ) L [ bi ] [ j ] = 0;
      else if ( X [ i - 1 ] == Y [ j - 1 ] ) L [ bi ] [ j ] = L [ 1 - bi ] [ j - 1 ] + 1;
      else L [ bi ] [ j ] = max ( L [ 1 - bi ] [ j ], L [ bi ] [ j - 1 ] );
    }
  }
  return L [ bi ] [ n ];
}


int f_filled ( string & X, string & Y ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"YNpjSv","736519","11010000100010","v ","8311172","100011101011","u","3943042","101","MpbfF OsizevaM"};
    char param1[][100] = {"qtUkJn","07592","0","qGBQT","157219329531","1000001111","YzkubTqLhP","3859","00010000101010","WgsFGaQwtp"};
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