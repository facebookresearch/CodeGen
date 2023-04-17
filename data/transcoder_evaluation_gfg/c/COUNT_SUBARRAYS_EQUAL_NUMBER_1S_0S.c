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
  unordered_map < int, int > um;
  int curr_sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    curr_sum += ( arr [ i ] == 0 ) ? - 1 : arr [ i ];
    um [ curr_sum ] ++;
  }
  int count = 0;
  for ( auto itr = um . begin ( );
  itr != um . end ( );
  itr ++ ) {
    if ( itr -> second > 1 ) count += ( ( itr -> second * ( itr -> second - 1 ) ) / 2 );
  }
  if ( um . find ( 0 ) != um . end ( ) ) count += um [ 0 ];
  return count;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,12,18,19,19,20,20,21,25,29,38,54,54,71,72,72,74,75,77,78,80,80,81,84,97,97};
int param0_1[] = {10,70,24,-38,32,-68,88,-28,-24,-70,-64,50,-30,64,54,-6,18,-30,-30,-62,-10,94,-54,-22,-88,96,22,26,-92,-40,-76,46,36,30,24,-52,0};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {66,50,17,15,86,84,87,24,81,23,71,31,13,72,58,19,29,28,40,14,48,48,81,4,52,88,54,56,10,12,58,55,7,66,15,73,22,2,20,27,57,56,56,31,9,55};
int param0_4[] = {-98,-62,-60,16,78,82};
int param0_5[] = {1,0,1};
int param0_6[] = {2,31,34,64};
int param0_7[] = {-70,90,-10,-64,-76,-74,-12,-44,-48,-54,76,-78,8,0,0,78,-28,6,98,-84,60,60,2,48,-96,-28,-78,-76,-56,-26,-60,50,44,34,-90,80,-30,-98,62,36,-46,-72};
int param0_8[] = {1,1,1};
int param0_9[] = {37,70,80,61,86,10,17,98,54,89,87,84,11,55,3,52,4,90,98,31,20,62,71,58,58,6,92,5,99,99,72,40,82,54,23,19,85,91,62,98,62,72,93,74};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,24,11,40,5,2,2,25,1,27};
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