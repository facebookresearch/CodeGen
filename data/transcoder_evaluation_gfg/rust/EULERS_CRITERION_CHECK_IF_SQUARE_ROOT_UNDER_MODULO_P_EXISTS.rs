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

pub unsafe fn f_gold(mut n: i32, mut p: i32)
 -> bool {
    n = n % p;
    let mut x: i32 = 2 as i32;
    while x < p { if x * x % p == n { return 1 as i32 != 0 } x += 1 }
    return 0 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [71 as i32, 85 as i32, 4 as i32,
         20 as i32, 71 as i32, 72 as i32,
         36 as i32, 95 as i32, 83 as i32,
         72 as i32];
    let mut param1: [i32; 10] =
        [78 as i32, 75 as i32, 35 as i32,
         99 as i32, 29 as i32, 88 as i32,
         54 as i32, 52 as i32, 33 as i32,
         13 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize]) as i32 ==
               f_gold(param0[i as usize], param1[i as usize]) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
