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
  if ( strlen(s) == 0 ) printf(0, endl);
  int ans = 0;
  int o = 0, c = 0;
  for ( int i = 0;
  i < strlen(s);
  i ++ ) {
    if ( s [ i ] == '(' ) o ++;
    if ( s [ i ] == ')' ) c ++;
  }
  if ( o != c ) return - 1;
  int a [ len(s) ];
  if ( s [ 0 ] == '(' ) a [ 0 ] = 1;
  else a [ 0 ] = - 1;
  if ( a [ 0 ] < 0 ) ans += abs ( a [ 0 ] );
  for ( int i = 1;
  i < strlen(s);
  i ++ ) {
    if ( s [ i ] == '(' ) a [ i ] = a [ i - 1 ] + 1;
    else a [ i ] = a [ i - 1 ] - 1;
    if ( a [ i ] < 0 ) ans += abs ( a [ i ] );
  }
  return ans;
}


int f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"()","))((","())","(()","(()()())","))())(()(())","))(())((","49","00001111","KDahByG "};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i]) == f_gold(param0[i]))
        {
            n_success+=1;
        }
    }
    printf(0, endl);
    return 0;
}