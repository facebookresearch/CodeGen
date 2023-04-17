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

bool f_gold ( int A [ ], int arr_size, int sum ) {
  int l, r;
  sort ( A, A + arr_size );
  for ( int i = 0;
  i < arr_size - 2;
  i ++ ) {
    l = i + 1;
    r = arr_size - 1;
    while ( l < r ) {
      if ( A [ i ] + A [ l ] + A [ r ] == sum ) {
        printf ( "Triplet is %d, %d, %d", A [ i ], A [ l ], A [ r ] );
        return true;
      }
      else if ( A [ i ] + A [ l ] + A [ r ] < sum ) l ++;
      else r --;
    }
  }
  return false;
}


bool f_filled ( int A [ ], int arr_size, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {28,47,65,89};
int param0_1[] = {-26,-64,-2,96,-52,-14,-56,52,-70,70,-64,74,-8,18,78,14,6,-16,50,84,-90,12,-88,52,52,-40,58,-48,98,-66,46,-88,68,12,0,70,-42};
int param0_2[] = {0};
int param0_3[] = {49,66,22,93,52,54,80,87};
int param0_4[] = {-96,-92,-86,-74,-62,-60,-56,-54,-46,-38,-32,-26,-16,-16,-8,-4,0,6,20,28,42,44,56};
int param0_5[] = {1,0,0,0,0,0,1,0,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,1};
int param0_6[] = {1,2,16,16,20,24,24,38,41,54,57,72,79,83,89,90,96,97,98};
int param0_7[] = {52,22,78,-30};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {72,40,92,11,98,20,4,58,49,11,58,28,16,16,44,10,50,23,83,41,41,92,1,28,26,83,6,52,48,9,77,51};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {3,22,0,5,13,39,12,2,21,29};
    int param2[] = {3,24,0,7,19,39,12,3,16,27};
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