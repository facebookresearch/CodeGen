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

pub unsafe fn f_gold(mut a: i32, mut b: i32,
                                mut c: i32) -> bool {
    if a + b <= c || a + c <= b || b + c <= a {
        return 0 as i32 != 0
    } else { return 1 as i32 != 0 };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [29 as i32, 83 as i32, 48 as i32,
         59 as i32, 56 as i32, 68 as i32,
         63 as i32, 95 as i32, 2 as i32,
         11 as i32];
    let mut param1: [i32; 10] =
        [19 as i32, 34 as i32, 14 as i32,
         12 as i32, 39 as i32, 85 as i32,
         36 as i32, 34 as i32, 90 as i32,
         16 as i32];
    let mut param2: [i32; 10] =
        [52 as i32, 49 as i32, 65 as i32,
         94 as i32, 22 as i32, 9 as i32,
         41 as i32, 37 as i32, 27 as i32,
         1 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize]) as i32 ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize]) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
