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

bool f_gold ( char str [] ) {
  vector < char > list;
  for ( int i = 0;
  i < strlen(str);
  i ++ ) {
    auto pos = find ( list . begin ( ), list . end ( ), str [ i ] );
    if ( pos != list . end ( ) ) {
      auto posi = find ( list . begin ( ), list . end ( ), str [ i ] );
      list . erase ( posi );
    }
    else list . push_back ( str [ i ] );
  }
  if ( strlen(str) % 2 == 0 && list . empty ( ) || ( strlen(str) % 2 == 1 && len(list) == 1 ) ) return true;
  else return false;
}


bool f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"abccba","2674377254","11","abcdecba","26382426486138","111010111010","hUInqJXNdbfP","5191","1110101101","NupSrU xz"};
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