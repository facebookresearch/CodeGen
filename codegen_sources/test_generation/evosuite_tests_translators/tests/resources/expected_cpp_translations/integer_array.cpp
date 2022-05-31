#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
#include "gtest/gtest.h"
#include "gmock/gmock.h"

using namespace std;



//TOFILL





  TEST(EvoSuiteTest, test0){
      int* integerArray0 = new int[2];
      int int0 = (-1);
      int integer0 = ((-1));
      ASSERT_EQ ((-1),  (int)integer0);
      ASSERT_TRUE (integer0 == (int0));

      integerArray0[0] = integer0;
      int integer1 = (1);
      ASSERT_EQ (1,  (int)integer1);
      ASSERT_FALSE (integer1 == (int0));
      ASSERT_FALSE (integer1 == (integer0));

      integerArray0[1] = integer1;
      int* intArray0 = new int[3];
      intArray0[2] = int0;
      bool bool0 = f_filled(integerArray0, intArray0, 1, 0);
      ASSERT_TRUE (bool0);
      ASSERT_THAT(new int[] {(-1), 0, 0}, ::testing::ContainerEq( intArray0));
      ASSERT_EQ (2,  integerArray0.length);
      ASSERT_EQ (3,  intArray0.length);
  }

  TEST(EvoSuiteTest, test1){
      int* integerArray0 = new int[2];
      int int0 = (-1);
      int integer0 = ((-1));
      ASSERT_EQ ((-1),  (int)integer0);
      ASSERT_TRUE (integer0 == (int0));

      integerArray0[0] = integer0;
      int int1 = 1;
      integerArray0[1] = integer0;
      int* intArray0 = new int[3];
      intArray0[2] = int0;
      bool bool0 = f_filled(integerArray0, intArray0, int1, (-50146));
      ASSERT_TRUE (bool0);
      ASSERT_THAT(new int[] {(-1), 0, 0}, ::testing::ContainerEq( intArray0));
      ASSERT_FALSE (int1 == int0);
      ASSERT_EQ (2,  integerArray0.length);
      ASSERT_EQ (3,  intArray0.length);
  }

  TEST(EvoSuiteTest, test2){
      int* integerArray0 = new int[2];
      int integer0 = ((-1));
      ASSERT_EQ ((-1),  (int)integer0);

      integerArray0[0] = integer0;
      integerArray0[1] = integer0;
      int* intArray0 = new int[3];
      bool bool0 = f_filled(integerArray0, intArray0, (-54229), 1);
      ASSERT_TRUE (bool0);
      ASSERT_THAT(new int[] {0, 0, 0}, ::testing::ContainerEq( intArray0));
      ASSERT_EQ (2,  integerArray0.length);
      ASSERT_EQ (3,  intArray0.length);
  }

  TEST(EvoSuiteTest, test3){
      int* integerArray0 = new int[2];
      int integer0 = ((-1));
      ASSERT_EQ ((-1),  (int)integer0);

      integerArray0[0] = integer0;
      int int0 = 1;
      integerArray0[1] = integerArray0[0];
      int* intArray0 = new int[3];
      bool bool0 = f_filled(integerArray0, intArray0, 1, int0);
      ASSERT_FALSE (bool0);
      ASSERT_THAT(new int[] {0, 0, 0}, ::testing::ContainerEq( intArray0));
      ASSERT_EQ (2,  integerArray0.length);
      ASSERT_EQ (3,  intArray0.length);
  }



int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}