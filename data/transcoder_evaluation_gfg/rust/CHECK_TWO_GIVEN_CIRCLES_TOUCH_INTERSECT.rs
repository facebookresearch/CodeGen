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

pub unsafe fn f_gold(mut x1: i32, mut y1: i32,
                                mut x2: i32, mut y2: i32,
                                mut r1: i32, mut r2: i32)
 -> i32 {
    let mut distSq: i32 =
        (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
    let mut radSumSq: i32 = (r1 + r2) * (r1 + r2);
    if distSq == radSumSq {
        return 1 as i32
    } else if distSq > radSumSq {
        return -(1 as i32)
    } else { return 0 as i32 };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [11 as i32, 87 as i32, 51 as i32,
         89 as i32, 64 as i32, 57 as i32,
         65 as i32, 32 as i32, 73 as i32,
         3 as i32];
    let mut param1: [i32; 10] =
        [36 as i32, 1 as i32, 1 as i32,
         67 as i32, 10 as i32, 86 as i32,
         90 as i32, 23 as i32, 61 as i32,
         99 as i32];
    let mut param2: [i32; 10] =
        [62 as i32, 62 as i32, 47 as i32,
         9 as i32, 79 as i32, 99 as i32,
         42 as i32, 28 as i32, 63 as i32,
         6 as i32];
    let mut param3: [i32; 10] =
        [64 as i32, 64 as i32, 90 as i32,
         52 as i32, 45 as i32, 43 as i32,
         82 as i32, 26 as i32, 77 as i32,
         19 as i32];
    let mut param4: [i32; 10] =
        [50 as i32, 54 as i32, 14 as i32,
         94 as i32, 67 as i32, 83 as i32,
         77 as i32, 60 as i32, 92 as i32,
         21 as i32];
    let mut param5: [i32; 10] =
        [4 as i32, 41 as i32, 71 as i32,
         21 as i32, 78 as i32, 63 as i32,
         32 as i32, 45 as i32, 76 as i32,
         28 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize], param3[i as usize],
                    param4[i as usize], param5[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize], param3[i as usize],
                      param4[i as usize], param5[i as usize]) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
