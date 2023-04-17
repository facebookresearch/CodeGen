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

int f_gold ( int arr [ ], int l, int h, int key ) {
  if ( l > h ) return - 1;
  int mid = ( l + h ) / 2;
  if ( arr [ mid ] == key ) return mid;
  if ( arr [ l ] <= arr [ mid ] ) {
    if ( key >= arr [ l ] && key <= arr [ mid ] ) return f_gold ( arr, l, mid - 1, key );
    return f_gold ( arr, mid + 1, h, key );
  }
  if ( key >= arr [ mid ] && key <= arr [ h ] ) return f_gold ( arr, mid + 1, h, key );
  return f_gold ( arr, l, mid - 1, key );
}


int f_filled ( int arr [ ], int l, int h, int key ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {20};
int param0_1[] = {40,50,55,67,70,4,5,6,7};
int param0_2[] = {14,41,38,67,99,11,96,52,4,29,22,57,3,45,14,76,70,38,93,5,74,50,18,17,20,34,51,69,86,73};
int param0_3[] = {-90,-88,-88,-82,-62,-44,-38,-38,-36,-34,-34,-32,-30,-28,-28,-26,-24,-20,-16,-16,-16,-6,-6,2,6,8,10,14,18,18,46,50,50,54,56,58,58,60,62,70,70,74,82,84,88,94,96};
int param0_4[] = {1,1,1,1,0,0,1,1,1,1,1,1,1,0};
int param0_5[] = {4,7,9,10,10,11,14,16,17,21,25,27,31,34,34,34,38,41,42,42,52,56,56,58,60,66,67,68,68,70,72,74,76,82,88,88,88,89,91,93,94,95,95};
int param0_6[] = {92,60,-60,64,18,70,56,34,58,14,28,-72,-22,-74,-46,-28,64,88,18,-50,-14,-20,64,6,-4,-98,60,98,84,-58,-98,66,80,68,-42,-58,82,90,-72,34,34,80,88,-64,66,-20,-26};
int param0_7[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_8[] = {33,18,98,47,76,58,29,68,62,78,12,95,20,88,39,12,43,45,5,45,96,64,38,28,70,25,65,79,39};
int *param0[9] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8};
    int param1[] = {0,0,0,0,0,0,0,0,0,0};
    int param2[] = {8,4,9,16,24,10,23,25,40,16};
    int param3[] = {3,40,67,15,24,10,39,25,29,28};
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