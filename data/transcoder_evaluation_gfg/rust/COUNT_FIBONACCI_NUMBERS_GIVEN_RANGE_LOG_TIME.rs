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
    let mut f1: i32 = 0 as i32;
    let mut f2: i32 = 1 as i32;
    let mut f3: i32 = 1 as i32;
    let mut result: i32 = 0 as i32;
    while f1 <= high {
        if f1 >= low { result += 1 }
        f1 = f2;
        f2 = f3;
        f3 = f1 + f2
    }
    return result;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [76 as i32, 96 as i32, 19 as i32,
         36 as i32, 60 as i32, 20 as i32,
         76 as i32, 63 as i32, 2 as i32,
         41 as i32];
    let mut param1: [i32; 10] =
        [43 as i32, 52 as i32, 79 as i32,
         2 as i32, 11 as i32, 15 as i32,
         4 as i32, 93 as i32, 25 as i32,
         39 as i32];
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
