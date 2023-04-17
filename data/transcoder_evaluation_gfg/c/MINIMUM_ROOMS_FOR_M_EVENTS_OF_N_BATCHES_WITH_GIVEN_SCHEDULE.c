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

int f_gold ( char slots [] [ ], int n, int m ) {
  int counts [ m ] = {
    0 };
    for ( int i = 0;
    i < n;
    i ++ ) for ( int j = 0;
    j < m;
    j ++ ) if ( slots [ i ] [ j ] == '1' ) counts [ j ] ++;
    return * max_element ( counts, counts + m );
  }
  

int f_filled ( char slots [] [ ], int n, int m ) {}

int main(void) {
    int n_success = 0;
    char param0_0 [][] = {gcte","ULo","wGb","unnP"};
string *param0[1] = {param0_0};
    int param1[] = {18,3,11,46,33,8,5,7,1,7};
    int param2[] = {30,7,10,29,21,7,4,12,1,8};
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