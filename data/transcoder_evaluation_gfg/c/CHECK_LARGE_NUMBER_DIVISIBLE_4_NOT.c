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

bool f_gold ( char str [] ) {
  int n = strlen(str);
  if ( n == 0 ) return false;
  if ( n == 1 ) return ( ( str [ 0 ] - '0' ) % 4 == 0 );
  int last = str [ n - 1 ] - '0';
  int second_last = str [ n - 2 ] - '0';
  return ( ( second_last * 10 + last ) % 4 == 0 );
}


bool f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"PjAFZXQgN","12325195609714","00101111101","xOtbXZiA","980","000000100","zFacc W","8","110011","afiutekeSfYrX"};
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