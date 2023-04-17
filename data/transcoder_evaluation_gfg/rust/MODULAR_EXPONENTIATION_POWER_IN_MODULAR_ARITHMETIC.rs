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

pub unsafe fn f_gold(mut x: i32, mut y: u32,
                                mut p: i32) -> i32 {
    let mut res: i32 = 1 as i32;
    x = x % p;
    while y > 0 as i32 as u32 {
        if y & 1 as i32 as u32 != 0 { res = res * x % p }
        y = y >> 1 as i32;
        x = x * x % p
    }
    return res;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [45 as i32, 67 as i32, 26 as i32,
         33 as i32, 35 as i32, 68 as i32,
         14 as i32, 5 as i32, 23 as i32,
         37 as i32];
    let mut param1: [i32; 10] =
        [5 as i32, 25 as i32, 91 as i32,
         61 as i32, 8 as i32, 41 as i32,
         76 as i32, 89 as i32, 42 as i32,
         63 as i32];
    let mut param2: [i32; 10] =
        [68 as i32, 49 as i32, 44 as i32,
         9 as i32, 13 as i32, 5 as i32,
         20 as i32, 13 as i32, 45 as i32,
         56 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize] as u32,
                    param2[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize] as u32,
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
