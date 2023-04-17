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

bool f_gold ( char str1 [ ], char str2 [ ], int m, int n ) {
  if ( m == 0 ) return true;
  if ( n == 0 ) return false;
  if ( str1 [ m - 1 ] == str2 [ n - 1 ] ) return f_gold ( str1, str2, m - 1, n - 1 );
  return f_gold ( str1, str2, m, n - 1 );
}


bool f_filled ( char str1 [ ], char str2 [ ], int m, int n ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"AXY","AXY","1100","t","034","01111010110","SjOXhD","455","001","MkK"};
    char param1[][100] = {"ADXCPY","YADXCP","001011001111","Isv","376083","10110110","PWkZDupqagB","4553","11100","qfjWaMdMYkqcK"};
    int param2[] = {3,4,4,1,3,8,6,3,3,3};
    int param3[] = {6,6,12,3,6,8,9,4,5,13};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(&param0[i].front(),&param1[i].front(),param2[i],param3[i]) == f_gold(&param0[i].front(),&param1[i].front(),param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}