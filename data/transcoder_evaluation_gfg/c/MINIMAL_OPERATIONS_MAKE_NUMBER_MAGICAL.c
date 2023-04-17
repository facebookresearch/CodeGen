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
  int ans = 6;
  for ( int i = 0;
  i < 10;
  ++ i ) {
    for ( int j = 0;
    j < 10;
    ++ j ) {
      for ( int k = 0;
      k < 10;
      ++ k ) {
        for ( int l = 0;
        l < 10;
        ++ l ) {
          for ( int m = 0;
          m < 10;
          ++ m ) {
            for ( int n = 0;
            n < 10;
            ++ n ) {
              if ( i + j + k == l + m + n ) {
                int c = 0;
                if ( i != s [ 0 ] - '0' ) c ++;
                if ( j != s [ 1 ] - '0' ) c ++;
                if ( k != s [ 2 ] - '0' ) c ++;
                if ( l != s [ 3 ] - '0' ) c ++;
                if ( m != s [ 4 ] - '0' ) c ++;
                if ( n != s [ 5 ] - '0' ) c ++;
                if ( c < ans ) ans = c;
              }
            }
          }
        }
      }
    }
  }
  return ans;
}


int f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"RHn","123635172","10","WqWeJgrVkLU","453745797","0011010110","OGhkmFYf ","96","101001","kN"};
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