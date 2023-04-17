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

int f_gold ( int n, int a [ ] ) {
  return n * ( a [ 0 ] * a [ 0 ] - a [ 2 * n - 1 ] * a [ 2 * n - 1 ] ) / ( 2 * n - 1 );
}


int f_filled ( int n, int a [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {6,23,15,25,21,26,23,27,15,18};
    int param1_0[] = {2,3,5,12,17,25,73,88};
int param1_1[] = {60,-90,-84,-46,-12,0,-92,38,-14,80,88,-70,56,58,56,-68,-56,70,-34,-22,-40,-48,-56,46,-26,-50,-68,40};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {81,93,12,83,37,63,60,89,40,32,78,54,63,76,76,77,50,2,53,82,50,46,5,49,37,67,77,16,95,84,6,66,1,16,10};
int param1_4[] = {-98,-92,-90,-82,-68,-62,-30,-28,-10,-8,-2,-2,-2,8,16,20,28,30,38,42,50,52,62,82,86,86,96,96};
int param1_5[] = {0,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,1,0,0,1,1,0,1,1,0,1,1,0};
int param1_6[] = {5,9,15,18,18,22,22,26,27,34,52,55,59,59,68,71,71,73,78,81,82,85,86,91,97,98};
int param1_7[] = {-30,28,74,92,-54,-52,-66,-40,-60,-70,-68,68,-36,-36,-52,-90,82,34,-96,90,-96,56,84,24,-78,-50,32,-96,82,8,54,-44,88,-70,80,26,72,-98,16,-32,-86,-20,24,88,-50};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {99,99,24,86,84,17,41,87,68,34,17,70,23,84,74,4,78,84,83,48,75,9,73,99,81,84,54,2,23,11,8,61,30};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
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