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
      float float0 = f_filled(31337.701F);
      ASSERT_NEAR (9.8205152E8F, float0, 0.01F);
  }

  TEST(EvoSuiteTest, test1){
      float float0 = f_filled(0.0F);
      ASSERT_NEAR (0.0F, float0, 0.01F);
  }



int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}