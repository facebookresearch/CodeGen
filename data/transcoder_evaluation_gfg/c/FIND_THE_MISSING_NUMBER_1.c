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
  int i, total = 1;
  for ( i = 2;
  i <= ( n + 1 );
  i ++ ) {
    total += i;
    total -= a [ i - 2 ];
  }
  return total;
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {13,27,46,59,62,82,92};
int param0_1[] = {22,86,-64,-20,-56,-16,86,42,72,-90,10,42,56,8,50,24,-34,0,-78,64,18,20,-84,-22,90,-20,86,26,-54,0,90,-48,4,88,18,-64,-22,-74,48,-36,-86,-24,88,-64,68,62,92};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {55,89,56,85,26,4,91,91,3,77,63,59,76,90,1,94,44,70,8,54,3,91,29,95,28,75,20};
int param0_4[] = {-94,-84,-80,-78,-66,-62,-54,-52,-26,-8,-8,-6,4,4,8,14,26,58,60,62,62,76,78,86,92};
int param0_5[] = {1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0};
int param0_6[] = {1,2,7,7,9,14,23,29,31,31,35,35,38,41,44,49,49,50,51,54,55,56,57,63,67,69,73,79,79,80,86,88,93};
int param0_7[] = {78,-48,16,22,-16,34,56,-20,-62,-82,-74,-40,20,-24,-46,64,66,-76,58,-84,96,76,86,-32,46};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {73,76,25,59,40,85,90,38,13,97,93,99,45,7};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {6,38,15,22,18,25,24,12,29,12};
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