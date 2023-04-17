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

void f_gold ( int arr [ ], int n ) {
  vector < int > evenArr;
  vector < int > oddArr;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( ! ( i % 2 ) ) evenArr . push_back ( arr [ i ] );
    else oddArr . push_back ( arr [ i ] );
  }
  sort ( evenArr . begin ( ), evenArr . end ( ) );
  sort ( oddArr . begin ( ), oddArr . end ( ), greater < int > ( ) );
  int i = 0;
  for ( int j = 0;
  j < len(evenArr);
  j ++ ) arr [ i ++ ] = evenArr [ j ];
  for ( int j = 0;
  j < len(oddArr);
  j ++ ) arr [ i ++ ] = oddArr [ j ];
}


void f_filled ( int arr [ ], int n ) {}


int main(void) {
    int n_success = 0;
    int param0_0[] = {6,6,6,10,15,21,38,50,51,72,79,81,82,84,85,86,87};
int param0_1[] = {82,-36,18,-88,-24,20,26,-52,28,2};
int param0_2[] = {0,0,0,1,1,1};
int param0_3[] = {81,47,38,70,35,43,94,30,57,55,78,97,72,1};
int param0_4[] = {-80,-78,-72,-46,-26,-24,-20,8,16,26,38,44,54,68,68,78,86,92};
int param0_5[] = {0,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0};
int param0_6[] = {3,4,9,12,20,30,33,34,37,38,50,51,52,54,60,69,73,74,92,93,94,97,98};
int param0_7[] = {86,-32,64,-36,-36,-30,-66,-60,-76,-56,-60,-16,-60,-98,-18,72,-14};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {61,11,46,40,82,35,37,41,52,76,13,53,53,3,40,29,7,51,20,51,87,1,80,73,89,93,1,71,33,50,62,85,46,1,71,54,81,85};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {15,7,3,8,11,21,13,10,29,36};
    int filled_function_param0_0[] = {6,6,6,10,15,21,38,50,51,72,79,81,82,84,85,86,87};
int filled_function_param0_1[] = {82,-36,18,-88,-24,20,26,-52,28,2};
int filled_function_param0_2[] = {0,0,0,1,1,1};
int filled_function_param0_3[] = {81,47,38,70,35,43,94,30,57,55,78,97,72,1};
int filled_function_param0_4[] = {-80,-78,-72,-46,-26,-24,-20,8,16,26,38,44,54,68,68,78,86,92};
int filled_function_param0_5[] = {0,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0};
int filled_function_param0_6[] = {3,4,9,12,20,30,33,34,37,38,50,51,52,54,60,69,73,74,92,93,94,97,98};
int filled_function_param0_7[] = {86,-32,64,-36,-36,-30,-66,-60,-76,-56,-60,-16,-60,-98,-18,72,-14};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_9[] = {61,11,46,40,82,35,37,41,52,76,13,53,53,3,40,29,7,51,20,51,87,1,80,73,89,93,1,71,33,50,62,85,46,1,71,54,81,85};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {15,7,3,8,11,21,13,10,29,36};
    for(int i = 0; i < len(param0); ++i)
    {
        f_filled(filled_function_param0[i],filled_function_param1[i]);
        f_gold(param0[i],param1[i]);
        if(equal(begin(param0[i]), end(param0[i]), begin(filled_function_param0[i])) && param1[i] == filled_function_param1[i])
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}