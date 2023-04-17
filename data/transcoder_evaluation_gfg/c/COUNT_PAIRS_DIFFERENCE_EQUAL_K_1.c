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

int f_gold ( int arr [ ], int n, int k ) {
  int count = 0;
  sort ( arr, arr + n );
  int l = 0;
  int r = 0;
  while ( r < n ) {
    if ( arr [ r ] - arr [ l ] == k ) {
      count ++;
      l ++;
      r ++;
    }
    else if ( arr [ r ] - arr [ l ] > k ) l ++;
    else r ++;
  }
  return count;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {5,5,10,19,29,32,40,60,65,70,72,89,92};
int param0_1[] = {-38,40,8,64,-38,56,4,8,84,60,-48,-78,-82,-88,-30,58,-58,62,-52,-98,24,22,14,68,-74,48,-56,-72,-90,26,-10,58,40,36,-80,68,58,-74,-46,-62,-12,74,-58};
int param0_2[] = {0,0,1};
int param0_3[] = {16,80,59,29,14,44,13,76,7,65,62,1,34,49,70,96,73,71,42,73,66,96};
int param0_4[] = {-98,-88,-58,-56,-48,-34,-22,-18,-14,-14,-8,-4,-2,2,18,38,42,46,54,68,70,90,94,96,98};
int param0_5[] = {0,1,1};
int param0_6[] = {11,43,50,58,60,68,75};
int param0_7[] = {86,94,-80,0,52,-56,42,88,-10,24,6,8};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {54,99,4,14,9,34,81,36,80,50,34,9,7};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {7,24,1,12,23,2,4,11,29,9};
    int param2[] = {12,36,1,16,22,1,4,9,30,8};
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