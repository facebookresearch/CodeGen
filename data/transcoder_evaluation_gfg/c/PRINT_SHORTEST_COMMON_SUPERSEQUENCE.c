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

char f_gold [] ( char X [], char Y [] ) {
  int m = strlen(X);
  int n = strlen(Y);
  int dp [ m + 1 ] [ n + 1 ];
  for ( int i = 0;
  i <= m;
  i ++ ) {
    for ( int j = 0;
    j <= n;
    j ++ ) {
      if ( i == 0 ) dp [ i ] [ j ] = j;
      else if ( j == 0 ) dp [ i ] [ j ] = i;
      else if ( X [ i - 1 ] == Y [ j - 1 ] ) dp [ i ] [ j ] = 1 + dp [ i - 1 ] [ j - 1 ];
      else dp [ i ] [ j ] = 1 + min ( dp [ i - 1 ] [ j ], dp [ i ] [ j - 1 ] );
    }
  }
  int index = dp [ m ] [ n ];
  char str [];
  int i = m, j = n;
  while ( i > 0 && j > 0 ) {
    if ( X [ i - 1 ] == Y [ j - 1 ] ) {
      str . push_back ( X [ i - 1 ] );
      i --, j --, index --;
    }
    else if ( dp [ i - 1 ] [ j ] > dp [ i ] [ j - 1 ] ) {
      str . push_back ( Y [ j - 1 ] );
      j --, index --;
    }
    else {
      str . push_back ( X [ i - 1 ] );
      i --, index --;
    }
  }
  while ( i > 0 ) {
    str . push_back ( X [ i - 1 ] );
    i --, index --;
  }
  while ( j > 0 ) {
    str . push_back ( Y [ j - 1 ] );
    j --, index --;
  }
  reverse ( str . begin ( ), str . end ( ) );
  return str;
}


char f_filled [] ( char X [], char Y [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"TDqjbbdzRkA","1071","0","yqLp","22508607","11000010","fcOw","0089872133806","000010000110","aeQVc"};
    char param1[][100] = {"Y","6273318333","100","oXDzdBmOmTHkM","736179592","01001","muMFduA","73","0011111100","fWZsG"};
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