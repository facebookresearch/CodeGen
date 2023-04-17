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

int f_gold ( char a [], char b [] ) {
  int m = strlen(a);
  int n = strlen(b);
  int lookup [ m + 1 ] [ n + 1 ] = {
    {
      0 }
    };
    for ( int i = 0;
    i <= n;
    ++ i ) lookup [ 0 ] [ i ] = 0;
    for ( int i = 0;
    i <= m;
    ++ i ) lookup [ i ] [ 0 ] = 1;
    for ( int i = 1;
    i <= m;
    i ++ ) {
      for ( int j = 1;
      j <= n;
      j ++ ) {
        if ( a [ i - 1 ] == b [ j - 1 ] ) lookup [ i ] [ j ] = lookup [ i - 1 ] [ j - 1 ] + lookup [ i - 1 ] [ j ];
        else lookup [ i ] [ j ] = lookup [ i - 1 ] [ j ];
      }
    }
    return lookup [ m ] [ n ];
  }
  

int f_filled ( char a [], char b [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"fZOKCdZ Lav","2","1000001110","IAOyBzgIWHo","211806","1","CVaQTG","6265187228","10111101101000","vEi"};
    char param1[][100] = {"fKA","187012","0","oA","10","001011100","CT","628","01111","bigsvkQG"};
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