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



  TEST(EvoSuiteTest, test2){
      bool bool0 = f_filled("", NULL);
      ASSERT_FALSE (bool0);
  }


int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}