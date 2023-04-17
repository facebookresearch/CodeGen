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

pub unsafe fn f_gold(mut input: i32,
                                mut unlock_code: i32) -> i32 {
    let mut rotation: i32 = 0 as i32;
    let mut input_digit: i32 = 0;
    let mut code_digit: i32 = 0;
    while input != 0 || unlock_code != 0 {
        input_digit = input % 10 as i32;
        code_digit = unlock_code % 10 as i32;
        rotation +=
            min(abs(input_digit - code_digit),
                10 as i32 - abs(input_digit - code_digit));
        input /= 10 as i32;
        unlock_code /= 10 as i32
    }
    return rotation;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [71 as i32, 90 as i32, 28 as i32,
         41 as i32, 32 as i32, 39 as i32,
         33 as i32, 89 as i32, 50 as i32,
         92 as i32];
    let mut param1: [i32; 10] =
        [46 as i32, 65 as i32, 84 as i32,
         23 as i32, 58 as i32, 82 as i32,
         58 as i32, 32 as i32, 51 as i32,
         77 as i32];
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
