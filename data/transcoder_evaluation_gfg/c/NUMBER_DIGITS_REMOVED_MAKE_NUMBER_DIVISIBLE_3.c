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

int f_gold ( char num [] ) {
  int n = strlen(num);
  int sum = accumulate ( begin ( num ), end ( num ), 0 ) - '0' * 1;
  if ( sum % 3 == 0 ) return 0;
  if ( n == 1 ) return - 1;
  for ( int i = 0;
  i < n;
  i ++ ) if ( sum % 3 == ( num [ i ] - '0' ) % 3 ) return 1;
  if ( n == 2 ) return - 1;
  return 2;
}


int f_filled ( char num [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"wVVe","850390909067","1110","NRSAazejUS","297975","1","ThYMuVOm","1874418087476","11011001001","YJ"};
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