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

int f_gold ( int arr [ ], int left, int right ) {
  if ( left <= right ) {
    int mid = ( left + right ) / 2;
    if ( arr [ mid - 1 ] < arr [ mid ] && arr [ mid ] > arr [ mid + 1 ] ) return mid;
    if ( arr [ mid ] < arr [ mid + 1 ] ) return f_gold ( arr, mid + 1, right );
    else return f_gold ( arr, left, mid - 1 );
  }
  return - 1;
}


int f_filled ( int arr [ ], int left, int right ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,10,33,44,50,50,53,58,64,68,76,83,90,98};
int param0_1[] = {-96,-20,20,4,-76,-96,-44,64,-30,-12,48,-84,-16,-28,84};
int param0_2[] = {0,0,0,0,1,1};
int param0_3[] = {46,24,32,6,23,66,21,78,11,97,35,51,3,56,14,5,43,19,67,15,87,28,28,97,52,91,70,72,97,73,67,48,68,33,50,34,78,75};
int param0_4[] = {-88,-6,38,44,44,46,50};
int param0_5[] = {1};
int param0_6[] = {7,7,10,13,15,17,18,25,26,30,40,41,42,45,47,47,55,61,62,62,63,64,66,67,69,79,79,82,82,88,91,94,97};
int param0_7[] = {-18,-4,-66,-38,-68,-80,40,62,0,92,86,62,8,-22,72,-12,18,-72,-86,-84,70,-78,46,72,72,46,42,70,12,20,46,46};
int param0_8[] = {0,0,0,0,0,1,1,1,1,1};
int param0_9[] = {11,36,74,82,70,8,7,78,91,59,86,36};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {8,11,4,30,6,0,26,22,6,11};
    int param2[] = {9,14,4,28,6,0,32,25,7,7};
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