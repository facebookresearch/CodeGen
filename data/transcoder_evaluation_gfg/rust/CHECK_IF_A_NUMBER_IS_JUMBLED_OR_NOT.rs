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

pub unsafe fn f_gold(mut num: i32) -> bool {
    if num / 10 as i32 == 0 as i32 {
        return 1 as i32 != 0
    }
    while num != 0 as i32 {
        if num / 10 as i32 == 0 as i32 {
            return 1 as i32 != 0
        }
        let mut digit1: i32 = num % 10 as i32;
        let mut digit2: i32 =
            num / 10 as i32 % 10 as i32;
        if abs(digit2 - digit1) > 1 as i32 {
            return 0 as i32 != 0
        }
        num = num / 10 as i32
    }
    return 1 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [67 as i32, 77 as i32, 35 as i32,
         79 as i32, 45 as i32, 22 as i32,
         68 as i32, 17 as i32, 5 as i32,
         85 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize]) as i32 ==
               f_gold(param0[i as usize]) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
