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
    if n <= 1 as i32 { return 0 as i32 != 0 }
    if n <= 3 as i32 { return 1 as i32 != 0 }
    if n % 2 as i32 == 0 as i32 ||
           n % 3 as i32 == 0 as i32 {
        return 0 as i32 != 0
    }
    let mut i: i32 = 5 as i32;
    while i * i <= n {
        if n % i == 0 as i32 ||
               n % (i + 2 as i32) == 0 as i32 {
            return 0 as i32 != 0
        }
        i = i + 6 as i32
    }
    return 1 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [15 as i32, 90 as i32, 38 as i32,
         65 as i32, 91 as i32, 16 as i32,
         48 as i32, 74 as i32, 14 as i32,
         47 as i32];
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
