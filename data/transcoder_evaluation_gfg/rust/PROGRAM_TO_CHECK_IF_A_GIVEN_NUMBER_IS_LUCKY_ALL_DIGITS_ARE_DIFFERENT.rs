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

pub unsafe fn f_gold(mut n: i32) -> bool {
    let mut arr: [bool; 10] = [false; 10];
    let mut i: i32 = 0 as i32;
    while i < 10 as i32 {
        arr[i as usize] = 0 as i32 != 0;
        i += 1
    }
    while n > 0 as i32 {
        let mut digit: i32 = n % 10 as i32;
        if arr[digit as usize] { return 0 as i32 != 0 }
        arr[digit as usize] = 1 as i32 != 0;
        n = n / 10 as i32
    }
    return 1 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [474 as i32, 9445 as i32, 90 as i32,
         30 as i32, 37453 as i32, 27 as i32,
         2400 as i32, 98 as i32, 46 as i32,
         722 as i32];
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
