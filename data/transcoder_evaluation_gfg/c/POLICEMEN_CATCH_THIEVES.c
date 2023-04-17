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

int f_gold ( char arr [ ], int n, int k ) {
  int res = 0;
  vector < int > thi;
  vector < int > pol;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] == 'P' ) pol . push_back ( i );
    else if ( arr [ i ] == 'T' ) thi . push_back ( i );
  }
  int l = 0, r = 0;
  while ( l < len(thi) && r < len(pol) ) {
    if ( abs ( thi [ l ] - pol [ r ] ) <= k ) {
      res ++;
      l ++;
      r ++;
    }
    else if ( thi [ l ] < pol [ r ] ) l ++;
    else r ++;
  }
  return res;
}


int f_filled ( char arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    char param0_0[] = {'A','B','B','D','E','E','F','G','G','G','I','J','O','P','Q','Q','Q','Q','R','R','S','U','X','Y','Y','c','d','h','i','i','i','i','k','k','l','l','l','l','m','p','r','r','s','t','t','u','x','z'};
char param0_1[] = {'7','6','0','1','0','1'};
char param0_2[] = {'0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1'};
char param0_3[] = {'y','k','S','i','s','r','i','z','y','f','E','U','y','G','f','f','s','v','v','D','v','V','S','D','K','S','f','V','g','I','J','p','j','k','R','n','m','O','L','X','y','U','y','k','w'};
char param0_4[] = {'1','1','5','8','8'};
char param0_5[] = {'0','1','0','0','1','1','1','0','0','0','1','0','1','0','1','0','0','0','0','0','1','0','0','0','0','1','1','1','0','0','0','0','0','0'};
char param0_6[] = {'A','I','K','Q','Q','X','Z','f','g'};
char param0_7[] = {'7','0','6','9','7','5','1','3','9','8','0','0','1','3','9','2','5','5','2','7','9','3','3','9','3','8','5','5','0','4','6','2','7','4','0','4','6','4','2','3'};
char param0_8[] = {'0','0','0','1','1','1','1','1','1','1','1'};
char param0_9[] = {'D','C','P','H','G','o','u','P','T','G','E','U','n','E','U'};
char *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,3,9,24,2,23,5,35,8,11};
    int param2[] = {45,3,10,44,2,18,8,28,10,12};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}