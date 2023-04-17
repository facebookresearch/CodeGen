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

pub unsafe fn f_gold(mut arr: *mut i32,
                                mut low: i32, mut high: i32)
 -> i32 {
    if high >= low {
        let mut mid: i32 = (low + high) / 2 as i32;
        if mid == *arr.offset(mid as isize) { return mid }
        if mid > *arr.offset(mid as isize) {
            return f_gold(arr, mid + 1 as i32, high)
        } else { return f_gold(arr, low, mid - 1 as i32) }
    }
    return -(1 as i32);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0_0: [i32; 1] = [9 as i32];
    let mut param0_1: [i32; 9] =
        [1 as i32, 1 as i32, 0 as i32,
         1 as i32, 1 as i32, 0 as i32,
         1 as i32, 0 as i32, 0 as i32];
    let mut param0_2: [i32; 30] =
        [1 as i32, 4 as i32, 16 as i32,
         16 as i32, 19 as i32, 28 as i32,
         34 as i32, 34 as i32, 35 as i32,
         36 as i32, 37 as i32, 46 as i32,
         49 as i32, 52 as i32, 54 as i32,
         60 as i32, 60 as i32, 60 as i32,
         63 as i32, 70 as i32, 75 as i32,
         77 as i32, 80 as i32, 81 as i32,
         81 as i32, 84 as i32, 85 as i32,
         87 as i32, 93 as i32, 99 as i32];
    let mut param0_3: [i32; 6] =
        [30 as i32, 30 as i32, -(94 as i32),
         -(10 as i32), 2 as i32, 58 as i32];
    let mut param0_4: [i32; 34] =
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
         1 as i32];
    let mut param0_5: [i32; 10] =
        [72 as i32, 38 as i32, 91 as i32,
         63 as i32, 30 as i32, 67 as i32,
         39 as i32, 29 as i32, 96 as i32,
         42 as i32];
    let mut param0: [*mut i32; 6] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr()];
    let mut param1: [i32; 10] =
        [0 as i32, 0 as i32, 0 as i32,
         1 as i32, 2 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32];
    let mut param2: [i32; 10] =
        [16 as i32, 4 as i32, 4 as i32,
         5 as i32, 5 as i32, 7 as i32,
         5 as i32, 5 as i32, 12 as i32,
         7 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize]) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
