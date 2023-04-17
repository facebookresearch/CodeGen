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

pub unsafe fn f_gold(mut low: i32, mut high: i32)
 -> i32 {
    let mut fact: i32 = 1 as i32;
    let mut x: i32 = 1 as i32;
    while fact < low { fact = fact * x; x += 1 }
    let mut res: i32 = 0 as i32;
    while fact <= high { res += 1; fact = fact * x; x += 1 }
    return res;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [57 as i32, 57 as i32, 31 as i32,
         62 as i32, 49 as i32, 82 as i32,
         31 as i32, 5 as i32, 76 as i32,
         55 as i32];
    let mut param1: [i32; 10] =
        [79 as i32, 21 as i32, 37 as i32,
         87 as i32, 98 as i32, 76 as i32,
         45 as i32, 52 as i32, 43 as i32,
         6 as i32];
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
