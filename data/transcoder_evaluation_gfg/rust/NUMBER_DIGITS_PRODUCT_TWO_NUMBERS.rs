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

pub unsafe fn f_gold(mut a: i32, mut b: i32)
 -> i32 {
    let mut count: i32 = 0 as i32;
    let mut p: i32 = abs(a * b);
    if p == 0 as i32 { return 1 as i32 }
    while p > 0 as i32 { count += 1; p = p / 10 as i32 }
    return count;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [86 as i32, 81 as i32, 48 as i32,
         64 as i32, 56 as i32, 5 as i32,
         25 as i32, 94 as i32, 5 as i32,
         46 as i32];
    let mut param1: [i32; 10] =
        [39 as i32, 87 as i32, 84 as i32,
         80 as i32, 20 as i32, 70 as i32,
         13 as i32, 83 as i32, 55 as i32,
         46 as i32];
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
