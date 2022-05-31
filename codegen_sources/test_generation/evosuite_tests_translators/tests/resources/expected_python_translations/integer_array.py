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


class PERMUTE_TWO_ARRAYS_SUM_EVERY_PAIR_GREATER_EQUAL_K(unittest.TestCase):
    def test0(self):
        integerArray0 = [None] * 2
        int0 = -1
        integer0 = -1
        assert (-1) == int(integer0)
        assert integer0 == (int0)
        assert integer0 is not None

        integerArray0[0] = integer0
        integer1 = 1
        assert 1 == int(integer1)
        assert not (integer1 == (int0))
        assert not (integer1 == (integer0))
        assert integer1 is not None

        integerArray0[1] = integer1
        intArray0 = [0] * 3
        intArray0[2] = int0
        boolean0 = f_filled(integerArray0, intArray0, 1, 0)
        assert boolean0
        assert [(-1), 0, 0] == intArray0
        assert 2 == len(integerArray0)
        assert 3 == len(intArray0)

    def test1(self):
        integerArray0 = [None] * 2
        int0 = -1
        integer0 = -1
        assert (-1) == int(integer0)
        assert integer0 == (int0)
        assert integer0 is not None

        integerArray0[0] = integer0
        int1 = 1
        integerArray0[1] = integer0
        intArray0 = [0] * 3
        intArray0[2] = int0
        boolean0 = f_filled(integerArray0, intArray0, int1, (-50146))
        assert boolean0
        assert [(-1), 0, 0] == intArray0
        assert not (int1 == int0)
        assert 2 == len(integerArray0)
        assert 3 == len(intArray0)

    def test2(self):
        integerArray0 = [None] * 2
        integer0 = -1
        assert (-1) == int(integer0)
        assert integer0 is not None

        integerArray0[0] = integer0
        integerArray0[1] = integer0
        intArray0 = [0] * 3
        boolean0 = f_filled(integerArray0, intArray0, (-54229), 1)
        assert boolean0
        assert [0, 0, 0] == intArray0
        assert 2 == len(integerArray0)
        assert 3 == len(intArray0)

    def test3(self):
        integerArray0 = [None] * 2
        integer0 = -1
        assert (-1) == int(integer0)
        assert integer0 is not None

        integerArray0[0] = integer0
        int0 = 1
        integerArray0[1] = integerArray0[0]
        intArray0 = [0] * 3
        boolean0 = f_filled(integerArray0, intArray0, 1, int0)
        assert not (boolean0)
        assert [0, 0, 0] == intArray0
        assert 2 == len(integerArray0)
        assert 3 == len(intArray0)


if __name__ == "__main__":
    unittest.main()
