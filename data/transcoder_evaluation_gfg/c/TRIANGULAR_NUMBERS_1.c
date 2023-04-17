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

bool f_gold ( int num ) {
  if ( num < 0 ) return false;
  int c = ( - 2 * num );
  int b = 1, a = 1;
  int d = ( b * b ) - ( 4 * a * c );
  if ( d < 0 ) return false;
  float root1 = ( - b + sqrt ( d ) ) / ( 2 * a );
  float root2 = ( - b - sqrt ( d ) ) / ( 2 * a );
  if ( root1 > 0 && floor ( root1 ) == root1 ) return true;
  if ( root2 > 0 && floor ( root2 ) == root2 ) return true;
  return false;
}


bool f_filled ( int num ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {1,3,6,10,55,48,63,72,16,85};
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