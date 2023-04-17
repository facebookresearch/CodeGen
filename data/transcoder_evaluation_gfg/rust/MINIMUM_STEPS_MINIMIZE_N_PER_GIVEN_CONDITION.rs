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
    let mut table: Vec<i32> = ::std::vec::from_elem(0, vla);
    let mut i: i32 = 0 as i32;
    while i <= n { *table.as_mut_ptr().offset(i as isize) = n - i; i += 1 }
    let mut i_0: i32 = n;
    while i_0 >= 1 as i32 {
        if i_0 % 2 as i32 == 0 {
            *table.as_mut_ptr().offset((i_0 / 2 as i32) as isize) =
                min(*table.as_mut_ptr().offset(i_0 as isize) +
                        1 as i32,
                    *table.as_mut_ptr().offset((i_0 / 2 as i32) as
                                                   isize))
        }
        if i_0 % 3 as i32 == 0 {
            *table.as_mut_ptr().offset((i_0 / 3 as i32) as isize) =
                min(*table.as_mut_ptr().offset(i_0 as isize) +
                        1 as i32,
                    *table.as_mut_ptr().offset((i_0 / 3 as i32) as
                                                   isize))
        }
        i_0 -= 1
    }
    return *table.as_mut_ptr().offset(1 as i32 as isize);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [59 as i32, 7 as i32, 90 as i32,
         78 as i32, 49 as i32, 15 as i32,
         45 as i32, 56 as i32, 7 as i32,
         70 as i32];
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
