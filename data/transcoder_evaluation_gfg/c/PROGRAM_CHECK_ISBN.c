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

bool f_gold ( string & isbn ) {
  int n = strlen(isbn);
  if ( n != 10 ) return false;
  int sum = 0;
  for ( int i = 0;
  i < 9;
  i ++ ) {
    int digit = isbn [ i ] - '0';
    if ( 0 > digit || 9 < digit ) return false;
    sum += ( digit * ( 10 - i ) );
  }
  char last = isbn [ 9 ];
  if ( last != 'X' && ( last < '0' || last > '9' ) ) return false;
  sum += ( ( last == 'X' ) ? 10 : ( last - '0' ) );
  return ( sum % 11 == 0 );
}


bool f_filled ( string & isbn ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"007462542X","0112112425","0545010225","0552527408","424519151311","101011","9780552527408","2290344397","1473226406","DDdguSGiRr"};
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