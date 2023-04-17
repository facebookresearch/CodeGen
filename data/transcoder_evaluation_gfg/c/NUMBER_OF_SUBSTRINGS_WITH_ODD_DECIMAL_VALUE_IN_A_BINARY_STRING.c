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

int f_gold ( char s [] ) {
  int n = strlen(s);
  int auxArr [ n ] = {
    0 };
    if ( s [ 0 ] == '1' ) auxArr [ 0 ] = 1;
    for ( int i = 1;
    i < n;
    i ++ ) {
      if ( s [ i ] == '1' ) auxArr [ i ] = auxArr [ i - 1 ] + 1;
      else auxArr [ i ] = auxArr [ i - 1 ];
    }
    int count = 0;
    for ( int i = n - 1;
    i >= 0;
    i -- ) if ( s [ i ] == '1' ) count += auxArr [ i ];
    return count;
  }
  

int f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"OGiOkJF","517376","11","Ze","8763644247018","00111010001","HGwkBKUOVu","652","101000011110","kvdpG "};
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