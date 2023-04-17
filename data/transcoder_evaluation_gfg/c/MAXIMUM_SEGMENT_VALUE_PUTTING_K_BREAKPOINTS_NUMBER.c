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

int f_gold ( string & s, int k ) {
  int seg_len = strlen(s) - k;
  int res = 0;
  for ( int i = 0;
  i < seg_len;
  i ++ ) res = res * 10 + ( s [ i ] - '0' );
  int seg_len_pow = pow ( 10, seg_len - 1 );
  int curr_val = res;
  for ( int i = 1;
  i <= ( strlen(s) - seg_len );
  i ++ ) {
    curr_val = curr_val - ( s [ i - 1 ] - '0' ) * seg_len_pow;
    curr_val = curr_val * 10 + ( s [ i + seg_len - 1 ] - '0' );
    res = max ( res, curr_val );
  }
  return res;
}


int f_filled ( string & s, int k ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"kjgHiKOrCpvn","656666342","11010111010101","hTSBuAXHgWd","458794087","100000","EtbP","870292","1","DkRQuGByuhHcw"};
    int param1[] = {5,3,3,4,1,5,3,4,11,61};
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