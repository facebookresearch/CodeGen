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

pub unsafe fn f_gold(mut arr: *mut i32, mut l: i32,
                                mut r: i32, mut x: i32)
 -> i32 {
    if r < l { return -(1 as i32) }
    if *arr.offset(l as isize) == x { return l }
    if *arr.offset(r as isize) == x { return r }
    return f_gold(arr, l + 1 as i32, r - 1 as i32, x);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0_0: [i32; 3] =
        [10 as i32, 74 as i32, 3 as i32];
    let mut param0_1: [i32; 8] =
        [-(90 as i32), 72 as i32, 36 as i32,
         96 as i32, 42 as i32, 0 as i32,
         -(66 as i32), 4 as i32];
    let mut param0_2: [i32; 1] = [0 as i32];
    let mut param0_3: [i32; 4] =
        [99 as i32, 70 as i32, 67 as i32,
         5 as i32];
    let mut param0_4: [i32; 9] =
        [-(98 as i32), -(98 as i32), -(26 as i32),
         -(26 as i32), -(24 as i32), -(18 as i32),
         -(16 as i32), 80 as i32, 5 as i32];
    let mut param0_5: [i32; 7] =
        [1 as i32, 1 as i32, 1 as i32,
         1 as i32, 0 as i32, 1 as i32,
         0 as i32];
    let mut param0_6: [i32; 11] =
        [1 as i32, 5 as i32, 12 as i32,
         12 as i32, 17 as i32, 17 as i32,
         12 as i32, 95 as i32, 96 as i32,
         98 as i32, 4 as i32];
    let mut param0_7: [i32; 9] =
        [50 as i32, -(70 as i32), -(30 as i32),
         -(54 as i32), 6 as i32, -(10 as i32),
         70 as i32, 84 as i32, 5 as i32];
    let mut param0_8: [i32; 3] =
        [0 as i32, 1 as i32, 5 as i32];
    let mut param0_9: [i32; 6] =
        [59 as i32, 21 as i32, 28 as i32,
         3 as i32, 14 as i32, 5 as i32];
    let mut param0: [*mut i32; 10] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr(),
         param0_6.as_mut_ptr(), param0_7.as_mut_ptr(), param0_8.as_mut_ptr(),
         param0_9.as_mut_ptr()];
    let mut param1: [i32; 10] =
        [0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32];
    let mut param2: [i32; 10] =
        [2 as i32, 7 as i32, 1 as i32,
         3 as i32, 8 as i32, 6 as i32,
         10 as i32, 8 as i32, 2 as i32,
         5 as i32];
    let mut param3: [i32; 10] =
        [1 as i32, 96 as i32, -(1 as i32),
         3 as i32, 80 as i32, 1 as i32,
         12 as i32, 27 as i32, 14 as i32,
         28 as i32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize], param3[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize], param3[i as usize]) {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
