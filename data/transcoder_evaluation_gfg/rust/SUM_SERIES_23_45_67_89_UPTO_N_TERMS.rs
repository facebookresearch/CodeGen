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

pub unsafe fn f_gold(mut n: i32) -> f64 {
    let mut i: i32 = 1 as i32;
    let mut res: f64 = 0.0f64;
    let mut sign: bool = 1 as i32 != 0;
    while n > 0 as i32 {
        n -= 1;
        if sign {
            sign = !sign;
            i += 1;
            i += 1;
            res = res + i as f64 / i as f64
        } else {
            sign = !sign;
            i += 1;
            i += 1;
            res = res - i as f64 / i as f64
        }
    }
    return res;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [49 as i32, 4 as i32, 60 as i32,
         90 as i32, 96 as i32, 29 as i32,
         86 as i32, 47 as i32, 77 as i32,
         87 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if (abs((1 as i32 as f64 -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize]) as i32) as
                              f64) /
                         (abs(f_filled(param0[i as usize]) as i32) as
                              f64 + 0.0000001f64)) as i32)
                as f64) < 0.001f64 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
