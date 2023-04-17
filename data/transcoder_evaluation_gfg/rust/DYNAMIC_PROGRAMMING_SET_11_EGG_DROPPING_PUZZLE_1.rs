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

pub unsafe fn f_gold(mut n: i32, mut k: i32)
 -> i32 {
    let vla = (n + 1 as i32) as usize;
    let vla_0 = (k + 1 as i32) as usize;
    let mut eggFloor: Vec<i32> =
        ::std::vec::from_elem(0, vla * vla_0);
    let mut res: i32 = 0;
    let mut i: i32 = 0;
    let mut j: i32 = 0;
    let mut x: i32 = 0;
    i = 1 as i32;
    while i <= n {
        *eggFloor.as_mut_ptr().offset(i as isize *
                                          vla_0 as
                                              isize).offset(1 as i32
                                                                as isize) =
            1 as i32;
        *eggFloor.as_mut_ptr().offset(i as isize *
                                          vla_0 as
                                              isize).offset(0 as i32
                                                                as isize) =
            0 as i32;
        i += 1
    }
    j = 1 as i32;
    while j <= k {
        *eggFloor.as_mut_ptr().offset(1 as i32 as isize *
                                          vla_0 as isize).offset(j as isize) =
            j;
        j += 1
    }
    i = 2 as i32;
    while i <= n {
        j = 2 as i32;
        while j <= k {
            *eggFloor.as_mut_ptr().offset(i as isize *
                                              vla_0 as
                                                  isize).offset(j as isize) =
                2147483647 as i32;
            x = 1 as i32;
            while x <= j {
                res =
                    1 as i32 +
                        max(*eggFloor.as_mut_ptr().offset((i -
                                                               1 as
                                                                   i32)
                                                              as isize *
                                                              vla_0 as
                                                                  isize).offset((x
                                                                                     -
                                                                                     1
                                                                                         as
                                                                                         i32)
                                                                                    as
                                                                                    isize),
                            *eggFloor.as_mut_ptr().offset(i as isize *
                                                              vla_0 as
                                                                  isize).offset((j
                                                                                     -
                                                                                     x)
                                                                                    as
                                                                                    isize));
                if res <
                       *eggFloor.as_mut_ptr().offset(i as isize *
                                                         vla_0 as
                                                             isize).offset(j
                                                                               as
                                                                               isize)
                   {
                    *eggFloor.as_mut_ptr().offset(i as isize *
                                                      vla_0 as
                                                          isize).offset(j as
                                                                            isize)
                        = res
                }
                x += 1
            }
            j += 1
        }
        i += 1
    }
    return *eggFloor.as_mut_ptr().offset(n as isize *
                                             vla_0 as
                                                 isize).offset(k as isize);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [42 as i32, 16 as i32, 24 as i32,
         95 as i32, 49 as i32, 39 as i32,
         63 as i32, 17 as i32, 45 as i32,
         40 as i32];
    let mut param1: [i32; 10] =
        [34 as i32, 18 as i32, 3 as i32,
         58 as i32, 98 as i32, 92 as i32,
         68 as i32, 80 as i32, 41 as i32,
         91 as i32];
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
