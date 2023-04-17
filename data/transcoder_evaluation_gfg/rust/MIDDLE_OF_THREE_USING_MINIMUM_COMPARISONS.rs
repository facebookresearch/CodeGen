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
                                mut c: i32) -> i32 {
    if a < b && b < c || c < b && b < a {
        return b
    } else if b < a && a < c || c < a && a < b { return a } else { return c };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [56 as i32, 56 as i32, 36 as i32,
         71 as i32, 3 as i32, 84 as i32,
         30 as i32, 82 as i32, 90 as i32,
         38 as i32];
    let mut param1: [i32; 10] =
        [5 as i32, 60 as i32, 56 as i32,
         54 as i32, 70 as i32, 57 as i32,
         80 as i32, 54 as i32, 70 as i32,
         4 as i32];
    let mut param2: [i32; 10] =
        [82 as i32, 17 as i32, 51 as i32,
         6 as i32, 81 as i32, 47 as i32,
         85 as i32, 32 as i32, 55 as i32,
         5 as i32];
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
