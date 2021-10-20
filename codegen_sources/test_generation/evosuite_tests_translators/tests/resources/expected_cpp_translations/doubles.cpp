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
      double double0 = (3051.0);
      double double1 = f_filled(double0);
      ASSERT_NEAR (3051.0, double1, 1.0E-4);
  }


int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}