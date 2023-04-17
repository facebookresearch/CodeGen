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

pub unsafe fn f_gold(mut a: i32, mut b: i32)
 -> i32 {
    let mut cnt: i32 = 0 as i32;
    let mut i: i32 = a;
    while i <= b {
        let mut j: i32 = 1 as i32;
        while j * j <= i { if j * j == i { cnt += 1 } j += 1 }
        i += 1
    }
    return cnt;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [48 as i32, 3 as i32, 20 as i32,
         98 as i32, 96 as i32, 40 as i32,
         9 as i32, 57 as i32, 28 as i32,
         98 as i32];
    let mut param1: [i32; 10] =
        [42 as i32, 82 as i32, 72 as i32,
         98 as i32, 90 as i32, 82 as i32,
         15 as i32, 77 as i32, 80 as i32,
         75 as i32];
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
