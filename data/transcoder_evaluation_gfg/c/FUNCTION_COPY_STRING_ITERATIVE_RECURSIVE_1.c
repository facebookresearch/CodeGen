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

void f_gold ( char s1 [ ], char s2 [ ], int index = 0 ) {
  s2 [ index ] = s1 [ index ];
  if ( s1 [ index ] == '\0' ) return;
  f_gold ( s1, s2, index + 1 );
}


void f_filled ( char s1 [ ], char s2 [ ], int index = 0 ) {}

int main(void) {
    int n_success = 0;
    char param0_0[] = {','B','D','D','D','E','E','E','G','H','J','K','K','K','L','N','O','S','V','W','Y','Z','b','c','d','d','f','f','f','f','f','f','i','k','k','o','t','u','v','x','x','z'};
char param0_1[] = {'4'};
char param0_2[] = {'0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1'};
char param0_3[] = {'D','I','u','K','e','s','n','z','d','y','S','P','y','r'};
char *param0[4] = {param0_0,param0_1,param0_2,param0_3};
    char param1_0[] = {'Z'};
char param1_1[] = {'8','6','0','2','8','0','8','7','0','5','4','5','9','4','5','4','4'};
char param1_2[] = {'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'};
char param1_3[] = {'S','m','d','a','W','N','F','H','B','E','h','M','z','H','c','X','l','a','R','e','D','D','q','V','U','w','o','K','u','n','b','k','Y','M','L','H','L','X','H','r','D','o','A','Y','H'};
char param1_4[] = {'0','0','0','0','0','1','1','1','2','2','2','3','3','4','4','4','5','5','5','5','6','6','7','7','7','7','7','8','8','8','8','9','9','9','9','9','9','9'};
char param1_5[] = {'1','1','0','0','0','1','0','1','1','0','0','0','1','0','1','0','1','1','0','1','1','0','1'};
char param1_6[] = {'G','G','J','K','L','N','Q','R','R','S','U','W','X','Y','Y','a','b','b','b','c','d','e','e','f','f','h','j','j','k','k','l','m','m','n','o','s','t','t','w','z','z','z'};
char param1_7[] = {'8'};
char param1_8[] = {'0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1'};
char param1_9[] = {'N','h','M','N','n','F','Y','L','G','w','o','G','y','q'};
char *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {0,11,34,41,33,13,40,0,12,7};
    char filled_function_param0_0[] = {','B','D','D','D','E','E','E','G','H','J','K','K','K','L','N','O','S','V','W','Y','Z','b','c','d','d','f','f','f','f','f','f','i','k','k','o','t','u','v','x','x','z'};
char filled_function_param0_1[] = {'4'};
char filled_function_param0_2[] = {'0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1'};
char filled_function_param0_3[] = {'D','I','u','K','e','s','n','z','d','y','S','P','y','r'};
char *filled_function_param0[4] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3};
    char filled_function_param1_0[] = {'Z'};
char filled_function_param1_1[] = {'8','6','0','2','8','0','8','7','0','5','4','5','9','4','5','4','4'};
char filled_function_param1_2[] = {'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'};
char filled_function_param1_3[] = {'S','m','d','a','W','N','F','H','B','E','h','M','z','H','c','X','l','a','R','e','D','D','q','V','U','w','o','K','u','n','b','k','Y','M','L','H','L','X','H','r','D','o','A','Y','H'};
char filled_function_param1_4[] = {'0','0','0','0','0','1','1','1','2','2','2','3','3','4','4','4','5','5','5','5','6','6','7','7','7','7','7','8','8','8','8','9','9','9','9','9','9','9'};
char filled_function_param1_5[] = {'1','1','0','0','0','1','0','1','1','0','0','0','1','0','1','0','1','1','0','1','1','0','1'};
char filled_function_param1_6[] = {'G','G','J','K','L','N','Q','R','R','S','U','W','X','Y','Y','a','b','b','b','c','d','e','e','f','f','h','j','j','k','k','l','m','m','n','o','s','t','t','w','z','z','z'};
char filled_function_param1_7[] = {'8'};
char filled_function_param1_8[] = {'0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1'};
char filled_function_param1_9[] = {'N','h','M','N','n','F','Y','L','G','w','o','G','y','q'};
char *filled_function_param1[10] = {filled_function_param1_0,filled_function_param1_1,filled_function_param1_2,filled_function_param1_3,filled_function_param1_4,filled_function_param1_5,filled_function_param1_6,filled_function_param1_7,filled_function_param1_8,filled_function_param1_9};
    int filled_function_param2[] = {0,11,34,41,33,13,40,0,12,7};
    for(int i = 0; i < len(param0); ++i)
    {
        f_filled(filled_function_param0[i],filled_function_param1[i],filled_function_param2[i]);
        f_gold(param0[i],param1[i],param2[i]);
        if(equal(begin(param0[i]), end(param0[i]), begin(filled_function_param0[i])) && equal(begin(param1[i]), end(param1[i]), begin(filled_function_param1[i])) && param2[i] == filled_function_param2[i])
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}