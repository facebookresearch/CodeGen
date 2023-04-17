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

pub unsafe fn f_gold(mut n: i32, mut p: i32)
 -> i32 {
    let mut ans: i32 = 0 as i32;
    let mut temp: i32 = p;
    while temp <= n { ans += n / temp; temp = temp * p }
    return ans;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [49 as i32, 80 as i32, 10 as i32,
         81 as i32, 11 as i32, 45 as i32,
         86 as i32, 27 as i32, 80 as i32,
         97 as i32];
    let mut param1: [i32; 10] =
        [30 as i32, 25 as i32, 9 as i32,
         57 as i32, 4 as i32, 34 as i32,
         90 as i32, 78 as i32, 60 as i32,
         31 as i32];
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
