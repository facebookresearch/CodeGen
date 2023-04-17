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

bool f_gold ( char str1 [], char str2 [] ) {
  if ( strlen(str1) != strlen(str2) ) return false;
  char clock_rot [] = "";
  char anticlock_rot [] = "";
  int len = strlen(str2);
  anticlock_rot = anticlock_rot + str2 . substr ( len - 2, 2 ) + str2 . substr ( 0, len - 2 );
  clock_rot = clock_rot + str2 . substr ( 2 ) + str2 . substr ( 0, 2 );
  return ( str1 . compare ( clock_rot ) == 0 || str1 . compare ( anticlock_rot ) == 0 );
}


bool f_filled ( char str1 [], char str2 [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"amazon","onamaz","amazon","ab","737009","000110","l","4420318628","11011111000000"," pvFHANc"};
    char param1[][100] = {"azonam","amazon","azoman","ab","239119","01111","YVo hqvnGxow","52856","10","xBIDFbiGb"};
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