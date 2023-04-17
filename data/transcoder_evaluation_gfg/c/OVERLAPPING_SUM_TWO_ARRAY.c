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

int f_gold ( int A [ ], int B [ ], int n ) {
  unordered_map < int, int > hash;
  for ( int i = 0;
  i < n;
  i ++ ) {
    hash [ A [ i ] ] ++;
    hash [ B [ i ] ] ++;
  }
  int sum = 0;
  for ( auto x : hash ) if ( x . second == 1 ) sum += x . first;
  return sum;
}


int f_filled ( int A [ ], int B [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {13,31,63,75,90,92,94,98};
int param0_1[] = {-20};
int param0_2[] = {0,0,0,1,1,1};
int param0_3[] = {47,71,9,64,66,99,7,44,75,84,88,49,95,56,3,90,73,2};
int param0_4[] = {-76,-72,-70,-60,-44,-38,-38,-26,-16,-10,-4,-2,4,18,30,38,54,56,64,66,68,70,72,82,84};
int param0_5[] = {0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,1};
int param0_6[] = {3,4,4,6,11,13,14,18,30,30,34,39,40,45,46,50,51,56,60,61,66,68,72,79,79,82,83,87,89,91,91,92,92,93,94};
int param0_7[] = {-14,12,98,34,58,-70,6,52,-50,96,-6};
int param0_8[] = {0,0,0,1,1,1,1,1};
int param0_9[] = {34,85,60,55,38,69,21,43,39,83,10,71,73,15,94,59,83,39,29,31,61,9,11,27,71,90,18,11,4,3,97,43,58,50,35,42,70,33,98,61,32,32,12,29};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {14,16,20,28,32,55,56,56};
int param1_1[] = {60};
int param1_2[] = {0,0,1,1,1,1};
int param1_3[] = {8,27,21,40,99,8,52,37,72,50,61,82,88,71,27,84,38,35};
int param1_4[] = {-80,-64,-50,-44,-34,-26,-24,-22,-6,-2,2,2,12,24,34,44,48,50,52,70,76,82,86,94,96};
int param1_5[] = {0,0,0,1,1,0,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,0,1,1,0,0};
int param1_6[] = {3,7,15,15,21,23,30,32,35,38,38,41,41,41,44,45,49,52,60,60,63,66,66,70,72,74,74,75,79,81,87,88,89,93,96};
int param1_7[] = {50,-22,-82,40,-80,30,-58,-64,60,6,-28};
int param1_8[] = {0,0,1,1,1,1,1,1};
int param1_9[] = {74,10,95,67,59,17,32,87,87,12,22,45,50,35,25,51,10,86,75,4,74,43,92,63,60,28,32,72,66,61,43,48,20,89,55,59,22,85,73,43,7,65,53,98};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {6,0,5,16,16,17,22,9,5,34};
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