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

pub unsafe fn f_gold(mut n: i32) -> i32 {
    let mut odd_count: i32 = 0 as i32;
    let mut even_count: i32 = 0 as i32;
    if n < 0 as i32 { n = -n }
    if n == 0 as i32 { return 1 as i32 }
    if n == 1 as i32 { return 0 as i32 }
    while n != 0 {
        if n & 1 as i32 != 0 { odd_count += 1 }
        if n & 2 as i32 != 0 { even_count += 1 }
        n = n >> 2 as i32
    }
    return f_gold(abs(odd_count - even_count));
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [94 as i32, 94 as i32, 79 as i32,
         39 as i32, 16 as i32, 90 as i32,
         64 as i32, 76 as i32, 83 as i32,
         47 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize]) == f_gold(param0[i as usize]) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
