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

int f_gold ( int m, int n ) {
  long long factorCount [ n + 1 ];
  bool prime [ n + 1 ];
  for ( int i = 0;
  i <= n;
  i ++ ) {
    factorCount [ i ] = 0;
    prime [ i ] = true;
  }
  for ( int i = 2;
  i <= n;
  i ++ ) {
    if ( prime [ i ] == true ) {
      factorCount [ i ] = 1;
      for ( int j = i * 2;
      j <= n;
      j += i ) {
        factorCount [ j ] ++;
        prime [ j ] = false;
      }
    }
  }
  int max = factorCount [ m ];
  int num = m;
  for ( int i = m;
  i <= n;
  i ++ ) {
    if ( factorCount [ i ] > max ) {
      max = factorCount [ i ];
      num = i;
    }
  }
  return num;
}


int f_filled ( int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {21,92,1,51,97,74,18,45,31,23};
    int param1[] = {6,53,60,85,72,17,37,75,47,87};
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