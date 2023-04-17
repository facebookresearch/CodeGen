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

bool f_gold ( char num [] ) {
  if ( strlen(num) >= 3 ) {
    int d1 = ( int ) num [ strlen(num) - 1 ];
    if ( d1 % 2 != 0 ) return ( 0 );
    int d2 = ( int ) num [ strlen(num) - 2 ];
    int sum = 0;
    for ( int i = 0;
    i < strlen(num);
    i ++ ) sum += num [ i ];
    return ( sum % 3 == 0 && ( d2 * 10 + d1 ) % 4 == 0 );
  }
  else {
    int number = stoi ( num );
    return ( number % 12 == 0 );
  }
}


bool f_filled ( char num [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"12244824607284961224","392603977949","11101001111","92387493287593874594898678979792","2233244912","10101","12","254535361","1","hMPxVMpOBt"};
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