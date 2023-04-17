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

int f_gold ( int arr [ ], int n, int x ) {
  int i;
  for ( i = 0;
  i < n - 1;
  i ++ ) if ( arr [ i ] > arr [ i + 1 ] ) break;
  int l = ( i + 1 ) % n;
  int r = i;
  int cnt = 0;
  while ( l != r ) {
    if ( arr [ l ] + arr [ r ] == x ) {
      cnt ++;
      if ( l == ( r - 1 + n ) % n ) {
        return cnt;
      }
      l = ( l + 1 ) % n;
      r = ( r - 1 + n ) % n;
    }
    else if ( arr [ l ] + arr [ r ] < x ) l = ( l + 1 ) % n;
    else r = ( n + r - 1 ) % n;
  }
  return cnt;
}


int f_filled ( int arr [ ], int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {24,54};
int param0_1[] = {68,-30,-18,-6,70,-40,86,98,-24,-48};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {84,44,40,45,2,41,52,17,50,41,5,52,48,90,13,55,34,55,94,44,41,2};
int param0_4[] = {-92,-76,-74,-72,-68,-64,-58,-44,-44,-38,-26,-24,-20,-12,-8,-8,-4,10,10,10,20,20,26,26,28,50,52,54,60,66,72,74,78,78,78,80,86,88};
int param0_5[] = {1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0,1,1,1};
int param0_6[] = {5,5,15,19,22,24,26,27,28,32,37,39,40,43,49,52,55,56,58,58,59,62,67,68,77,79,79,80,81,87,95,95,96,98,98};
int param0_7[] = {-98,28,54,44,-98,-70,48,-98,56,4,-18,26,-8,-58,30,82,4,-38,42,64,-28};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {26,72,74,86,98,86,22,6,95,36,11,82,34,3,50,36,81,94,55,30,62,53,50,95,32,83,9,16};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {1,8,33,18,29,19,28,17,24,19};
    int param2[] = {1,8,28,16,30,10,34,14,24,16};
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