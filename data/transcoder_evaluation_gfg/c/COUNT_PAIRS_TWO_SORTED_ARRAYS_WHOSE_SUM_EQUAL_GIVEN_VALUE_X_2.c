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

int f_gold ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {
  int count = 0;
  int l = 0, r = n - 1;
  while ( l < m && r >= 0 ) {
    if ( ( arr1 [ l ] + arr2 [ r ] ) == x ) {
      l ++;
      r --;
      count ++;
    }
    else if ( ( arr1 [ l ] + arr2 [ r ] ) < x ) l ++;
    else r --;
  }
  return count;
}


int f_filled ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {5,5,7,10,14,14,17,21,32,34,37,40,40,40,46,46,50,50,51,55,57,62,65,67,67,69,70,70,72,73,76,77,77,78,84,85,85,86,87,88,88,89,89,90,93,99};
int param0_1[] = {-84,52,-34,96,16,92,-64,-74};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {60,92,42,83,55,76,29,62};
int param0_4[] = {-94,-94,-58,-40,-40,-26,-24,-22,-22,-22,-2,0,4,8,12,16,16,18,22,32,42,44,50,58,64,78,80,90};
int param0_5[] = {0,0,1,1,1,0,0,1,1,1};
int param0_6[] = {1,5,7,7,7,14,15,16,17,18,18,19,20,25,27,31,36,42,47,51,56,56,56,58,58,59,63,63,63,65,66,67,76,83,93,94,97};
int param0_7[] = {78,-74,52,56,-8,92,14,56,-72,-92,32,-94,-26,-8,-66,72,-24,36,-84,-4,-68,14,78,40,-82,-10,16,56,6,-16,30,24,-32};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {17,50,65,4,19,10,45,70,76,81,28,97,55,70,38,2,40,67,36,33,6,85,25};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {2,5,8,8,10,12,13,15,17,18,20,20,21,27,28,31,34,37,40,46,48,52,53,54,54,58,59,60,66,68,68,69,70,71,72,73,77,77,80,84,84,92,92,95,97,97};
int param1_1[] = {-22,26,-12,-54,66,86,38,76};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {71,2,74,42,80,71,26,76};
int param1_4[] = {-86,-84,-78,-76,-72,-70,-62,-58,-54,-54,-50,-46,-44,-40,-30,-28,-16,-10,10,36,36,48,70,84,84,90,94,98};
int param1_5[] = {1,1,1,0,1,1,0,0,0,0};
int param1_6[] = {2,3,7,8,9,10,17,18,21,28,29,29,33,35,46,47,47,49,49,49,53,56,58,59,59,60,65,67,70,78,81,85,85,87,90,92,96};
int param1_7[] = {-74,22,-14,-2,36,86,-70,-20,-76,-84,-40,-36,42,22,-60,-94,-18,8,-14,-42,-68,62,-60,2,40,-66,68,96,70,98,-38,-74,-92};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {78,92,65,23,7,94,18,4,2,53,31,58,98,18,46,16,17,92,80,92,43,70,50};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {28,6,37,4,17,5,28,16,25,16};
    int param3[] = {29,5,26,7,27,8,34,30,33,22};
    int param4[] = {23,7,42,7,17,9,31,24,33,22};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i],param4[i]) == f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}