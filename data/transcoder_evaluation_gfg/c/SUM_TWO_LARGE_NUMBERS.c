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

char f_gold [] ( char str1 [], char str2 [] ) {
  if ( strlen(str1) > strlen(str2) ) swap ( str1, str2 );
  char str [] = "";
  int n1 = strlen(str1), n2 = strlen(str2);
  reverse ( str1 . begin ( ), str1 . end ( ) );
  reverse ( str2 . begin ( ), str2 . end ( ) );
  int carry = 0;
  for ( int i = 0;
  i < n1;
  i ++ ) {
    int sum = ( ( str1 [ i ] - '0' ) + ( str2 [ i ] - '0' ) + carry );
    str . push_back ( sum % 10 + '0' );
    carry = sum / 10;
  }
  for ( int i = n1;
  i < n2;
  i ++ ) {
    int sum = ( ( str2 [ i ] - '0' ) + carry );
    str . push_back ( sum % 10 + '0' );
    carry = sum / 10;
  }
  if ( carry ) str . push_back ( carry + '0' );
  reverse ( str . begin ( ), str . end ( ) );
  return str;
}


char f_filled [] ( char str1 [], char str2 [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"VkfzrPG","0526110506447","011010010","sPAwZACc ","3","0101","VTtNu","2317170","111111000010","Ktt"};
    char param1[][100] = {"rKZ","903","110100000","liYMsojPiinOV","611","01110101011","Wsmc","898421173423","01100001110111","CTbbVX wGBkE"};
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