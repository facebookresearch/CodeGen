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

pub unsafe fn f_gold(mut a: f32, mut b: f32)
 -> f32 {
    return 2 as i32 as f32 * a +
               2 as i32 as f32 * b;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [f32; 10] =
        [801.0366882228715f32, -7069.610056819919f32, 7723.966966568705f32,
         -7935.859205856963f32, 6094.247432557289f32, -7371.490363309265f32,
         8368.473889617526f32, -3761.921143166053f32, 3139.1089185587884f32,
         -5218.286665567171f32];
    let mut param1: [f32; 10] =
        [456.71190645582783f32, -4226.483870778477f32, 5894.65405158763f32,
         -5333.225064296693f32, 1660.420120702062f32, -1095.4543576847332f32,
         4735.838330834498f32, -5315.871691690649f32, 6490.194159517967f32,
         -8265.153014320813f32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if (abs((1 as i32 as f64 -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize], param1[i as usize])
                                  as i32) as f64) /
                         (abs(f_filled(param0[i as usize], param1[i as usize])
                                  as i32) as f64 +
                              0.0000001f64)) as i32) as f32)
               < 0.001f32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
