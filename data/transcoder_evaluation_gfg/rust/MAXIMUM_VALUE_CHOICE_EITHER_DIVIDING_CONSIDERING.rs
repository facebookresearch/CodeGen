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
    let mut res: Vec<i32> = ::std::vec::from_elem(0, vla);
    *res.as_mut_ptr().offset(0 as i32 as isize) = 0 as i32;
    *res.as_mut_ptr().offset(1 as i32 as isize) = 1 as i32;
    let mut i: i32 = 2 as i32;
    while i <= n {
        *res.as_mut_ptr().offset(i as isize) =
            max(i,
                *res.as_mut_ptr().offset((i / 2 as i32) as isize) +
                    *res.as_mut_ptr().offset((i / 3 as i32) as isize)
                    +
                    *res.as_mut_ptr().offset((i / 4 as i32) as isize)
                    +
                    *res.as_mut_ptr().offset((i / 5 as i32) as
                                                 isize));
        i += 1
    }
    return *res.as_mut_ptr().offset(n as isize);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [3 as i32, 19 as i32, 39 as i32,
         89 as i32, 96 as i32, 68 as i32,
         48 as i32, 5 as i32, 3 as i32,
         4 as i32];
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
