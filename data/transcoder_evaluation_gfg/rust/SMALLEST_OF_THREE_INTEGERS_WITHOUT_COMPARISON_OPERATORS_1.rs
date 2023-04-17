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

pub unsafe fn f_gold(mut x: i32, mut y: i32,
                                mut z: i32) -> i32 {
    if y / x == 0 { return if y / z == 0 { y } else { z } }
    return if x / z == 0 { x } else { z };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [48 as i32, 11 as i32, 50 as i32,
         21 as i32, 94 as i32, 22 as i32,
         3 as i32, 67 as i32, 59 as i32,
         50 as i32];
    let mut param1: [i32; 10] =
        [63 as i32, 55 as i32, 89 as i32,
         71 as i32, 39 as i32, 44 as i32,
         41 as i32, 62 as i32, 2 as i32,
         11 as i32];
    let mut param2: [i32; 10] =
        [56 as i32, 84 as i32, 96 as i32,
         74 as i32, 42 as i32, 86 as i32,
         68 as i32, 94 as i32, 83 as i32,
         1 as i32];
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
