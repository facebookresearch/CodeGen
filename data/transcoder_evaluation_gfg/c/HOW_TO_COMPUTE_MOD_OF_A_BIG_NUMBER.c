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

int f_gold ( char num [], int a ) {
  int res = 0;
  for ( int i = 0;
  i < strlen(num);
  i ++ ) res = ( res * 10 + ( int ) num [ i ] - '0' ) % a;
  return res;
}


int f_filled ( char num [], int a ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"RElCP","0139035510","00011110","TwanZWwLNXhFN","6247009752778","0100001011011","NCh","00714746542","101000100","MSTkXmlbPkV"};
    int param1[] = {13,44,86,66,55,33,75,54,93,78};
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