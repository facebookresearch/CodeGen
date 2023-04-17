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

int f_gold ( int a, int b ) {
  char s [] = to_string ( b );
  int i;
  for ( i = 0;
  i < strlen(s);
  i ++ ) {
    if ( s [ i ] != '9' ) break;
  }
  int result;
  if ( i == strlen(s) ) result = a * strlen(s);
  else result = a * ( strlen(s) - 1 );
  return result;
}


int f_filled ( int a, int b ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {31,72,23,42,13,93,33,94,60,11};
    int param1[] = {91,85,49,32,7,5,32,76,60,26};
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