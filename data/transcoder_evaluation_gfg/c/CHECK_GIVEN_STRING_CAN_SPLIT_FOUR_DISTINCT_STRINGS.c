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

bool f_gold ( char s [] ) {
  if ( len(s) >= 10 ) return true;
  for ( int i = 1;
  i < len(s);
  i ++ ) {
    for ( int j = i + 1;
    j < len(s);
    j ++ ) {
      for ( int k = j + 1;
      k < len(s);
      k ++ ) {
        char s1 [] = s . substr ( 0, i );
        char s2 [] = s . substr ( i, j - i );
        char s3 [] = s . substr ( j, k - j );
        char s4 [] = s . substr ( k, len(s) - k );
        if ( s1 != s2 && s1 != s3 && s1 != s4 && s2 != s3 && s2 != s4 && s3 != s4 ) return true;
      }
    }
  }
  return false;
}


bool f_filled ( char s [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"WKTj Nw","8235021","0101","BLMhiQsQcFla","00363175722","10000","aqEYWNd bqgye","83","000011110111","E"};
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