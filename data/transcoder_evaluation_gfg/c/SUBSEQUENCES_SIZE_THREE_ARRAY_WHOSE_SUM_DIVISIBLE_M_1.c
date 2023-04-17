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

int f_gold ( int A [ ], int N, int M ) {
  int ans = 0;
  int h [ M ] = {
    0 };
    for ( int i = 0;
    i < N;
    i ++ ) {
      A [ i ] = A [ i ] % M;
      h [ A [ i ] ] ++;
    }
    for ( int i = 0;
    i < M;
    i ++ ) {
      for ( int j = i;
      j < M;
      j ++ ) {
        int rem = ( M - ( i + j ) % M ) % M;
        if ( rem < j ) continue;
        if ( i == j && rem == j ) ans += h [ i ] * ( h [ i ] - 1 ) * ( h [ i ] - 2 ) / 6;
        else if ( i == j ) ans += h [ i ] * ( h [ i ] - 1 ) * h [ rem ] / 2;
        else if ( i == rem ) ans += h [ i ] * ( h [ i ] - 1 ) * h [ j ] / 2;
        else if ( rem == j ) ans += h [ j ] * ( h [ j ] - 1 ) * h [ i ] / 2;
        else ans = ans + h [ i ] * h [ j ] * h [ rem ];
      }
    }
    return ans;
  }
  

int f_filled ( int A [ ], int N, int M ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,7,13,16,19,20,21,25,28,31,36,38,42,44,50,54,55,56,63,63,63,65,65,65,67,71,73,73,76,78,87,90,91,99};
int param0_1[] = {28,-8,-86,-6,-28,74,82,88,-62,-24,-14,68,36,-54,-16,-52,-78,-24,68,-2,30,-56,30,-86,-54,54,62,-30,-82,66,94,12,10,4,40,-72,20,-2,-90,-90};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {45,14,91,37,91};
int param0_4[] = {-88,-78,-74,-50,-44,-34,-26,-22,14,46,48,80,82,86,88};
int param0_5[] = {1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1};
int param0_6[] = {9,14,16,18,23,36,37,58,78};
int param0_7[] = {-56,86,58,-58,46,-62,8,-22,80,96,-74,-94,-94,-2,-4};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {62,36,66,84,20,43,93,47,85,70,50,96,3,8,38,96,15,31,97,90,1,69,77,20,68,11,2,92,50,8,23,83,76,6,32,43,92};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {27,29,29,3,13,11,7,13,37,18};
    int param2[] = {21,21,43,4,12,15,4,14,34,35};
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