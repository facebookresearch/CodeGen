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

int f_gold ( char n [] ) {
  char num [] = n;
  int dec_value = 0;
  int base = 1;
  int len = strlen(num);
  for ( int i = len - 1;
  i >= 0;
  i -- ) {
    if ( num [ i ] == '1' ) dec_value += base;
    base = base * 2;
  }
  return dec_value;
}


int f_filled ( char n [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"uEmIAgF","753310137","010011010","kNi","04562016903312","000111101","bk","9","1","XxT nXLlk"};
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