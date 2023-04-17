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
    let vla = n as usize;
    let vla_0 = n as usize;
    let mut arr: Vec<i32> = ::std::vec::from_elem(0, vla * vla_0);
    let mut i: i32 = 0 as i32;
    while i < n {
        let mut j: i32 = 0 as i32;
        while j < n {
            *arr.as_mut_ptr().offset(i as isize *
                                         vla_0 as isize).offset(j as isize) =
                abs(i - j);
            j += 1
        }
        i += 1
    }
    let mut sum: i32 = 0 as i32;
    let mut i_0: i32 = 0 as i32;
    while i_0 < n {
        let mut j_0: i32 = 0 as i32;
        while j_0 < n {
            sum +=
                *arr.as_mut_ptr().offset(i_0 as isize *
                                             vla_0 as
                                                 isize).offset(j_0 as isize);
            j_0 += 1
        }
        i_0 += 1
    }
    return sum;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [60 as i32, 44 as i32, 72 as i32,
         90 as i32, 99 as i32, 45 as i32,
         27 as i32, 11 as i32, 65 as i32,
         52 as i32];
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
