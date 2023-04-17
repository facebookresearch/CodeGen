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

int f_gold ( int a [ ], int n, int l, int r ) {
  int count = 0;
  for ( int i = l;
  i < r;
  i ++ ) if ( a [ i ] == a [ i + 1 ] ) count += 1;
  return count;
}


int f_filled ( int a [ ], int n, int l, int r ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,13,13,16,16,19,39,41,48,52,57,62,65,67,76,84,88,91,95,96,97,98};
int param0_1[] = {62,76,86,-8,84,-6,72,84,6,-50,-18,-94,54,90,-74,-64,-26,-14,-32,62,10,4,70,-28,8,18,4,-62,-76,84,-78,-4,84,98,58,-68,42,-6,34,-38,52,-84,78};
int param0_2[] = {0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {11,75,98,29,62,53,48,91,86,66,48,94};
int param0_4[] = {-94,-84,-70,-70,-40,-40,-36,-24,10,48,62,74};
int param0_5[] = {1,0,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,0};
int param0_6[] = {1,2,6,7,10,11,13,19,19,25,29,30,32,34,35,45,45,46,47,48,48,53,58,61,64,65,67,75,76,81,81,84,84,85,86,94,94,96,99};
int param0_7[] = {-56,42,-34,-12,-86,82,-96,-66,30,16,-40,72,84,94,-48,-30,26,50,42,-44,-50,22,-38,8,34,94,2,16,-32,18,-58,12,-26,28,-62};
int param0_8[] = {0,0,0,0,1,1,1};
int param0_9[] = {6,29};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {18,32,10,8,11,36,25,21,4,1};
    int param2[] = {12,38,6,6,7,40,19,30,5,1};
    int param3[] = {17,23,6,6,8,37,37,26,5,1};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}