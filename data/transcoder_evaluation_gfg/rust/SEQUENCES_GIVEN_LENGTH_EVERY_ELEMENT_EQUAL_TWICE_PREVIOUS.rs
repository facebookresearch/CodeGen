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

pub unsafe fn f_gold(mut m: i32, mut n: i32)
 -> i32 {
    if m < n { return 0 as i32 }
    if n == 0 as i32 { return 1 as i32 }
    return f_gold(m - 1 as i32, n) +
               f_gold(m / 2 as i32, n - 1 as i32);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [38 as i32, 39 as i32, 24 as i32,
         90 as i32, 44 as i32, 49 as i32,
         58 as i32, 97 as i32, 99 as i32,
         19 as i32];
    let mut param1: [i32; 10] =
        [34 as i32, 29 as i32, 99 as i32,
         23 as i32, 2 as i32, 70 as i32,
         84 as i32, 34 as i32, 72 as i32,
         67 as i32];
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
