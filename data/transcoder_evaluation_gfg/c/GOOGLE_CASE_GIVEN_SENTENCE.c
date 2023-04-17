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

char f_gold [] ( char s [] ) {
  int n = strlen(s);
  s [ 0 ] = tolower ( s [ 0 ] );
  for ( int i = 1;
  i < n;
  i ++ ) {
    if ( s [ i ] == ' ' && i < n ) {
      s [ i + 1 ] = tolower ( s [ i + 1 ] );
      i ++;
    }
    else s [ i ] = toupper ( s [ i ] );
  }
  return s;
}


char f_filled [] ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"TEYndweqZA","01865","11001100","CzwznJmQet","318305446","0000001111110","yzT","38630230","01101","zoizI"};
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