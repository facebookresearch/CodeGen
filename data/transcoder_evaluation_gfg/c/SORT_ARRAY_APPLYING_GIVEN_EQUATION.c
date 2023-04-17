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

void f_gold ( int arr [ ], int n, int A, int B, int C ) {
  for ( int i = 0;
  i < n;
  i ++ ) arr [ i ] = A * arr [ i ] * arr [ i ] + B * arr [ i ] + C;
  int index, maximum = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( maximum < arr [ i ] ) {
      index = i;
      maximum = arr [ i ];
    }
  }
  int i = 0, j = n - 1;
  int new_arr [ n ], k = 0;
  while ( i < index && j > index ) {
    if ( arr [ i ] < arr [ j ] ) new_arr [ k ++ ] = arr [ i ++ ];
    else new_arr [ k ++ ] = arr [ j -- ];
  }
  while ( i < index ) new_arr [ k ++ ] = arr [ i ++ ];
  while ( j > index ) new_arr [ k ++ ] = arr [ j -- ];
  new_arr [ n - 1 ] = maximum;
  for ( int i = 0;
  i < n;
  i ++ ) arr [ i ] = new_arr [ i ];
}


void f_filled ( int arr [ ], int n, int A, int B, int C ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,30,49,65,78,85,85,92};
int param0_1[] = {-48,89,-60,66,71,-37,47,-50,61,41,-22,-3,90,-57,77,-64,22,8,-90,-5,-94,-43,29,-29,86,-79,-8,27,-20,-44,16};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {87,70,77,87,73,81,66,19,83,7,63,42,42,59,20,73,17,27,47,2,63,62,19,17,69,39,82,71,81,39,36,40,45,4,25,69,30,76,68,88,29,73,68,51,24,14,69,18};
int param0_4[] = {-91,-85,-77,-73,-70,-68,-24,-21,-12,-1,9,29,48,52,56,63,88};
int param0_5[] = {0,0,0,1,1,0,1,1,1,1};
int param0_6[] = {4,5,9,14,18,20,22,23,25,28,30,31,34,35,36,38,38,39,44,48,49,51,54,55,59,64,66,71,72,72,73,76,78,82,82,84,92,93,95};
int param0_7[] = {40,6,33,8,78,-58,2,24,40,3,46,94,-26,8,22,-83,96,-29,-38,-59,19,62,98,-55,-42,79,26,62,-56,-85,-22};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {3,68,40,48,54,35,95,56,89,40,77,68,46,78,13,27,6,17,36,99,81,2,77,52,66,52,92,43,90,22,55,67,99,60,58};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {4,18,25,33,8,7,22,20,23,28};
    int param2[] = {4,20,26,42,12,8,33,16,21,21};
    int param3[] = {5,20,15,35,8,6,19,19,19,23};
    int param4[] = {4,23,18,41,8,7,25,16,23,23};
    int filled_function_param0_0[] = {9,30,49,65,78,85,85,92};
int filled_function_param0_1[] = {-48,89,-60,66,71,-37,47,-50,61,41,-22,-3,90,-57,77,-64,22,8,-90,-5,-94,-43,29,-29,86,-79,-8,27,-20,-44,16};
int filled_function_param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int filled_function_param0_3[] = {87,70,77,87,73,81,66,19,83,7,63,42,42,59,20,73,17,27,47,2,63,62,19,17,69,39,82,71,81,39,36,40,45,4,25,69,30,76,68,88,29,73,68,51,24,14,69,18};
int filled_function_param0_4[] = {-91,-85,-77,-73,-70,-68,-24,-21,-12,-1,9,29,48,52,56,63,88};
int filled_function_param0_5[] = {0,0,0,1,1,0,1,1,1,1};
int filled_function_param0_6[] = {4,5,9,14,18,20,22,23,25,28,30,31,34,35,36,38,38,39,44,48,49,51,54,55,59,64,66,71,72,72,73,76,78,82,82,84,92,93,95};
int filled_function_param0_7[] = {40,6,33,8,78,-58,2,24,40,3,46,94,-26,8,22,-83,96,-29,-38,-59,19,62,98,-55,-42,79,26,62,-56,-85,-22};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_9[] = {3,68,40,48,54,35,95,56,89,40,77,68,46,78,13,27,6,17,36,99,81,2,77,52,66,52,92,43,90,22,55,67,99,60,58};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {4,18,25,33,8,7,22,20,23,28};
    int filled_function_param2[] = {4,20,26,42,12,8,33,16,21,21};
    int filled_function_param3[] = {5,20,15,35,8,6,19,19,19,23};
    int filled_function_param4[] = {4,23,18,41,8,7,25,16,23,23};
    for(int i = 0; i < len(param0); ++i)
    {
        f_filled(filled_function_param0[i],filled_function_param1[i],filled_function_param2[i],filled_function_param3[i],filled_function_param4[i]);
        f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]);
        if(equal(begin(param0[i]), end(param0[i]), begin(filled_function_param0[i])) && param1[i] == filled_function_param1[i] && param2[i] == filled_function_param2[i] && param3[i] == filled_function_param3[i] && param4[i] == filled_function_param4[i])
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}