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

pub unsafe fn f_gold(mut n: u32) -> u32 {
    let mut count: u32 = 0 as i32 as u32;
    if n != 0 && n & n.wrapping_sub(1 as i32 as u32) == 0 {
        return n
    }
    while n != 0 as i32 as u32 {
        n >>= 1 as i32;
        count = count.wrapping_add(1 as i32 as u32)
    }
    return ((1 as i32) << count) as u32;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [13 as i32, 27 as i32, 1 as i32,
         24 as i32, 98 as i32, 94 as i32,
         36 as i32, 41 as i32, 74 as i32,
         39 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize] as u32) ==
               f_gold(param0[i as usize] as u32) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
