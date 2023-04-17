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

int f_gold ( char s [ ], char t [ ] ) {
  int count = 0;
  for ( int i = 0;
  i < strlen ( t );
  i ++ ) {
    if ( count == strlen ( s ) ) break;
    if ( t [ i ] == s [ count ] ) count ++;
  }
  return count;
}


int f_filled ( char s [ ], char t [ ] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"nObYIOjEQZ","84574","1010001010010","DjZtAfUudk","550","1110","GywyxwH","67318370914755","11011000000101","G"};
    char param1[][100] = {"uARTDTQbmGI","8538229","11","OewGm","132744553919","0101","LPQqEqrDZiwY","9928","00000","V"};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(&param0[i].front(),&param1[i].front()) == f_gold(&param0[i].front(),&param1[i].front()))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}