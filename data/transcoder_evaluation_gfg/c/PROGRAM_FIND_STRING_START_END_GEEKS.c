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

bool f_gold ( char str [], char corner [] ) {
  int n = strlen(str);
  int cl = strlen(corner);
  if ( n < cl ) return false;
  return ( str . substr ( 0, cl ) . compare ( corner ) == 0 && str . substr ( n - cl, cl ) . compare ( corner ) == 0 );
}


bool f_filled ( char str [], char corner [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"geeksmanishgeeks","shreyadhatwalia","10000100","abaa","30645530","0000011011001","dkqEd","48694119324654","1101010010","Ks"};
    char param1[][100] = {"geeks","abc","100","a","30","001","d","654","11","KsFLmngGGOmHKs"};
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