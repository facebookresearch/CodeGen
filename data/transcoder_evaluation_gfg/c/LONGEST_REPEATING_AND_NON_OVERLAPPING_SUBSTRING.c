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
  int n = strlen(str);
  int LCSRe [ n + 1 ] [ n + 1 ];
  memset ( LCSRe, 0, sizeof ( LCSRe ) );
  char res [];
  int res_length = 0;
  int i, index = 0;
  for ( i = 1;
  i <= n;
  i ++ ) {
    for ( int j = i + 1;
    j <= n;
    j ++ ) {
      if ( str [ i - 1 ] == str [ j - 1 ] && LCSRe [ i - 1 ] [ j - 1 ] < ( j - i ) ) {
        LCSRe [ i ] [ j ] = LCSRe [ i - 1 ] [ j - 1 ] + 1;
        if ( LCSRe [ i ] [ j ] > res_length ) {
          res_length = LCSRe [ i ] [ j ];
          index = max ( i, index );
        }
      }
      else LCSRe [ i ] [ j ] = 0;
    }
  }
  if ( res_length > 0 ) for ( i = index - res_length + 1;
  i <= index;
  i ++ ) res . push_back ( str [ i - 1 ] );
  return res;
}


char f_filled [] ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"fbfHTjE","09285256323","0011000101110","ue JkVZTt","48387612426300","010","ddRrUz","1049162633793","100011","iJfadiVaQqv"};
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