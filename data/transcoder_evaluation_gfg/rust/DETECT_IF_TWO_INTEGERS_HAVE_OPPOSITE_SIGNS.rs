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

pub unsafe fn f_gold(mut x: i32, mut y: i32)
 -> bool {
    return x ^ y < 0 as i32;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [59 as i32, -(20 as i32), -(100 as i32),
         54 as i32, -(16 as i32), -(23 as i32),
         93 as i32, 24 as i32, -(8 as i32),
         29 as i32];
    let mut param1: [i32; 10] =
        [-(99 as i32), -(21 as i32), 100 as i32,
         -(49 as i32), 16 as i32, -(68 as i32),
         37 as i32, -(61 as i32), 69 as i32,
         10 as i32];
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
