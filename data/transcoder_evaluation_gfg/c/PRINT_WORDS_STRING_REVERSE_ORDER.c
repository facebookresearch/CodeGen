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

char f_gold [] ( char str [] ) {
  int i = strlen(str) - 1;
  int start, end = i + 1;
  char result [] = "";
  while ( i >= 0 ) {
    if ( str [ i ] == ' ' ) {
      start = i + 1;
      while ( start != end ) result += str [ start ++ ];
      result += ' ';
      end = i;
    }
    i --;
  }
  start = 0;
  while ( start != end ) result += str [ start ++ ];
  return result;
}


char f_filled [] ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {
    "m Dm YZ",
    "65 48 57 71",
    "01 010",
    "mT vhByi",
    "19 44 9 1",
    "0",
    "z vUi  ",
    "7 591 36643 9 055",
    "01",
    "ti YGaijPY"
    };
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