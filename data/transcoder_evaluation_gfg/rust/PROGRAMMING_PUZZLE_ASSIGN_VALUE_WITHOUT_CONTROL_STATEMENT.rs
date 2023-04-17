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
                                mut x: bool) -> i32 {
    let mut arr: [i32; 2] = [a, b];
    return arr[x as usize];
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [21 as i32, 17 as i32, 35 as i32,
         23 as i32, 48 as i32, 9 as i32,
         18 as i32, 46 as i32, 99 as i32,
         61 as i32];
    let mut param1: [i32; 10] =
        [7 as i32, 49 as i32, 43 as i32,
         51 as i32, 30 as i32, 44 as i32,
         30 as i32, 91 as i32, 23 as i32,
         54 as i32];
    let mut param2: [i32; 10] =
        [34 as i32, 69 as i32, 18 as i32,
         80 as i32, 99 as i32, 64 as i32,
         34 as i32, 71 as i32, 35 as i32,
         5 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize] != 0) ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize] != 0) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
