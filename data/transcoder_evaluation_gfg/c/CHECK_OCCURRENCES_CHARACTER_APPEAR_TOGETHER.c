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

bool f_gold ( char s [], char c ) {
  bool oneSeen = false;
  int i = 0, n = strlen(s);
  while ( i < n ) {
    if ( s [ i ] == c ) {
      if ( oneSeen == true ) return false;
      while ( i < n && s [ i ] == c ) i ++;
      oneSeen = true;
    }
    else i ++;
  }
  return true;
}


bool f_filled ( char s [], char c ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"gILrzLimS","307471222","110","GcAB","113","011110010","wcwob","74571582216153","100000011","ryPErkzY"};
    char param1[] = {'m','2','0','v','3','0','w','1','0','q'};
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