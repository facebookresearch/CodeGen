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

char f_gold [] ( char str [], int k ) {
  char palin [] = str;
  int l = 0;
  int r = strlen(str) - 1;
  while ( l < r ) {
    if ( str [ l ] != str [ r ] ) {
      palin [ l ] = palin [ r ] = max ( str [ l ], str [ r ] );
      k --;
    }
    l ++;
    r --;
  }
  if ( k < 0 ) return "Not possible";
  l = 0;
  r = strlen(str) - 1;
  while ( l <= r ) {
    if ( l == r ) {
      if ( k > 0 ) palin [ l ] = '9';
    }
    if ( palin [ l ] < '9' ) {
      if ( k >= 2 && palin [ l ] == str [ l ] && palin [ r ] == str [ r ] ) {
        k -= 2;
        palin [ l ] = palin [ r ] = '9';
      }
      else if ( k >= 1 && ( palin [ l ] != str [ l ] || palin [ r ] != str [ r ] ) ) {
        k --;
        palin [ l ] = palin [ r ] = '9';
      }
    }
    l ++;
    r --;
  }
  return palin;
}


char f_filled [] ( char str [], int k ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"wUJmbRlwogtFv","43435","43435","12345","5032","0100000001101","sBrbNQiRwQd","7549384614","10000001","VqrTsaoD"};
    int param1[] = {5,3,1,1,3,5,4,3,4,4};
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