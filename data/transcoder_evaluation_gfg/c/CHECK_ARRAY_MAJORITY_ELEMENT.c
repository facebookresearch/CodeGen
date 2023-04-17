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

bool f_gold ( int a [ ], int n ) {
  unordered_map < int, int > mp;
  for ( int i = 0;
  i < n;
  i ++ ) mp [ a [ i ] ] ++;
  for ( auto x : mp ) if ( x . second >= n / 2 ) return true;
  return false;
}


bool f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,14,20,26,32,33,34,35,35,49,51,55,57,64,64,68,70,72,74,77,78,78,78,80,91,91,94};
int param0_1[] = {-14,-98,-36,68,-20,18,16,-50,66,98,12,-2,-68};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {29,96,94,67,87,65,27,21,60,49,73,85,9,17,72,3,73,69,95,3,30,88,54,94,40};
int param0_4[] = {-86,-80,-76,-76,-74,-62,-62,-56,-48,-36,-28,-22,-18,-18,-18,-16,-14,-12,-6,-2,10,14,18,24,32,32,40,40,40,42,46,48,50,56,56,56,68,76,84,94,96,96};
int param0_5[] = {0,1,1,1,0};
int param0_6[] = {5,8,9,12,14,16,19,29,32,32,37,38,38,39,40,41,43,45,47,51,53,58,58,63,64,65,69,83,84,86,92,93,96,98};
int param0_7[] = {-68,-50,-20,22,90,86,4,60,-88,82,-4,-54,36,-44,86};
int param0_8[] = {0,0,0,0,1,1,1,1};
int param0_9[] = {85,64,25,64,46,35,31,45,93,81,49,33,96,48,37};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {15,11,22,15,23,3,17,13,6,13};
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