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

int f_gold ( int a [ ], int n ) {
  sort ( a, a + n, greater < int > ( ) );
  int sum = 0;
  bool flag = false;
  int len;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( ( a [ i ] == a [ i + 1 ] || a [ i ] - a [ i + 1 ] == 1 ) && ( ! flag ) ) {
      flag = true;
      len = a [ i + 1 ];
      i ++;
    }
    else if ( ( a [ i ] == a [ i + 1 ] || a [ i ] - a [ i + 1 ] == 1 ) && ( flag ) ) {
      sum = sum + a [ i + 1 ] * len;
      flag = false;
      i ++;
    }
  }
  return sum;
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,11,14,15,22,33,64,81,82,95};
int param0_1[] = {-42,2,84,18,60,84,-12,64,46,60,40,52,-62,-48,60,64,76,50,88,92,42,-82,44,-98,-4};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {50,6,43,82,99,1,20,7,52,18,52,18,45,75,58,48,49,70,69,19,49,35,45,14,52,33,9,31,86,70,77,70,91,56,76,69,68,31,21,72,78,83,76,1};
int param0_4[] = {-92,-76,-70,-62,-46,-36,-36,-32,-26,-8,-2,4,8,14,14,26,34,48,58,68,74,78,84,86};
int param0_5[] = {1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0,0,1,1,1,0,1};
int param0_6[] = {19,20,23,25,26,26,34,43,43,46,49,56,59,59,68,73,93,93};
int param0_7[] = {-82,-80,-68,-98,34,96,-72,22,-30,-92,74,-68,48,92,-26,-32,-8,72,84,-10,60,74,-98,78,-32,84,64,-56,94,24,72,40,-44,2,-18,34};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {40,32,38,69,56,28,79,29,63,72,4,46,25,32,12,83,59,59,32,1,56,15,62,3,6,85,29,45,88,84,52,62,89,33,48,23,85,54,46,78,7,12};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {9,22,22,32,21,38,10,33,24,26};
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