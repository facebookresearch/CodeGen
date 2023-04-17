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

int f_gold ( char str [], int n ) {
  int len = strlen(str);
  int dp [ len ] [ n ];
  memset ( dp, 0, sizeof ( dp ) );
  dp [ 0 ] [ ( str [ 0 ] - '0' ) % n ] ++;
  for ( int i = 1;
  i < len;
  i ++ ) {
    dp [ i ] [ ( str [ i ] - '0' ) % n ] ++;
    for ( int j = 0;
    j < n;
    j ++ ) {
      dp [ i ] [ j ] += dp [ i - 1 ] [ j ];
      dp [ i ] [ ( j * 10 + ( str [ i ] - '0' ) ) % n ] += dp [ i - 1 ] [ j ];
    }
  }
  return dp [ len - 1 ] [ 0 ];
}


int f_filled ( char str [], int n ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"fYqkPLSWBgFy","151587","111111110","JQJHaUkkTrt","736592575580","10","L","3476601","0110001001","YimayLFU"};
    int param1[] = {55,84,9,97,68,3,74,2,53,45};
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