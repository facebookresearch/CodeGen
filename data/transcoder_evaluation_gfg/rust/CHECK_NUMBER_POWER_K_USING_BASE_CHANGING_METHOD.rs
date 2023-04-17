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

pub unsafe fn f_gold(mut n: u32, mut k: u32)
 -> bool {
    let mut oneSeen: bool = 0 as i32 != 0;
    while n > 0 as i32 as u32 {
        let mut digit: i32 = n.wrapping_rem(k) as i32;
        if digit > 1 as i32 { return 0 as i32 != 0 }
        if digit == 1 as i32 {
            if oneSeen { return 0 as i32 != 0 }
            oneSeen = 1 as i32 != 0
        }
        n = n.wrapping_div(k)
    }
    return 1 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [64 as i32, 16 as i32, 27 as i32,
         81 as i32, 1 as i32, 69 as i32,
         8 as i32, 31 as i32, 43 as i32,
         54 as i32];
    let mut param1: [i32; 10] =
        [4 as i32, 2 as i32, 3 as i32,
         72 as i32, 9 as i32, 17 as i32,
         20 as i32, 79 as i32, 81 as i32,
         89 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize] as u32,
                    param1[i as usize] as u32) as i32 ==
               f_gold(param0[i as usize] as u32,
                      param1[i as usize] as u32) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
