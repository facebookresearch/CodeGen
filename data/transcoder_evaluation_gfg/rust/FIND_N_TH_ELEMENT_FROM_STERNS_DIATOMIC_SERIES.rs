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
    let vla = (n + 1 as i32) as usize;
    let mut DP: Vec<i32> = ::std::vec::from_elem(0, vla);
    *DP.as_mut_ptr().offset(0 as i32 as isize) = 0 as i32;
    *DP.as_mut_ptr().offset(1 as i32 as isize) = 1 as i32;
    let mut i: i32 = 2 as i32;
    while i <= n {
        if i % 2 as i32 == 0 as i32 {
            *DP.as_mut_ptr().offset(i as isize) =
                *DP.as_mut_ptr().offset((i / 2 as i32) as isize)
        } else {
            *DP.as_mut_ptr().offset(i as isize) =
                *DP.as_mut_ptr().offset(((i - 1 as i32) /
                                             2 as i32) as isize) +
                    *DP.as_mut_ptr().offset(((i + 1 as i32) /
                                                 2 as i32) as isize)
        }
        i += 1
    }
    return *DP.as_mut_ptr().offset(n as isize);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [37 as i32, 24 as i32, 13 as i32,
         56 as i32, 26 as i32, 67 as i32,
         82 as i32, 60 as i32, 64 as i32,
         65 as i32];
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
