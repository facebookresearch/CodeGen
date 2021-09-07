# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
def f_gold(arr, n, x):
    if n < 2:
        return False
    s = set()
    for i in range(0, n):
        if arr[i] == 0:
            if x == 0:
                return True
            else:
                continue
        if x % arr[i] == 0:
            if x // arr[i] in s:
                return True
            s.add(arr[i])
    return False


#TOFILL

if __name__ == '__main__':
    param = [
        ([1, 2, 3, 7, 23, 23, 25, 27, 37, 42, 53, 56, 58,
          61, 69, 78, 79, 84, 85, 86, 90, 93, 95], 15, 17,),
        ([-10, -18, 88, -36, 78, 66, -70, -34, -88, -98, -70, -4, -94, -92, -76, -78, -30, -
          48, -72, 86, -64, 38, -80, 20, 70, -32, -90, 74, -78, 12, -54, 88, 38, -96, 28], 17, 22,),
        ([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 9, 5,),
        ([83, 61, 55, 89, 16, 78, 44, 54, 22, 49, 58, 62, 53, 99, 35, 83, 29, 19,
          96, 39, 60, 6, 34, 67, 43, 29, 46, 3, 81, 78, 80, 39, 86, 78, 21], 23, 27,),
        ([-96, -88, -80, -62, -58, -56, -54, -52, -34, -20, -
          6, -2, 6, 20, 52, 54, 70, 72, 80, 82, 94], 18, 12,),
        ([0, 1, 1, 0, 0, 1, 1, 1], 4, 6,),
        ([8, 11, 11, 20, 22, 23, 26, 27, 31, 38, 40, 40, 45, 46, 46, 48,
          50, 61, 73, 76, 78, 78, 79, 80, 81, 84, 90, 91, 93, 95], 24, 28,),
        ([18], 0, 0,),
        ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 37, 39,),
        ([19, 37, 47, 40, 72, 59, 51, 53, 92, 3, 21, 81, 29, 48, 97,
          59, 10, 74, 11, 37, 49, 95, 88, 85, 6, 26, 76, 33], 22, 21,)
    ]
    n_success = 0
    for i, parameters_set in enumerate(param):
        if f_filled(*parameters_set) == f_gold(*parameters_set):
            n_success += 1
    print("#Results: %i, %i" % (n_success, len(param)))
