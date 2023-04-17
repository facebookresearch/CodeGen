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

int f_gold ( char str [] ) {
  vector < pair < char, int > > arr;
  arr . push_back ( {
    '@', - 1 }
    );
    int maxlen = 0;
    for ( int i = 0;
    i < strlen(str);
    ++ i ) {
      arr . push_back ( {
        str [ i ], i }
        );
        while ( len(arr) >= 3 && arr [ len(arr) - 3 ] . first == '1' && arr [ len(arr) - 2 ] . first == '0' && arr [ len(arr) - 1 ] . first == '0' ) {
          arr . pop_back ( );
          arr . pop_back ( );
          arr . pop_back ( );
        }
        int tmp = arr . back ( ) . second;
        maxlen = max ( maxlen, i - tmp );
      }
      return maxlen;
    }
    

int f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"U","544","111"," cDQaNxpRSOe","42920062459","00100101","FiC","302746335230","1","ZBLHiwGreUR "};
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