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

int f_gold ( char str [ ], int n ) {
  int ans = ( n * ( n + 1 ) ) / 2;
  int a_index = 0;
  int b_index = 0;
  int c_index = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( str [ i ] == 'a' ) {
      a_index = i + 1;
      ans -= min ( b_index, c_index );
    }
    else if ( str [ i ] == 'b' ) {
      b_index = i + 1;
      ans -= min ( a_index, c_index );
    }
    else {
      c_index = i + 1;
      ans -= min ( a_index, b_index );
    }
  }
  return ans;
}


int f_filled ( char str [ ], int n ) {}

int main(void) {
    int n_success = 0;
    char param0_0[] = {','Y','e','u','I','P','y','j','o','n'};
char param0_1[] = {'0','0','2','2','3','3','4','5','6','6','6','7','8','9'};
char param0_2[] = {'0','1','0','1','1','1','1','0','0','0','1','1','0','0','0','0','0','0','1','1','1','1','0','1','0','1','1','1','1','1','0','0'};
char param0_3[] = {'E','G','G','J','L','O','O','S','T','U','V','V','Y','c','d','e','f','g','g','j','m','n','p','q','q','r','u','u','x'};
char param0_4[] = {'8','1','9','6','4','3','8','2','8','5','5','3','0','1','7','3','1','5','4','8','2','3','3','2','2','4','9','6','3','1','4','1','4','0','4','9','4','8','4','7'};
char param0_5[] = {'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'};
char param0_6[] = {'j','z','H','Q'};
char *param0[7] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6};
    int param1[] = {23,24,15,9,8,19,21,36,33,2};
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