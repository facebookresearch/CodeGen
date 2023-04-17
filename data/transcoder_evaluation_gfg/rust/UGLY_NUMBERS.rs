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
    let vla = n as usize;
    let mut ugly: Vec<u32> = ::std::vec::from_elem(0, vla);
    let mut i2: u32 = 0 as i32 as u32;
    let mut i3: u32 = 0 as i32 as u32;
    let mut i5: u32 = 0 as i32 as u32;
    let mut next_multiple_of_2: u32 =
        2 as i32 as u32;
    let mut next_multiple_of_3: u32 =
        3 as i32 as u32;
    let mut next_multiple_of_5: u32 =
        5 as i32 as u32;
    let mut next_ugly_no: u32 = 1 as i32 as u32;
    *ugly.as_mut_ptr().offset(0 as i32 as isize) =
        1 as i32 as u32;
    let mut i: i32 = 1 as i32;
    while (i as u32) < n {
        next_ugly_no =
            min(next_multiple_of_2 as i32,
                min(next_multiple_of_3 as i32,
                    next_multiple_of_5 as i32)) as u32;
        *ugly.as_mut_ptr().offset(i as isize) = next_ugly_no;
        if next_ugly_no == next_multiple_of_2 {
            i2 = i2.wrapping_add(1 as i32 as u32);
            next_multiple_of_2 =
                (*ugly.as_mut_ptr().offset(i2 as
                                               isize)).wrapping_mul(2 as
                                                                        i32
                                                                        as
                                                                        u32)
        }
        if next_ugly_no == next_multiple_of_3 {
            i3 = i3.wrapping_add(1 as i32 as u32);
            next_multiple_of_3 =
                (*ugly.as_mut_ptr().offset(i3 as
                                               isize)).wrapping_mul(3 as
                                                                        i32
                                                                        as
                                                                        u32)
        }
        if next_ugly_no == next_multiple_of_5 {
            i5 = i5.wrapping_add(1 as i32 as u32);
            next_multiple_of_5 =
                (*ugly.as_mut_ptr().offset(i5 as
                                               isize)).wrapping_mul(5 as
                                                                        i32
                                                                        as
                                                                        u32)
        }
        i += 1
    }
    return next_ugly_no;
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [i32; 10] =
        [27 as i32, 64 as i32, 93 as i32,
         90 as i32, 85 as i32, 86 as i32,
         72 as i32, 86 as i32, 32 as i32,
         1 as i32];
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
