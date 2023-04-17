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

pub unsafe fn f_gold(mut s: i32) -> i32 {
    let mut maxvalue: i32 = 0 as i32;
    let mut i: i32 = 1 as i32;
    while i <= s - 2 as i32 {
        let mut j: i32 = 1 as i32;
        while j <= s - 1 as i32 {
            let mut k: i32 = s - i - j;
            maxvalue = max(maxvalue, i * j * k);
            j += 1
        }
        i += 1
    }
    return maxvalue;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [67 as i32, 48 as i32, 59 as i32,
         22 as i32, 14 as i32, 66 as i32,
         1 as i32, 75 as i32, 58 as i32,
         78 as i32];
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
