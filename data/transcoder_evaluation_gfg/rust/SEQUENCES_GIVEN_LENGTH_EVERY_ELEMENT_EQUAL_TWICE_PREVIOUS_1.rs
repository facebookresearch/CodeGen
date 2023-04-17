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

pub unsafe fn f_gold(mut m: i32, mut n: i32)
 -> i32 {
    let vla = (m + 1 as i32) as usize;
    let vla_0 = (n + 1 as i32) as usize;
    let mut T: Vec<i32> = ::std::vec::from_elem(0, vla * vla_0);
    let mut i: i32 = 0 as i32;
    while i < m + 1 as i32 {
        let mut j: i32 = 0 as i32;
        while j < n + 1 as i32 {
            if i == 0 as i32 || j == 0 as i32 {
                *T.as_mut_ptr().offset(i as isize *
                                           vla_0 as isize).offset(j as isize)
                    = 0 as i32
            } else if i < j {
                *T.as_mut_ptr().offset(i as isize *
                                           vla_0 as isize).offset(j as isize)
                    = 0 as i32
            } else if j == 1 as i32 {
                *T.as_mut_ptr().offset(i as isize *
                                           vla_0 as isize).offset(j as isize)
                    = i
            } else {
                *T.as_mut_ptr().offset(i as isize *
                                           vla_0 as isize).offset(j as isize)
                    =
                    *T.as_mut_ptr().offset((i - 1 as i32) as isize *
                                               vla_0 as
                                                   isize).offset(j as isize) +
                        *T.as_mut_ptr().offset((i / 2 as i32) as isize
                                                   *
                                                   vla_0 as
                                                       isize).offset((j -
                                                                          1 as
                                                                              i32)
                                                                         as
                                                                         isize)
            }
            j += 1
        }
        i += 1
    }
    return *T.as_mut_ptr().offset(m as isize *
                                      vla_0 as isize).offset(n as isize);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [10 as i32, 5 as i32, 2 as i32,
         83 as i32, 91 as i32, 18 as i32,
         83 as i32, 98 as i32, 43 as i32,
         31 as i32];
    let mut param1: [i32; 10] =
        [4 as i32, 2 as i32, 8 as i32,
         7 as i32, 0 as i32, 53 as i32,
         41 as i32, 53 as i32, 37 as i32,
         20 as i32];
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
