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
  int difference = 0;
  int ans = 0;
  int hash_positive [ n + 1 ], hash_negative [ n + 1 ];
  fill_n ( hash_positive, n + 1, 0 );
  fill_n ( hash_negative, n + 1, 0 );
  hash_positive [ 0 ] = 1;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] & 1 == 1 ) difference ++;
    else difference --;
    if ( difference < 0 ) {
      ans += hash_negative [ - difference ];
      hash_negative [ - difference ] ++;
    }
    else {
      ans += hash_positive [ difference ];
      hash_positive [ difference ] ++;
    }
  }
  return ans;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,8,12,13,14,19,20,22,28,30,31,31,32,34,34,39,39,43,45,46,47,62,63,63,65,66,69,69,71,76,79,82,83,88,89,92,93,95,97,97};
int param0_1[] = {20,-98,-44,-82,28,20,-76,-16,42,0,-88,74,56,6,-68,-30,28,88,58,-78,46,2};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {44,4,29,83,28,75,58,89,40,38,29,45,21,87,97,42,95,20,48,38,15,67,23,81,50,53,64,67,30,13,52,56,87,10,80,38,31,19};
int param0_4[] = {-94,-94,-94,-90,-88,-86,-86,-82,-78,-76,-74,-68,-64,-62,-62,-60,-52,-48,-48,-46,-44,-44,-32,-28,-22,-12,-12,-8,-8,-4,4,6,10,14,28,40,42,52,56,60,60,60,64,68,70,82,82,84,96};
int param0_5[] = {1,0,0,0,1,0,1,1,1,0,0,0,1,0,0,1,1,1,0,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1};
int param0_6[] = {6,16,21,26,34,35,44,46,46,86};
int param0_7[] = {86,12,80,46,-12,6};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {71,94,91,19,85,5,87,96,66,17,95,5,32,17,93,48,46,24};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {26,15,24,23,48,27,7,4,15,12};
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