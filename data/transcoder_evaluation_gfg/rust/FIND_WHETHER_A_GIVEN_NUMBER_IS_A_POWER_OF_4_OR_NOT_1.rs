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

pub unsafe fn f_gold(mut n: u32) -> bool {
    let mut count: i32 = 0 as i32;
    if n != 0 && n & n.wrapping_sub(1 as i32 as u32) == 0 {
        while n > 1 as i32 as u32 {
            n >>= 1 as i32;
            count += 1 as i32
        }
        return if count % 2 as i32 == 0 as i32 {
                   1 as i32
               } else { 0 as i32 } != 0
    }
    return 0 as i32 != 0;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [1 as i32, 4 as i32, 64 as i32,
         -(64 as i32), 128 as i32, 1024 as i32,
         45 as i32, 33 as i32, 66 as i32,
         74 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize] as u32) as i32 ==
               f_gold(param0[i as usize] as u32) as i32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
