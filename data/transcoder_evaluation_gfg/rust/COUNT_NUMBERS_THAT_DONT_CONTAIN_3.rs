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

pub unsafe fn f_gold(mut n: i32) -> i32 {
    if n < 3 as i32 { return n }
    if n >= 3 as i32 && n < 10 as i32 {
        return n - 1 as i32
    }
    let mut po: i32 = 1 as i32;
    while n / po > 9 as i32 { po = po * 10 as i32 }
    let mut msd: i32 = n / po;
    if msd != 3 as i32 {
        return f_gold(msd) * f_gold(po - 1 as i32) + f_gold(msd) +
                   f_gold(n % po)
    } else { return f_gold(msd * po - 1 as i32) };
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [85 as i32, 86 as i32, 3 as i32,
         35 as i32, 59 as i32, 38 as i32,
         33 as i32, 15 as i32, 75 as i32,
         74 as i32];
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
