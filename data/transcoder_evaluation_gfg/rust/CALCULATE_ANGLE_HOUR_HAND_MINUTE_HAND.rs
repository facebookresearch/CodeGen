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

pub unsafe fn f_gold(mut h: f64, mut m: f64)
 -> i32 {
    if h < 0 as i32 as f64 ||
           m < 0 as i32 as f64 ||
           h > 12 as i32 as f64 ||
           m > 60 as i32 as f64 {
        println!("Wrong input");
    }
    if h == 12 as i32 as f64 {
        h = 0 as i32 as f64
    }
    if m == 60 as i32 as f64 {
        m = 0 as i32 as f64
    }
    let mut hour_angle: i32 =
        (0.5f64 * (h * 60 as i32 as f64 + m)) as
            i32;
    let mut minute_angle: i32 =
        (6 as i32 as f64 * m) as i32;
    let mut angle: i32 = abs(hour_angle - minute_angle);
    angle = min(360 as i32 - angle, angle);
    return angle;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [f64; 10] =
        [7322.337365895532f64, -0.5025472034247969f64, 8735.336068205026f64,
         -5478.862697905712f64, 8264.126919165505f64, -9671.311773842834f64,
         9995.328351000411f64, -5274.574323066984f64, 1310.8711644223736f64,
         -2829.678131972794f64];
    let mut param1: [f64; 10] =
        [6996.326968156217f64, -2910.070017192333f64, 1910.3752934680874f64,
         -9470.18148108585f64, 7058.937313484608f64, -3867.070379361206f64,
         2145.339179488316f64, -3583.7503371694124f64, 5214.059687285893f64,
         -9371.556600288217f64];
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
