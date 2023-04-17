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

int f_gold ( char X [], char Y [] ) {
  int m = strlen(X);
  int n = strlen(Y);
  int result = 0;
  int len [ 2 ] [ n ];
  int currRow = 0;
  for ( int i = 0;
  i <= m;
  i ++ ) {
    for ( int j = 0;
    j <= n;
    j ++ ) {
      if ( i == 0 || j == 0 ) {
        len [ currRow ] [ j ] = 0;
      }
      else if ( X [ i - 1 ] == Y [ j - 1 ] ) {
        len [ currRow ] [ j ] = len [ 1 - currRow ] [ j - 1 ] + 1;
        result = max ( result, len [ currRow ] [ j ] );
      }
      else {
        len [ currRow ] [ j ] = 0;
      }
    }
    currRow = 1 - currRow;
  }
  return result;
}


int f_filled ( char X [], char Y [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"GeeksforGeeks","333940","1000","Facebook","2684247","111","abcdxyz","625330958530","01011000001111","KXm"};
    char param1[][100] = {"GeeksQuiz","390","0","nice book","1","10","xyzabcd","412511","1001010001","gF"};
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