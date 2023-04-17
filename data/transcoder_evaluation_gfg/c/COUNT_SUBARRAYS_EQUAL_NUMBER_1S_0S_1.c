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
  map < int, int > mp;
  int sum = 0;
  int count = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] == 0 ) arr [ i ] = - 1;
    sum += arr [ i ];
    if ( sum == 0 ) count ++;
    if ( mp [ sum ] ) count += mp [ sum ];
    if ( mp [ sum ] == 0 ) mp [ sum ] = 1;
    else mp [ sum ] ++;
  }
  return count;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,6,6,9,9,9,16,18,19,20,21,22,23,26,26,28,39,40,41,43,43,44,44,45,51,51,55,59,60,62,67,67,68,69,70,71,71,72,82,84,88,88,89,89,91,92,92};
int param0_1[] = {-44,74,-52,-96,46,92,54,56,-38,88,40,34,-72,8,58,-14,36,94,34,-90,-42,80,-12,-42,-6,78,-98,34,-88,0,-76,90,40,64,26,18,-84,72,80};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {60,48,42,95,30,22,80,15,62,38,63,42,39,28,69,71,30,48,67,9,33,74,95,95,72,35,9};
int param0_4[] = {-96,-94,-94,-86,-66,-66,-62,-58,-36,-36,-22,-18,-10,2,4,6,10,16,20,24,26,28,28,28,40,42,44,58,76,78,78,80,90,92};
int param0_5[] = {0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,0,1,0,1,1,1,0,1,1};
int param0_6[] = {4,5,5,6,7,11,16,16,17,18,19,20,21,22,23,25,26,27,29,31,34,36,37,40,41,45,45,55,65,69,70,71,71,71,73,73,76,79,80,85,85,88,90,97,98,98,99,99};
int param0_7[] = {34,-20,38,-94,2,32,-26,90,94,-36,-94,6,-24,12,4,60,68,64,-60,-72,-54,-10,-64,-48,-88,60,48,64,0,-26,26,74,32,-92,4,84,6,-16,30,-56,-28,-86,-68};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {4,99,97,63,65,57,69,39,29,91,68,25,84,82,84,89,59,18,77,29,57,40,78,35,23,91,26,71,19,99,12,91,49,71,49,77,67};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {44,37,32,18,24,28,31,37,19,31};
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