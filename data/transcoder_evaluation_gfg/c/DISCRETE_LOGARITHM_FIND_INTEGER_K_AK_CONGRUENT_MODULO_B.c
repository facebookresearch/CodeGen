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

int f_gold ( int a, int b, int m ) {
  int n = ( int ) sqrt ( m ) + 1;
  int an = 1;
  for ( int i = 0;
  i < n;
  ++ i ) an = ( an * a ) % m;
  unordered_map < int, int > value;
  for ( int i = 1, cur = an;
  i <= n;
  ++ i ) {
    if ( ! value [ cur ] ) value [ cur ] = i;
    cur = ( cur * an ) % m;
  }
  for ( int i = 0, cur = b;
  i <= n;
  ++ i ) {
    if ( value [ cur ] ) {
      int ans = value [ cur ] * n - i;
      if ( ans < m ) return ans;
    }
    cur = ( cur * a ) % m;
  }
  return - 1;
}


int f_filled ( int a, int b, int m ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {38,10,55,3,80,65,47,50,44,47};
    int param1[] = {81,97,63,18,48,87,79,74,86,8};
    int param2[] = {29,69,15,41,77,97,19,90,56,77};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}