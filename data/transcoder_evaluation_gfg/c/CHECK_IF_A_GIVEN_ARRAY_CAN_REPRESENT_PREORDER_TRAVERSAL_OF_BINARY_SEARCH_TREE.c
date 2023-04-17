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

bool f_gold ( int pre [ ], int n ) {
  stack < int > s;
  int root = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( pre [ i ] < root ) return false;
    while ( ! s . empty ( ) && s . top ( ) < pre [ i ] ) {
      root = s . top ( );
      s . pop ( );
    }
    s . push ( pre [ i ] );
  }
  return true;
}


bool f_filled ( int pre [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,9,21,25,33,36,44,48,55,55,56,58,66,66,66,66,78,92,96,97};
int param0_1[] = {-16,80,70,72,-86,-28,42,28,-28,56,-32,40,-78,32,22,-52,-58};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {10,85,45,52,98,9,59,58,61,91,4,90,43,48,47};
int param0_4[] = {-92,-90,-88,-50,-48,-48,-44,-42,-40,-34,-28,-26,-26,-24,-8,-6,4,8,12,20,32,36,38,40,46,52,58,88,92};
int param0_5[] = {1,0,1,1,1};
int param0_6[] = {1,2,3,4,14,16,17,18,19,19,21,21,22,25,25,28,29,33,34,40,41,42,44,50,52,58,61,62,67,70,74,74,75,75,76,77,77,77,81,83,87,90,90,90,96,98,99,99};
int param0_7[] = {-98,40,84,-8,42,-52,2,16,-68,-28,-54,88,8,-4,-98,-40,-32,-64,54,32,-76,-10,-48,-88,80,32,-2,-94,-26,-54,30,-56};
int param0_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {9,35,62,78,55,29,55,36,77,89,73,31,53,94,22,23,87,96,7,15,71,61,25,61,99,34,1,87,21,14,58,69,61,49,54,7,89,52,78,97,11,78,27,37,56,19,20,21};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {18,16,35,8,17,2,30,26,17,34};
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