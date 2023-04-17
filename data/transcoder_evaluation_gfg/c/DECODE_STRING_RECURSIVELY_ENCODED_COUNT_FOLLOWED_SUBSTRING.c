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
  stack < int > integerstack;
  stack < char > stringstack;
  char temp [] = "", result = "";
  for ( int i = 0;
  i < strlen(str);
  i ++ ) {
    int count = 0;
    if ( str [ i ] >= '0' && str [ i ] <= '9' ) {
      while ( str [ i ] >= '0' && str [ i ] <= '9' ) {
        count = count * 10 + str [ i ] - '0';
        i ++;
      }
      i --;
      integerstack . push ( count );
    }
    else if ( str [ i ] == ']' ) {
      temp = "";
      count = 0;
      if ( ! integerstack . empty ( ) ) {
        count = integerstack . top ( );
        integerstack . pop ( );
      }
      while ( ! stringstack . empty ( ) && stringstack . top ( ) != '[' ) {
        temp = stringstack . top ( ) + temp;
        stringstack . pop ( );
      }
      if ( ! stringstack . empty ( ) && stringstack . top ( ) == '[' ) stringstack . pop ( );
      for ( int j = 0;
      j < count;
      j ++ ) result = result + temp;
      for ( int j = 0;
      j < strlen(result);
      j ++ ) stringstack . push ( result [ j ] );
      result = "";
    }
    else if ( str [ i ] == '[' ) {
      if ( str [ i - 1 ] >= '0' && str [ i - 1 ] <= '9' ) stringstack . push ( str [ i ] );
      else {
        stringstack . push ( str [ i ] );
        integerstack . push ( 1 );
      }
    }
    else stringstack . push ( str [ i ] );
  }
  while ( ! stringstack . empty ( ) ) {
    result = stringstack . top ( ) + result;
    stringstack . pop ( );
  }
  return result;
}


char f_filled [] ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"rpaBQkHqRaTb","9916267","000010100010","XfHXbWwaRd","750","0","K","0218044","10100010011","zR"};
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