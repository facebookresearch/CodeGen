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
  int n = len(s);
  int ans = - 1;
  char num [];
  for ( int i = 1;
  i < ( 1 << n );
  i ++ ) {
    char str [] = "";
    for ( int j = 0;
    j < n;
    j ++ ) {
      if ( ( i >> j ) & 1 ) {
        str += s [ j ];
      }
    }
    if ( str [ 0 ] != '0' ) {
      int temp = 0;
      for ( int j = 0;
      j < len(str);
      j ++ ) temp = temp * 10 + ( int ) ( str [ j ] - '0' );
      int k = sqrt ( temp );
      if ( k * k == temp ) {
        if ( ans < ( int ) len(str) ) {
          ans = ( int ) len(str);
          num = str;
        }
      }
    }
  }
  if ( ans == - 1 ) return ans;
  else {
    printf(num, " ");
    return n - ans;
  }
}


int f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"h","1391212","010","ksRFLRVL","5809836998","1111000","hJoDzrrBaF","6076","001010010","lU DBBVF"};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i]) == f_gold(param0[i]))
        {
            n_success+=1;
        }
    }
    printf(num, " ");
    return 0;
}