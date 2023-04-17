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

int f_gold ( char str [] [ ], int n ) {
  unordered_map < string, int > m;
  for ( int i = 0;
  i < n;
  i ++ ) m [ str [ i ] ] += 1;
  int res = 0;
  for ( auto it = m . begin ( );
  it != m . end ( );
  it ++ ) if ( ( it -> second == 2 ) ) res ++;
  return res;
}


int f_filled ( char str [] [ ], int n ) {}

int main(void) {
    int n_success = 0;
    char param0_0 [][] = {"};
char param0_1 [][] = {"938","074209","0949093096","218622476","71692175","0714","81217924991","74016430795374","52213147","338","939","798161500954","90528060774015","68715","75810","43450","8017","0193164","5945740","212","4589289","2912211026","0","49","8230114","0733435391403","5429","10070"};
char param0_2 [][] = {"00","0","00","0101111010100","110"};
char param0_3 [][] = {"g","h","ok","h","ok","sqozuC","ut","ZwRcG","ok","MR","jHrWyy","qaJlrokgRHuZH","LjPNzDUKszYmCq","g","ZGjLfMnyAGL","kEZoSxOMEWSFpw","IFtqNaDVnG","iJoJXl","vjrQMyWor","FTEHZqbHGlmHph","QeSdzm","nPostKHkigyJt","mOSekk"};
string *param0[4] = {param0_0,param0_1,param0_2,param0_3};
    int param1[] = {10,32,6,7,6,12,43,20,4,15};
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