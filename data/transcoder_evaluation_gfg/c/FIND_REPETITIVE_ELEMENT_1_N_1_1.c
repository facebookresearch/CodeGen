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
  unordered_set < int > s;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( s . find ( arr [ i ] ) != s . end ( ) ) return arr [ i ];
    s . insert ( arr [ i ] );
  }
  return - 1;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,10,14,17,30,37,39,42,49,56,68,74,85,85,92};
int param0_1[] = {62,-18,78,-32,38,90};
int param0_2[] = {0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {56,1,96,81,49,18,39,87,97};
int param0_4[] = {-98,-94,-80,-76,-60,-56,-56,-54,-48,-28,-14,-10,26,30,40,58,64,74,78,82,86,92,96,98};
int param0_5[] = {1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,1,1,1,0};
int param0_6[] = {5,7,19,20,22,29,33,35,35,36,37,40,44,49,50,53,60,60,61,62,68,68,69,72,72,81,81,83,85,85,90,91,92,97,98};
int param0_7[] = {14};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {29,29,14,91,42,70,79,75,9,86,48,47,37,48,69,81,49,37,33,23,42,45,10,33,47,39,96,45,94,48,44,4,6,73,91};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,4,7,5,16,11,26,0,18,33};
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