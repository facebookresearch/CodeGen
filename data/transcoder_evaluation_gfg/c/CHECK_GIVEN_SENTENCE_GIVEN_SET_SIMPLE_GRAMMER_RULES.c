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

bool f_gold ( char str [ ] ) {
  int len = strlen ( str );
  if ( str [ 0 ] < 'A' || str [ 0 ] > 'Z' ) return false;
  if ( str [ len - 1 ] != '.' ) return false;
  int prev_state = 0, curr_state = 0;
  int index = 1;
  while ( str [ index ] ) {
    if ( str [ index ] >= 'A' && str [ index ] <= 'Z' ) curr_state = 0;
    else if ( str [ index ] == ' ' ) curr_state = 1;
    else if ( str [ index ] >= 'a' && str [ index ] <= 'z' ) curr_state = 2;
    else if ( str [ index ] == '.' ) curr_state = 3;
    if ( prev_state == curr_state && curr_state != 2 ) return false;
    if ( prev_state == 2 && curr_state == 0 ) return false;
    if ( curr_state == 3 && prev_state != 1 ) return ( str [ index + 1 ] == '\0' );
    index ++;
    prev_state = curr_state;
  }
  return false;
}


bool f_filled ( char str [ ] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = { "I love cinema.", "The vertex is S.",
                    "I am single.", "My name is KG.",
                    "I lovE cinema.", "GeeksQuiz. is a quiz site.",
                    "I love Geeksquiz and Geeksforgeeks.",
                    "  You are my friend.", "I love cinema", "Hello world !" };
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(&param0[i].front()) == f_gold(&param0[i].front()))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}