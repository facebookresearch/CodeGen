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

int f_gold ( int n, int k, int a [ ] ) {
  sort ( a, a + n, greater < int > ( ) );
  int f_gold = 0;
  for ( int i = 0;
  i < n;
  i += k ) f_gold += ( 2 * a [ i ] );
  return f_gold;
}


int f_filled ( int n, int k, int a [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {17,2,0,16,31,28,9,32,17,19};
    int param1[] = {15,2,0,27,23,33,10,26,22,15};
    int param2_0[] = {1,4,8,18,24,34,38,38,39,39,41,53,56,57,63,72,73,77,79,99};
int param2_1[] = {-8,70,-90,-74};
int param2_2[] = {0};
int param2_3[] = {3,66,11,21,82,75,19,39,1,55,7,26,10,87,11,94,91,76,21,91,83,18,44,29,47,84,6,10,83,74,26,50};
int param2_4[] = {-96,-84,-80,-72,-60,-60,-58,-58,-52,-46,-36,-34,-32,-26,-22,-22,-20,-18,-14,-14,-6,-2,-2,0,2,4,18,22,24,38,42,46,50,58,72,78,82,84,90,96,96,96};
int param2_5[] = {0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,1,0,0,0,1,1,1,0,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,0,0,1,0,1};
int param2_6[] = {8,13,17,19,24,33,43,54,63,74,79,83};
int param2_7[] = {0,52,20,40,-2,74,12,10,-56,68,-52,36,8,34,82,-64,-78,-22,-24,74,-54,62,-70,-76,-80,8,-24,84,-84,-74,-90,6,22,58,62,24,-74,50,92};
int param2_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param2_9[] = {97,4,69,27,23,97,26,67,72,26,15,67,66,73,27,68,27,60,53,80,20,59,96,9,94,66,5,32};
int *param2[10] = {param2_0,param2_1,param2_2,param2_3,param2_4,param2_5,param2_6,param2_7,param2_8,param2_9};
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