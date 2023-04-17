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

int f_gold ( char str [] ) {
  char tmp [] = str + str;
  int n = strlen(str);
  for ( int i = 1;
  i <= n;
  i ++ ) {
    char substring [] = tmp . substr ( i, len(str) );
    if ( str == substring ) return i;
  }
  return n;
}


int f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"vdevdNdQSopPtj","5","100010101011","tlDOvJHAyMllu","06","101","DYgtU","4","00","Dt"};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i]) == f_gold(param0[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}