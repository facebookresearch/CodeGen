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

int f_gold ( int ar [ ], int ar_size ) {
  int res = 0;
  for ( int i = 0;
  i < ar_size;
  i ++ ) res = res ^ ar [ i ];
  return res;
}


int f_filled ( int ar [ ], int ar_size ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,1,7,10,12,19,20,22,23,25,27,32,33,39,43,44,45,46,47,47,48,49,50,51,55,58,68,69,73,76,77,79,81,84,92,95,99};
int param0_1[] = {-12,-40,-68};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {86,56,98,58,7,40,84,45,69,77,36,50,72,99,95};
int param0_4[] = {-90,-68,-66,-66,-58,-54,-52,-48,-40,-30,-26,-24,-20,-14,-10,-8,-6,-6,-6,18,30,34,36,42,50,56,64,68,70,74,92,92,98};
int param0_5[] = {0,0,1,0,0,0,1,1,1,0,1,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,0,1,1,1,1,0,0,1,0,0,0};
int param0_6[] = {3,21,47,51,78,84,84,85,86,99};
int param0_7[] = {-26,-72,44,62,-22,22,28,-28,32,-72,72,96,92,-52,-2,-22,-76,-88,-74,-8,-30,54,0,-62,14,-92,-58,72,40,46,96,86,-54,-92,46,92,20,-96,-92,-70,-94,78,-92,-54,-90};
int param0_8[] = {0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {69,1,12,81,78,18,81,47,49,19,99,40,52,47,71,69,80,72,66,84,72,6,98,89,3,87,81,85,37,14,5,36,26,74};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {36,2,21,9,26,27,9,33,9,22};
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