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
  int max = * max_element ( arr, arr + n );
  int min = * min_element ( arr, arr + n );
  int m = max - min + 1;
  if ( m > n ) return false;
  bool visited [ m ];
  memset ( visited, false, sizeof ( visited ) );
  for ( int i = 0;
  i < n;
  i ++ ) visited [ arr [ i ] - min ] = true;
  for ( int i = 0;
  i < m;
  i ++ ) if ( visited [ i ] == false ) return false;
  return true;
}


bool f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,4,19,25,65,72,75,83,90,92};
int param0_1[] = {46,2,28,-44,74,-36,-8,30,-96,60,52,-58,16,-38,78,38,-28,16,26,-42,48,40,6,72};
int param0_2[] = {0,1,1,1};
int param0_3[] = {50,21,9,29,86,2,82,49,34,18,77,83,44,67,85,58,15,85,22,3,39,67,42,37,6,35,18,57,41,32,39,30,41,68,84,36,64,36};
int param0_4[] = {-92,-82,-80,-78,-66,-66,-62,-58,-54,-52,-48,-30,-26,-22,-20,-20,-18,-14,-2,12,20,24,26,26,28,28,32,36,42,48,50,52,56,64,70,72,72,80,82,84,86,92};
int param0_5[] = {1,0,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0,0,0,0};
int param0_6[] = {18,19,21,23,30,33,38,40,45,56,63,68,93,96};
int param0_7[] = {20,-90,-42,48,18,-46,82,-12,-88,82,62,24,20,64,-68,-34,-38,8,-54,-20,-92,34,-90,78,18,8,-6,10,98,-24,72,-92,76,-22,12,-44,2,68,-72,42,34,20,-48};
int param0_8[] = {0,0,0,0,0,1,1,1,1};
int param0_9[] = {81,25,50,48,35,38,49,21,47,94,94,55,23,45,92,23,93,33,64,9,90,64,81,17,2,73,8,7,35,36,72};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {8,14,2,23,26,43,8,34,8,27};
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