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

int f_gold ( string & s ) {
  int n = strlen(s);
  int a [ n ];
  for ( int i = n - 1;
  i >= 0;
  i -- ) {
    int back_up = 0;
    for ( int j = i;
    j < n;
    j ++ ) {
      if ( j == i ) a [ j ] = 1;
      else if ( s [ i ] == s [ j ] ) {
        int temp = a [ j ];
        a [ j ] = back_up + 2;
        back_up = temp;
      }
      else {
        back_up = a [ j ];
        a [ j ] = max ( a [ j - 1 ], a [ j ] );
      }
    }
  }
  return a [ n - 1 ];
}


int f_filled ( string & s ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {" E","0845591950","00101011","pLSvlwrACvFaoT","7246","1010101100000","obPkcLSFp","914757557818","1","PKvUWIQ"};
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