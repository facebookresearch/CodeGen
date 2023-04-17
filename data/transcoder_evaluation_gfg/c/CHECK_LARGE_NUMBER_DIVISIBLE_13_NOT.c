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

bool f_gold ( char num [] ) {
  int length = len(num);
  if ( length == 1 && num [ 0 ] == '0' ) return true;
  if ( length % 3 == 1 ) {
    num += "00";
    length += 2;
  }
  else if ( length % 3 == 2 ) {
    num += "0";
    length += 1;
  }
  int sum = 0, p = 1;
  for ( int i = length - 1;
  i >= 0;
  i -- ) {
    int group = 0;
    group += num [ i -- ] - '0';
    group += ( num [ i -- ] - '0' ) * 10;
    group += ( num [ i ] - '0' ) * 100;
    sum = sum + group * p;
    p *= ( - 1 );
  }
  sum = abs ( sum );
  return ( sum % 13 == 0 );
}


bool f_filled ( char num [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"vzTUaItpCpLnjY","33855","0011110101011","MMQ","439340517954","000000000","UugAuRRJbjEgl","6406553695441","011001","yjFqEEvgiNjEX"};
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