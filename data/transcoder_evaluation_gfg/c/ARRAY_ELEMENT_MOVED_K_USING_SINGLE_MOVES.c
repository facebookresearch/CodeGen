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

int f_gold ( int a [ ], int n, int k ) {
  if ( k >= n - 1 ) return n;
  int best = 0, times = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( a [ i ] > best ) {
      best = a [ i ];
      if ( i ) times = 1;
    }
    else times += 1;
    if ( times >= k ) return best;
  }
  return best;
}


int f_filled ( int a [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,5,5,9,10,10,11,14,23,27,31,32,33,33,33,37,39,41,41,42,42,43,47,60,61,68,73,73,73,78,80,80,82,83,86,87,89,92,94,98};
int param0_1[] = {80,-58,64,48,-16,60,-50,-52,62,-86,-96,52,26,-30,14};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1};
int param0_3[] = {90,23,43,42,7,71,79};
int param0_4[] = {-96,-96,-90,-84,-68,-64,-56,-56,-50,-50,-48,-46,-28,-18,0,0,6,32,32,34,42,42,46,50,50,52,64,64,70,76,84,88};
int param0_5[] = {1,1,1};
int param0_6[] = {2,9,15,19,26,29,42,45,46,47,55,60,60,61,62,64,68,69,74,79,96};
int param0_7[] = {-32,12,80,42,80,8,58,-76,-42,-98,22,-90,-16,-4,-62,-32,28,12,78,-52,-84,78,88,-76,-52,68,-34,-16,-4,2,-78,-94,-22,34,6,-62,72};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {52,19};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,14,7,4,28,1,14,26,26,1};
    int param2[] = {37,13,6,4,21,2,17,31,14,1};
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