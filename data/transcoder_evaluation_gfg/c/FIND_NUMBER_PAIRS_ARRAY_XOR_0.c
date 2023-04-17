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

int f_gold ( int a [ ], int n ) {
  sort ( a, a + n );
  int count = 1;
  int answer = 0;
  for ( int i = 1;
  i < n;
  i ++ ) {
    if ( a [ i ] == a [ i - 1 ] ) {
      count += 1;
    }
    else {
      answer = answer + ( count * ( count - 1 ) ) / 2;
      count = 1;
    }
  }
  answer = answer + ( count * ( count - 1 ) ) / 2;
  return answer;
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,7,9,12,13,13,14,16,19,23,24,25,28,29,38,38,41,42,44,51,55,56,58,59,61,62,62,63,63,64,67,68,69,71,78,78,80,82,82,82,83,85,86,92,94,98};
int param0_1[] = {42,-20,52,34,58,62,-60,70,36,-8,-26,68,34,-92,42,94,56,84,-70,70};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {31,87,75,69,11,65,25,27};
int param0_4[] = {-92,-88,-86,-74,-72,-70,-70,-66,-62,-60,-52,-42,-42,8,14,30,36,84,88};
int param0_5[] = {1,0,0,0};
int param0_6[] = {2,8,9,12,21,23,30,31,33,34,34,41,43,45,52,53,53,55,56,61,73,73,73,74,76,79,81,81,81,90,91,92,92,97,99,99};
int param0_7[] = {84,6,-36,62,-2,-32,-82,-78,20,8,-50,-70,20,-58,94,-28,-84,-22,-44,-84,2,-68,-34,58,-64,-86,-40,-80,74,-26,12,2,-20,20,76,-14,-40,56,24,-16,-66,14,-42,0,72,82,-70};
int param0_8[] = {0,0,0,0,0,0,0,1,1};
int param0_9[] = {67,93,54,91,74,88,48,68,17,6,15,25};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,17,37,5,13,3,30,31,8,9};
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