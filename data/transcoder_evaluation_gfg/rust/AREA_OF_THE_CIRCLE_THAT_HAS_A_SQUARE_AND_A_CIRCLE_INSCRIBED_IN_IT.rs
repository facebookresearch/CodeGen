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

pub unsafe fn f_gold(mut a: i32) -> f32 {
    let mut area: f32 =
        (3.14159265358979323846f64 * a as f64 * a as f64
             / 4.0f64) as f32;
    return area;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [77 as i32, 18 as i32, 83 as i32,
         39 as i32, 68 as i32, 28 as i32,
         71 as i32, 14 as i32, 21 as i32,
         73 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if (abs((1 as i32 as f64 -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize]) as i32) as
                              f64) /
                         (abs(f_filled(param0[i as usize]) as i32) as
                              f64 + 0.0000001f64)) as i32)
                as f32) < 0.001f32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
