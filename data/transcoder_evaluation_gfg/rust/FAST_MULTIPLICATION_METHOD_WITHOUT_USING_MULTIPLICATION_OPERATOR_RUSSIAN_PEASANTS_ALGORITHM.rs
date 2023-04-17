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

pub unsafe fn f_gold(mut a: u32, mut b: u32)
 -> u32 {
    let mut res: i32 = 0 as i32;
    while b > 0 as i32 as u32 {
        if b & 1 as i32 as u32 != 0 {
            res = (res as u32).wrapping_add(a) as i32
        }
        a = a << 1 as i32;
        b = b >> 1 as i32
    }
    return res as u32;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [4 as i32, 36 as i32, 65 as i32,
         55 as i32, 35 as i32, 69 as i32,
         84 as i32, 5 as i32, 15 as i32,
         67 as i32];
    let mut param1: [i32; 10] =
        [33 as i32, 67 as i32, 52 as i32,
         37 as i32, 76 as i32, 98 as i32,
         62 as i32, 80 as i32, 36 as i32,
         84 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize] as u32,
                    param1[i as usize] as u32) ==
               f_gold(param0[i as usize] as u32,
                      param1[i as usize] as u32) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
