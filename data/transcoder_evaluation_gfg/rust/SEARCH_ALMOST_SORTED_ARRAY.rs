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
    if r >= l {
        let mut mid: i32 = l + (r - l) / 2 as i32;
        if *arr.offset(mid as isize) == x { return mid }
        if mid > l && *arr.offset((mid - 1 as i32) as isize) == x {
            return mid - 1 as i32
        }
        if mid < r && *arr.offset((mid + 1 as i32) as isize) == x {
            return mid + 1 as i32
        }
        if *arr.offset(mid as isize) > x {
            return f_gold(arr, l, mid - 2 as i32, x)
        }
        return f_gold(arr, mid + 2 as i32, r, x)
    }
    return -(1 as i32);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0_0: [i32; 3] =
        [75 as i32, 91 as i32, 93 as i32];
    let mut param0_1: [i32; 5] =
        [-(92 as i32), -(96 as i32), -(68 as i32),
         -(40 as i32), 70 as i32];
    let mut param0_2: [i32; 5] =
        [-(92 as i32), -(86 as i32), -(68 as i32),
         -(40 as i32), 70 as i32];
    let mut param0_3: [i32; 8] =
        [-(3 as i32), -(1 as i32), 0 as i32,
         30 as i32, 10 as i32, 45 as i32,
         70 as i32, 60 as i32];
    let mut param0_4: [i32; 8] =
        [-(3 as i32), -(1 as i32), 0 as i32,
         10 as i32, 5 as i32, 45 as i32,
         60 as i32, 50 as i32];
    let mut param0_5: [i32; 8] =
        [-(3 as i32), -(1 as i32), 0 as i32,
         10 as i32, 30 as i32, 45 as i32,
         60 as i32, 70 as i32];
    let mut param0_6: [i32; 3] =
        [0 as i32, 0 as i32, 1 as i32];
    let mut param0_7: [i32; 3] =
        [1 as i32, 1 as i32, 1 as i32];
    let mut param0_8: [i32; 4] =
        [30 as i32, 2 as i32, 30 as i32,
         45 as i32];
    let mut param0: [*mut i32; 9] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr(),
         param0_6.as_mut_ptr(), param0_7.as_mut_ptr(), param0_8.as_mut_ptr()];
    let mut param1: [i32; 10] =
        [0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32, 0 as i32, 0 as i32,
         0 as i32];
    let mut param2: [i32; 10] =
        [15 as i32, 15 as i32, 4 as i32,
         4 as i32, 7 as i32, 7 as i32,
         7 as i32, 2 as i32, 2 as i32,
         3 as i32];
    let mut param3: [i32; 10] =
        [71 as i32, 71 as i32, -(96 as i32),
         20 as i32, 0 as i32, 12 as i32,
         18 as i32, 20 as i32, 17 as i32,
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
