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
  int min_xor = INT_MAX;
  for ( int i = 0;
  i < n;
  i ++ ) for ( int j = i + 1;
  j < n;
  j ++ ) min_xor = min ( min_xor, arr [ i ] ^ arr [ j ] );
  return min_xor;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,5,7,10,10,11,14,19,21,24,27,27,27,28,28,28,33,34,41,42,43,48,52,53,53,59,62,64,66,71,77,78,78,79,80,82,90,97,99,99};
int param0_1[] = {-68,-58,52,88,90,66,-66,-84,-70,-64,56,42,94,-10,0,80,8,28,-94,36,90,56,56,80,-94,50,90,-28,-22,-2,-96,74,-16,-14};
int param0_2[] = {0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {57,63,11,73,60,73,25,65,39,48,31,17,23,94,10,97,42,45,83,75,97,96};
int param0_4[] = {-92,-92,-90,-88,-84,-82,-66,-64,-64,-62,-44,-42,-40,-28,-22,-12,-4,-2,0,4,16,22,28,34,54,60,72,74,78,86,94};
int param0_5[] = {1,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,1,1,1,1,1,0,0};
int param0_6[] = {2,2,6,13,16,16,17,19,19,20,22,25,27,29,34,34,34,36,38,39,42,49,49,53,59,59,71,77,79,82,83,83,84,84,86,86,87,88,93,96};
int param0_7[] = {-14,20,36,12,-54,-50,92,-28,44,-46,6,96,82,70,-20,24,-96,-14,46,-28,-46,-28,22,-82,36,-94,-48,-92,96,74,14};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {50,48,94,64,60,48,79,75,77,62,33,42,22,78,32,99,27,23,76,51,34,54,70,12,19,17,13,82,96,70,4,12,5,11,23,23,18,93,38,69};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {34,17,9,21,18,36,36,20,39,30};
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