#![feature(main)]
// Copyright (c) 2019-present, Facebook, Inc.
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.
//

#[no_mangle]
pub unsafe fn abs(mut x: i32)
 -> i32 {
    return x.abs();
}

#[no_mangle]
pub unsafe fn min(mut x: i32, mut y: i32)
 -> i32 {
    return if x < y { x } else { y };
}
#[no_mangle]
pub unsafe fn max(mut x: i32, mut y: i32)
 -> i32 {
    return if x > y { x } else { y };
}

pub unsafe fn f_gold(mut arr: *mut i32, mut n: i32)
 -> i32 {
    let vla = n as usize;
    let mut msis: Vec<i32> = ::std::vec::from_elem(0, vla);
    let vla_0 = n as usize;
    let mut msds: Vec<i32> = ::std::vec::from_elem(0, vla_0);
    let mut max_sum: i32 =
        -(2147483647 as i32) - 1 as i32;
    *msis.as_mut_ptr().offset(0 as i32 as isize) =
        *arr.offset(0 as i32 as isize);
    let mut i: i32 = 1 as i32;
    while i < n {
        if *arr.offset(i as isize) >
               *arr.offset((i - 1 as i32) as isize) {
            *msis.as_mut_ptr().offset(i as isize) =
                *msis.as_mut_ptr().offset((i - 1 as i32) as isize) +
                    *arr.offset(i as isize)
        } else {
            *msis.as_mut_ptr().offset(i as isize) = *arr.offset(i as isize)
        }
        i += 1
    }
    *msds.as_mut_ptr().offset((n - 1 as i32) as isize) =
        *arr.offset((n - 1 as i32) as isize);
    let mut i_0: i32 = n - 2 as i32;
    while i_0 >= 0 as i32 {
        if *arr.offset(i_0 as isize) >
               *arr.offset((i_0 + 1 as i32) as isize) {
            *msds.as_mut_ptr().offset(i_0 as isize) =
                *msds.as_mut_ptr().offset((i_0 + 1 as i32) as isize) +
                    *arr.offset(i_0 as isize)
        } else {
            *msds.as_mut_ptr().offset(i_0 as isize) =
                *arr.offset(i_0 as isize)
        }
        i_0 -= 1
    }
    let mut i_1: i32 = 0 as i32;
    while i_1 < n {
        if max_sum <
               *msis.as_mut_ptr().offset(i_1 as isize) +
                   *msds.as_mut_ptr().offset(i_1 as isize) -
                   *arr.offset(i_1 as isize) {
            max_sum =
                *msis.as_mut_ptr().offset(i_1 as isize) +
                    *msds.as_mut_ptr().offset(i_1 as isize) -
                    *arr.offset(i_1 as isize)
        }
        i_1 += 1
    }
    return max_sum;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0_0: [i32; 23] =
        [7 as i32, 12 as i32, 16 as i32,
         23 as i32, 26 as i32, 27 as i32,
         39 as i32, 39 as i32, 40 as i32,
         44 as i32, 57 as i32, 58 as i32,
         77 as i32, 78 as i32, 81 as i32,
         82 as i32, 84 as i32, 86 as i32,
         91 as i32, 94 as i32, 94 as i32,
         95 as i32, 97 as i32];
    let mut param0_1: [i32; 44] =
        [72 as i32, 38 as i32, -(60 as i32),
         98 as i32, -(52 as i32), -(38 as i32),
         -(2 as i32), 94 as i32, 34 as i32,
         56 as i32, 90 as i32, 46 as i32,
         6 as i32, -(2 as i32), 30 as i32,
         -(96 as i32), -(76 as i32), -(96 as i32),
         -(76 as i32), 32 as i32, 68 as i32,
         64 as i32, -(32 as i32), -(4 as i32),
         72 as i32, -(62 as i32), 58 as i32,
         20 as i32, -(84 as i32), 0 as i32,
         -(96 as i32), 70 as i32, -(22 as i32),
         -(56 as i32), 70 as i32, -(74 as i32),
         -(90 as i32), -(86 as i32), -(14 as i32),
         82 as i32, -(90 as i32), 40 as i32,
         -(64 as i32), 94 as i32];
    let mut param0_2: [i32; 39] =
        [0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32];
    let mut param0_3: [i32; 6] =
        [69 as i32, 31 as i32, 85 as i32,
         84 as i32, 28 as i32, 28 as i32];
    let mut param0_4: [i32; 17] =
        [-(80 as i32), -(74 as i32), -(24 as i32),
         -(22 as i32), -(22 as i32), 4 as i32,
         20 as i32, 28 as i32, 30 as i32,
         32 as i32, 36 as i32, 58 as i32,
         58 as i32, 68 as i32, 92 as i32,
         94 as i32, 98 as i32];
    let mut param0_5: [i32; 11] =
        [1 as i32, 1 as i32, 0 as i32,
         0 as i32, 0 as i32, 1 as i32,
         0 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32];
    let mut param0_6: [i32; 48] =
        [2 as i32, 2 as i32, 2 as i32,
         4 as i32, 6 as i32, 7 as i32,
         8 as i32, 10 as i32, 15 as i32,
         17 as i32, 19 as i32, 20 as i32,
         21 as i32, 27 as i32, 28 as i32,
         29 as i32, 32 as i32, 32 as i32,
         40 as i32, 44 as i32, 46 as i32,
         47 as i32, 49 as i32, 50 as i32,
         50 as i32, 52 as i32, 55 as i32,
         56 as i32, 58 as i32, 59 as i32,
         64 as i32, 69 as i32, 73 as i32,
         74 as i32, 74 as i32, 77 as i32,
         80 as i32, 80 as i32, 84 as i32,
         89 as i32, 91 as i32, 95 as i32,
         96 as i32, 96 as i32, 97 as i32,
         98 as i32, 98 as i32, 99 as i32];
    let mut param0_7: [i32; 21] =
        [26 as i32, -(86 as i32), 8 as i32,
         64 as i32, -(40 as i32), 64 as i32,
         60 as i32, -(16 as i32), 54 as i32,
         -(42 as i32), -(86 as i32), 14 as i32,
         -(48 as i32), -(20 as i32), -(42 as i32),
         -(4 as i32), -(34 as i32), -(52 as i32),
         -(74 as i32), 22 as i32, 10 as i32];
    let mut param0_8: [i32; 42] =
        [0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32,
         1 as i32, 1 as i32, 1 as i32];
    let mut param0_9: [i32; 6] =
        [8 as i32, 5 as i32, 5 as i32,
         56 as i32, 5 as i32, 38 as i32];
    let mut param0: [*mut i32; 10] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr(),
         param0_6.as_mut_ptr(), param0_7.as_mut_ptr(), param0_8.as_mut_ptr(),
         param0_9.as_mut_ptr()];
    let mut param1: [i32; 10] =
        [13 as i32, 37 as i32, 33 as i32,
         5 as i32, 16 as i32, 10 as i32,
         46 as i32, 18 as i32, 27 as i32,
         3 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize]) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
