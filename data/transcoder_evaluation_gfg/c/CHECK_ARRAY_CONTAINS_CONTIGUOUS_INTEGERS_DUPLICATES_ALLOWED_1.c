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

bool f_gold ( int arr [ ], int n ) {
  unordered_set < int > us;
  for ( int i = 0;
  i < n;
  i ++ ) us . insert ( arr [ i ] );
  int count = 1;
  int curr_ele = arr [ 0 ] - 1;
  while ( us . find ( curr_ele ) != us . end ( ) ) {
    count ++;
    curr_ele --;
  }
  curr_ele = arr [ 0 ] + 1;
  while ( us . find ( curr_ele ) != us . end ( ) ) {
    count ++;
    curr_ele ++;
  }
  return ( count == ( int ) ( len(us) ) );
}


bool f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {15,19,38,59,71};
int param0_1[] = {-20,66,-22,-56,-6,94,70,-80,24,-26,-58,-76,-20,-8,-62,18,-56,-20,42,-40,-88,-74,64,-26,-92,66,-18,-64,66,12,24,-8,78,-82,14,-76};
int param0_2[] = {0,0,1,1,1};
int param0_3[] = {40,38,17,50,16,35,34,23,3,12,97,53,75,36,3,73,99,11,70,9,23,3,11,9,64,44,62,94,55,69,44,59,57,99,69,12,27,42,14,83,53,4,4};
int param0_4[] = {-78,-36,-28,-16,-8,-4,4,4,10,14,30,30,32,32,38,46,54,72};
int param0_5[] = {1,0,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,1,1,0,1,1};
int param0_6[] = {7,32,54,70,79,88};
int param0_7[] = {-38,48,-96,-84,10,70,-28,-66,40,-26,-24,-8,28,-6,6,-14,-2,-58,-6,-14,-58,-74,20,32,98,-24,-10,42,-4,-96,-56,-40,74,-98,-86,-94,12,80,10,-54,-44};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1};
int param0_9[] = {49,87,18,19,56,25,64,94,43,97,74,79,13,36,72,46,10,84,2,11,41,87,55,38,89,92,65,57,62,16};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {3,26,4,26,16,38,5,30,12,21};
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