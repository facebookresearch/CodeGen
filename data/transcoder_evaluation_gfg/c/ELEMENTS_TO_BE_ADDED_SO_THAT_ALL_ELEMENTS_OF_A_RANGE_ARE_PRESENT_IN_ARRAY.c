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

int f_gold ( int arr [ ], int n ) {
  int count = 0;
  sort ( arr, arr + n );
  for ( int i = 0;
  i < n - 1;
  i ++ ) if ( arr [ i ] != arr [ i + 1 ] && arr [ i ] != arr [ i + 1 ] - 1 ) count += arr [ i + 1 ] - arr [ i ] - 1;
  return count;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,4,5,7,7,9,13,15,18,19,25,27,27,29,32,36,48,51,53,53,55,65,66,67,72,74,74,76,77,79,80,81,82,83,83,86,87,97,98,98,99};
int param0_1[] = {34,6,-16,-26,-80,-90,-74,16,-84,64,-8,14,-52,-26,-90,-84,94,92,-88,-84,72};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {25,29,12,79,23,92,54,43,26,10,43,39,32,12,62,13,13};
int param0_4[] = {-94,-86,-72,-64,-64,-58,-56,-56,-56,-56,-54,-54,-52,-42,-42,-40,-36,-32,-28,-22,-20,-18,-12,-8,-6,-4,0,2,4,10,16,30,32,48,48,60,70,74,76,84};
int param0_5[] = {1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,0,1,0,1,1,1,0};
int param0_6[] = {4,5,8,12,16,16,17,20,20,23,26,26,27,28,32,34,40,40,41,41,44,45,47,49,51,52,54,57,60,62,63,64,66,68,69,70,71,76,77,80,80,80,90,91,92,94,96,98,99};
int param0_7[] = {66,-46,-92,-40,76,74,10,20,56,-46,88,-18,48,96,-48,-86,38,-98,50,4,-52,-38,14,-48,96,16,-74,-26,80,14,-92,-60,-78,-68,96,-72,-44,-92,2,60,4,48,84,-92};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {49,84,66};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {30,17,24,14,35,29,42,37,17,2};
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