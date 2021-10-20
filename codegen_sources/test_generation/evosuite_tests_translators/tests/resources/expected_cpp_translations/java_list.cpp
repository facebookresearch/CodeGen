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
      vector<double> arrayList0;
      double double0 = (0.0);
      arrayList0.add(double0);
      double double1 = (1.0);
      f_filled(arrayList0, double1);
      ASSERT_FALSE (arrayList0.contains(double1));
  }

  TEST(EvoSuiteTest, test1){
      vector<double> arrayList0;
      double double0 = (0.0);
      arrayList0.add(double0);
      f_filled(arrayList0, double0);
      ASSERT_TRUE (arrayList0.contains(0.0));
  }

  TEST(EvoSuiteTest, test2){
      vector<double> arrayList0;
      double double0 = (9000.554);
      arrayList0.add(double0);
      f_filled(arrayList0, double0);
      ASSERT_EQ (9001,  arrayList0.size());
  }

  TEST(EvoSuiteTest, test3){
      vector<double> arrayList0;
      double double0 = (0.0);
      f_filled(arrayList0, double0);
      ASSERT_FALSE (arrayList0.contains(double0));
  }



int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}