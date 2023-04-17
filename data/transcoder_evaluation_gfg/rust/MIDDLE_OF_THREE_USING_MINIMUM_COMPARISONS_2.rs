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
    let mut x: i32 = a - b;
    let mut y: i32 = b - c;
    let mut z: i32 = a - c;
    if x * y > 0 as i32 {
        return b
    } else if x * z > 0 as i32 { return c } else { return a };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [48 as i32, 21 as i32, 71 as i32,
         93 as i32, 3 as i32, 58 as i32,
         88 as i32, 8 as i32, 17 as i32,
         13 as i32];
    let mut param1: [i32; 10] =
        [46 as i32, 7 as i32, 4 as i32,
         34 as i32, 61 as i32, 78 as i32,
         41 as i32, 84 as i32, 66 as i32,
         3 as i32];
    let mut param2: [i32; 10] =
        [38 as i32, 16 as i32, 31 as i32,
         11 as i32, 32 as i32, 6 as i32,
         66 as i32, 38 as i32, 27 as i32,
         23 as i32];
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
