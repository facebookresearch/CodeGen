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

pub unsafe fn f_gold(mut N: i32, mut K: i32)
 -> i32 {
    let mut ans: i32 = 0 as i32;
    let mut y: i32 = N / K;
    let mut x: i32 = N % K;
    ans =
        K * (K - 1 as i32) / 2 as i32 * y +
            x * (x + 1 as i32) / 2 as i32;
    return ans;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [40 as i32, 46 as i32, 97 as i32,
         63 as i32, 92 as i32, 60 as i32,
         67 as i32, 61 as i32, 74 as i32,
         67 as i32];
    let mut param1: [i32; 10] =
        [90 as i32, 64 as i32, 20 as i32,
         1 as i32, 52 as i32, 35 as i32,
         40 as i32, 62 as i32, 61 as i32,
         41 as i32];
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
