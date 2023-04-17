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

int f_gold ( int start, int end, int arr [ ] ) {
  unordered_map < int, int > frequency;
  for ( int i = start;
  i <= end;
  i ++ ) frequency [ arr [ i ] ] ++;
  int count = 0;
  for ( auto x : frequency ) if ( x . first == x . second ) count ++;
  return count;
}


int f_filled ( int start, int end, int arr [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {0,1,3,10,2,0,14,29,31,21};
    int param1[] = {31,25,4,15,3,6,18,33,19,32};
    int param2_0[] = {1,2,2,3,3,3,12,13,18,18,26,28,29,36,37,39,40,49,55,57,63,69,69,73,85,86,87,87,89,89,90,91,92,93,93,93,95,99};
int param2_1[] = {24,-62,2,1,94,56,-22,-70,-22,-34,-92,-18,56,2,60,38,-88,16,-28,30,-30,58,-80,94,6,56};
int param2_2[] = {0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_3[] = {84,13,81,40,87,82,50,30,90,80,81,70,14,54,72,93,78,27,61};
int param2_4[] = {-20,20,34,60,90};
int param2_5[] = {1,0,0,0,0,0,0,0,0,0};
int param2_6[] = {11,18,18,19,25,30,42,42,56,58,63,66,67,68,69,75,78,83,83};
int param2_7[] = {-24,-82,24,-84,94,2,-30,86,58,-56,-96,60,-38,76,94,74,-98,-84,-38,46,4,-84,-90,-28,-50,46,16,28,-14,-82,-64,42,64,-2,-40,96,60,2,-86,32,38,-66};
int param2_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_9[] = {2,91,42,85,97,92,24,39,63,89,31,59,51,89,72,62,26,92,75,4,6,13,20,95,22,30,52,60,37,27,49,15,67,26};
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