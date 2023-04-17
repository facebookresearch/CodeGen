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

bool f_gold ( string & str ) {
  vector < bool > mark ( 26, false );
  int index;
  for ( int i = 0;
  i < strlen(str);
  i ++ ) {
    if ( 'A' <= str [ i ] && str [ i ] <= 'Z' ) index = str [ i ] - 'A';
    else if ( 'a' <= str [ i ] && str [ i ] <= 'z' ) index = str [ i ] - 'a';
    mark [ index ] = true;
  }
  for ( int i = 0;
  i <= 25;
  i ++ ) if ( mark [ i ] == false ) return ( false );
  return ( true );
}


bool f_filled ( string & str ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {
    "The quick brown fox jumps over the lazy dog ",
    "The quick brown fox jumps over the dog",
    "abcdefghijklmnopqrstuvwxyz",
    "AbcdefghijKlmnopqrstUVwxyz",
    "The quicK broWn fOX jumps over the laZYy dog ",
    "AbcdefghijKlmnopqrstVwxyz",
    "U",
    "397548458372",
    "11",
    "iwCiUFU r"};
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