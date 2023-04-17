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

pub unsafe fn f_gold(mut a: i32, mut b: i32,
                                mut c: i32, mut d: i32)
 -> bool {
    let mut sum: i32 = a * a + b * b + c * c;
    if d * d == sum {
        return 1 as i32 != 0
    } else { return 0 as i32 != 0 };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [1 as i32, 3 as i32, 0 as i32,
         -(1 as i32), 82 as i32, 14 as i32,
         6 as i32, 13 as i32, 96 as i32,
         70 as i32];
    let mut param1: [i32; 10] =
        [2 as i32, 2 as i32, 0 as i32,
         -(1 as i32), 79 as i32, 57 as i32,
         96 as i32, 7 as i32, 65 as i32,
         33 as i32];
    let mut param2: [i32; 10] =
        [2 as i32, 5 as i32, 0 as i32,
         -(1 as i32), 6 as i32, 35 as i32,
         45 as i32, 3 as i32, 72 as i32,
         6 as i32];
    let mut param3: [i32; 10] =
        [3 as i32, 38 as i32, 0 as i32,
         1 as i32, 59 as i32, 29 as i32,
         75 as i32, 63 as i32, 93 as i32,
         2 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize], param3[i as usize]) as i32 ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize], param3[i as usize]) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
