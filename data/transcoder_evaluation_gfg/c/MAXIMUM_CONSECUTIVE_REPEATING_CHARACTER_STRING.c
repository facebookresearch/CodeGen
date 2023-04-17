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

char f_gold ( char str [] ) {
  int len = strlen(str);
  int count = 0;
  char res = str [ 0 ];
  for ( int i = 0;
  i < len;
  i ++ ) {
    int cur_count = 1;
    for ( int j = i + 1;
    j < len;
    j ++ ) {
      if ( str [ i ] != str [ j ] ) break;
      cur_count ++;
    }
    if ( cur_count > count ) {
      count = cur_count;
      res = str [ i ];
    }
  }
  return res;
}


char f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"geeekk","3786868","110","aaaabbcbbb","11","011101","WoHNyJYLC","3141711779","10111101101","aabbabababcc"};
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