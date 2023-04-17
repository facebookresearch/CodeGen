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

int f_gold ( int X [ ], int Y [ ], int m, int n ) {
  int res = 0;
  sort ( X, X + m, greater < int > ( ) );
  sort ( Y, Y + n, greater < int > ( ) );
  int hzntl = 1, vert = 1;
  int i = 0, j = 0;
  while ( i < m && j < n ) {
    if ( X [ i ] > Y [ j ] ) {
      res += X [ i ] * vert;
      hzntl ++;
      i ++;
    }
    else {
      res += Y [ j ] * hzntl;
      vert ++;
      j ++;
    }
  }
  int total = 0;
  while ( i < m ) total += X [ i ++ ];
  res += total * vert;
  total = 0;
  while ( j < n ) total += Y [ j ++ ];
  res += total * hzntl;
  return res;
}


int f_filled ( int X [ ], int Y [ ], int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,9,9,16,18,20,22,22,23,25,25,26,28,32,33,33,33,34,37,40,44,46,46,52,53,56,58,58,59,60,61,67,67,69,70,70,73,75,77,83,87,87,87,90,90,93,97,98};
int param0_1[] = {-52,66,66,-4,-74,78,52,-72};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {58,78,48,44,63,37,89,76,66,83,52,97,19,28,67,38,54,77,2,96,28,87};
int param0_4[] = {-84,-78,-76,-72,-68,-62,-62,-60,-58,-44,-34,-10,-8,-4,-2,-2,14,16,20,26,26,32,70,78,86,90,96};
int param0_5[] = {0,1,1,0,0,1,1,0,1,0,1,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1,0};
int param0_6[] = {30,75};
int param0_7[] = {70,78,-60,-10,-8,46,38,60,-54,-68,16,10,36,-10,38,-96,-52,-82,-56,22,-56,0,96,-60,24,70,40,62,-20,-36,74,32,44,14,-18,50,58};
int param0_8[] = {0,0,0,1};
int param0_9[] = {81,40,29,74,13,67,10,25,24,81,90};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {2,3,9,10,13,16,17,19,20,23,25,27,29,30,30,35,37,39,39,45,47,50,55,55,55,56,59,60,62,63,67,70,70,71,72,73,73,74,77,86,87,88,91,92,95,96,97,99};
int param1_1[] = {-40,30,-34,-76,84,88,-78,72};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param1_3[] = {37,36,26,5,83,75,33,33,72,63,91,94,75,92,9,19,79,29,40,47,63,36};
int param1_4[] = {-98,-98,-86,-82,-76,-62,-60,-48,-32,-32,-24,-18,-10,-4,0,16,16,26,36,42,48,50,64,66,78,92,98};
int param1_5[] = {1,0,1,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,0};
int param1_6[] = {10,39};
int param1_7[] = {64,-42,-50,-76,46,32,-66,86,-6,46,94,70,-62,90,78,4,6,-20,92,-18,-34,-96,92,-24,-90,-94,62,40,-14,-28,80,-86,-86,-56,40,-92,-22};
int param1_8[] = {0,1,1,1};
int param1_9[] = {51,45,23,7,53,14,49,58,25,75,74};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {25,6,15,13,15,25,1,19,2,8};
    int param3[] = {27,7,19,14,24,26,1,19,2,10};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}