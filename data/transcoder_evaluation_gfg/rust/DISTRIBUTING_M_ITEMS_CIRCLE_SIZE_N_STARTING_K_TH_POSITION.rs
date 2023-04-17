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

pub unsafe fn f_gold(mut n: i32, mut m: i32,
                                mut k: i32) -> i32 {
    if m <= n - k + 1 as i32 { return m + k - 1 as i32 }
    m = m - (n - k + 1 as i32);
    return if m % n == 0 as i32 { n } else { (m) % n };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [19 as i32, 23 as i32, 92 as i32,
         9 as i32, 20 as i32, 68 as i32,
         66 as i32, 77 as i32, 90 as i32,
         26 as i32];
    let mut param1: [i32; 10] =
        [14 as i32, 51 as i32, 10 as i32,
         50 as i32, 67 as i32, 25 as i32,
         30 as i32, 22 as i32, 1 as i32,
         34 as i32];
    let mut param2: [i32; 10] =
        [34 as i32, 5 as i32, 24 as i32,
         34 as i32, 20 as i32, 40 as i32,
         24 as i32, 32 as i32, 71 as i32,
         54 as i32];
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
