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

int f_gold ( char s [ ] ) {
  int n = strlen ( s );
  int count = 0;
  for ( int i = 0;
  i < n;
  ++ i ) if ( s [ i ] == '4' || s [ i ] == '8' || s [ i ] == '0' ) count ++;
  for ( int i = 0;
  i < n - 1;
  ++ i ) {
    int h = ( s [ i ] - '0' ) * 10 + ( s [ i + 1 ] - '0' );
    if ( h % 4 == 0 ) count = count + i + 1;
  }
  return count;
}


int f_filled ( char s [ ] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"Qaq","9400761825850","0011001111","lasWqrLRq","5662","110"," tOYKf","6536991235305","11111","uZftT iDHcYiCt"};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(&param0[i].front()) == f_gold(&param0[i].front()))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}