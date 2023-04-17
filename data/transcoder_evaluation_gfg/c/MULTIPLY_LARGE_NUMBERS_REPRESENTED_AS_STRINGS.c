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

char f_gold [] ( char num1 [], char num2 [] ) {
  int len1 = len(num1);
  int len2 = len(num2);
  if ( len1 == 0 || len2 == 0 ) return "0";
  vector < int > result ( len1 + len2, 0 );
  int i_n1 = 0;
  int i_n2 = 0;
  for ( int i = len1 - 1;
  i >= 0;
  i -- ) {
    int carry = 0;
    int n1 = num1 [ i ] - '0';
    i_n2 = 0;
    for ( int j = len2 - 1;
    j >= 0;
    j -- ) {
      int n2 = num2 [ j ] - '0';
      int sum = n1 * n2 + result [ i_n1 + i_n2 ] + carry;
      carry = sum / 10;
      result [ i_n1 + i_n2 ] = sum % 10;
      i_n2 ++;
    }
    if ( carry > 0 ) result [ i_n1 + i_n2 ] += carry;
    i_n1 ++;
  }
  int i = len(result) - 1;
  while ( i >= 0 && result [ i ] == 0 ) i --;
  if ( i == - 1 ) return "0";
  char s [] = "";
  while ( i >= 0 ) s += std :: to_string ( result [ i -- ] );
  return s;
}


char f_filled [] ( char num1 [], char num2 [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"OaITtzE","88111031","1100111","eiWPbMrFx","43701248","100001111110","jVgOapMp","68337672","00110101","JqSh"};
    char param1[][100] = {"RnYlJUqzk","558471","11111110111101","tBAJaI","4027","11","Xm","56939","1","iAfjQRwuVyost"};
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