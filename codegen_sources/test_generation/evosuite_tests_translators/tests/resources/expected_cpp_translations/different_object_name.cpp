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
      
      int* intArray0 = new int[1];
      int int0 = f_filled(intArray0, (-39131));
      ASSERT_EQ (0,  int0);
  }


int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}