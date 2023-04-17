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
  return * max_element ( arr, arr + n );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {10,12,14,16,17,17,20,24,26,28,37,38,41,45,49,50,59,61,63,65,65,66,69,70,70,73,73,74,81,81,83,87,94,97};
int param0_1[] = {-56,38,-22,84,-60,2,68,-78,62,-98,24,26,48,62,-80,-14,-84,12,-54,-12,-20,-82,10,-34,-50,-72,78,16,30,-76,72,34,6,52,44,18,-38,48,-14};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {92,5,40,65,86,51,14,29,66,6,62,92,29,13,88,54,15,60,45,2,51,9,33,51,31,11,62,61,77,38,11,4,27,54,72,64,85,46,24,44,39,73,82,85};
int param0_4[] = {-92,-90,-84,-80,-80,-76,-70,-70,-48,-44,-38,-28,-14,-14,-12,-2,2,4,6,10,16,16,20,22,24,26,50,52,56,56,58,58,74,80,82,84,86};
int param0_5[] = {0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,1,1,0,0,1,0,1,1,0,1,0,0,1,1,1,0,0,0,0,0,1,0};
int param0_6[] = {5,19,20,26,31,32,34,37,39,40,46,46,50,53,58,58,59,65,72,72,75,76,77,78,81,83,83,95,98,99};
int param0_7[] = {32,-84,-84,86,-24,36,-12,82,48,-12,82,-76,84,-20,-12,-18,46,-74,-14,-86};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {95,73,74,14,73,74,19,93,34,53,85,75,80,15,36,57,15,98,51,37,8,9,62,71,28,24,37,53,84,76,22,48,15,19,43,88,58,38,63,68,27,22,37,76,59,66,22};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {17,25,11,40,33,29,28,14,33,34};
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