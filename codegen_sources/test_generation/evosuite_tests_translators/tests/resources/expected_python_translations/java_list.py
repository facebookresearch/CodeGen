import numpy as np
import math
from math import *
import collections
from collections import *
import heapq
import itertools
import random
import sys
import unittest


# TOFILL


class CLASS_db35bde703321c750c7134d5769b704c9ab7f9841c6654abb814683a361f9de1(
    unittest.TestCase
):
    def test0(self):
        arrayList0 = []
        double0 = 0.0
        arrayList0.append(double0)
        double1 = 1.0
        f_filled(arrayList0, double1)
        assert not (double1 in arrayList0)

    def test1(self):
        arrayList0 = []
        double0 = 0.0
        arrayList0.append(double0)
        f_filled(arrayList0, double0)
        assert 0.0 in arrayList0

    def test2(self):
        arrayList0 = []
        double0 = 9000.554
        arrayList0.append(double0)
        f_filled(arrayList0, double0)
        assert 9001 == arrayList0.size()

    def test3(self):
        arrayList0 = []
        double0 = 0.0
        f_filled(arrayList0, double0)
        assert not (double0 in arrayList0)


if __name__ == "__main__":
    unittest.main()
