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

pub unsafe fn f_gold(mut a: f64, mut b: f64)
 -> f64 {
    let mut mod_0: f64 = 0.;
    if a < 0 as i32 as f64 {
        mod_0 = -a
    } else { mod_0 = a }
    if b < 0 as i32 as f64 { b = -b }
    while mod_0 >= b { mod_0 = mod_0 - b }
    if a < 0 as i32 as f64 { return -mod_0 }
    return mod_0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [f64; 10] =
        [3243.229719038493f64, -4362.665881044217f64, 7255.066257575837f64,
         -6929.554320261099f64, 3569.942027998315f64, -6513.849053096595f64,
         7333.183189243961f64, -2856.1752826258803f64, 9787.228111241662f64,
         -1722.873699288031f64];
    let mut param1: [f64; 10] =
        [5659.926861939672f64, -9196.507113304497f64, 2623.200060506935f64,
         -3009.0234530313287f64, 6920.809419868375f64, -70.95992406437102f64,
         580.3500610971768f64, -9625.97442825802f64, 2419.6844962423256f64,
         -8370.700544254058f64];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if (abs((1 as i32 as f64 -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize], param1[i as usize])
                                  as i32) as f64) /
                         (abs(f_filled(param0[i as usize], param1[i as usize])
                                  as i32) as f64 +
                              0.0000001f64)) as i32) as
                f64) < 0.001f64 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
