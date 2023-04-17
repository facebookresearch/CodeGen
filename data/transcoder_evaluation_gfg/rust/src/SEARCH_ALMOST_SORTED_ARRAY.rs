#![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case,
         non_upper_case_globals, unused_assignments, unused_mut)]
#![register_tool(c2rust)]
#![feature(main, register_tool)]
extern "C" {
    #[no_mangle]
    fn printf(_: *const libc::c_char, _: ...) -> libc::c_int;
    #[no_mangle]
    fn qsort(__base: *mut libc::c_void, __nmemb: size_t, __size: size_t,
             __compar: __compar_fn_t);
}
pub type size_t = libc::c_ulong;
pub type __compar_fn_t
    =
    Option<unsafe extern "C" fn(_: *const libc::c_void,
                                _: *const libc::c_void) -> libc::c_int>;
// Copyright (c) 2019-present, Facebook, Inc.
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.
//
#[no_mangle]
pub unsafe extern "C" fn min(mut x: libc::c_int, mut y: libc::c_int)
 -> libc::c_int {
    return if x < y { x } else { y };
}
#[no_mangle]
pub unsafe extern "C" fn max(mut x: libc::c_int, mut y: libc::c_int)
 -> libc::c_int {
    return if x > y { x } else { y };
}
#[no_mangle]
pub unsafe extern "C" fn cmpfunc(mut a: *const libc::c_void,
                                 mut b: *const libc::c_void) -> libc::c_int {
    return *(a as *mut libc::c_int) - *(b as *mut libc::c_int);
}
#[no_mangle]
pub unsafe extern "C" fn len(mut arr: *mut libc::c_int) -> libc::c_int {
    return (::std::mem::size_of::<*mut libc::c_int>() as
                libc::c_ulong).wrapping_div(::std::mem::size_of::<libc::c_int>()
                                                as libc::c_ulong) as
               libc::c_int;
}
#[no_mangle]
pub unsafe extern "C" fn sort(mut arr: *mut libc::c_int, mut n: libc::c_int) {
    qsort(arr as *mut libc::c_void, n as size_t,
          ::std::mem::size_of::<libc::c_int>() as libc::c_ulong,
          Some(cmpfunc as
                   unsafe extern "C" fn(_: *const libc::c_void,
                                        _: *const libc::c_void)
                       -> libc::c_int));
}
#[no_mangle]
pub unsafe extern "C" fn f_gold(mut arr: *mut libc::c_int, mut l: libc::c_int,
                                mut r: libc::c_int, mut x: libc::c_int)
 -> libc::c_int {
    if r >= l {
        let mut mid: libc::c_int = l + (r - l) / 2 as libc::c_int;
        if *arr.offset(mid as isize) == x { return mid }
        if mid > l && *arr.offset((mid - 1 as libc::c_int) as isize) == x {
            return mid - 1 as libc::c_int
        }
        if mid < r && *arr.offset((mid + 1 as libc::c_int) as isize) == x {
            return mid + 1 as libc::c_int
        }
        if *arr.offset(mid as isize) > x {
            return f_gold(arr, l, mid - 2 as libc::c_int, x)
        }
        return f_gold(arr, mid + 2 as libc::c_int, r, x)
    }
    return -(1 as libc::c_int);
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut arr: *mut libc::c_int,
                                  mut l: libc::c_int, mut r: libc::c_int,
                                  mut x: libc::c_int) -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0_0: [libc::c_int; 3] =
        [75 as libc::c_int, 91 as libc::c_int, 93 as libc::c_int];
    let mut param0_1: [libc::c_int; 5] =
        [-(92 as libc::c_int), -(96 as libc::c_int), -(68 as libc::c_int),
         -(40 as libc::c_int), 70 as libc::c_int];
    let mut param0_2: [libc::c_int; 5] =
        [-(92 as libc::c_int), -(86 as libc::c_int), -(68 as libc::c_int),
         -(40 as libc::c_int), 70 as libc::c_int];
    let mut param0_3: [libc::c_int; 8] =
        [-(3 as libc::c_int), -(1 as libc::c_int), 0 as libc::c_int,
         30 as libc::c_int, 10 as libc::c_int, 45 as libc::c_int,
         70 as libc::c_int, 60 as libc::c_int];
    let mut param0_4: [libc::c_int; 8] =
        [-(3 as libc::c_int), -(1 as libc::c_int), 0 as libc::c_int,
         10 as libc::c_int, 5 as libc::c_int, 45 as libc::c_int,
         60 as libc::c_int, 50 as libc::c_int];
    let mut param0_5: [libc::c_int; 8] =
        [-(3 as libc::c_int), -(1 as libc::c_int), 0 as libc::c_int,
         10 as libc::c_int, 30 as libc::c_int, 45 as libc::c_int,
         60 as libc::c_int, 70 as libc::c_int];
    let mut param0_6: [libc::c_int; 3] =
        [0 as libc::c_int, 0 as libc::c_int, 1 as libc::c_int];
    let mut param0_7: [libc::c_int; 3] =
        [1 as libc::c_int, 1 as libc::c_int, 1 as libc::c_int];
    let mut param0_8: [libc::c_int; 4] =
        [30 as libc::c_int, 2 as libc::c_int, 30 as libc::c_int,
         45 as libc::c_int];
    let mut param0: [*mut libc::c_int; 9] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr(),
         param0_6.as_mut_ptr(), param0_7.as_mut_ptr(), param0_8.as_mut_ptr()];
    let mut param1: [libc::c_int; 10] =
        [0 as libc::c_int, 0 as libc::c_int, 0 as libc::c_int,
         0 as libc::c_int, 0 as libc::c_int, 0 as libc::c_int,
         0 as libc::c_int, 0 as libc::c_int, 0 as libc::c_int,
         0 as libc::c_int];
    let mut param2: [libc::c_int; 10] =
        [15 as libc::c_int, 15 as libc::c_int, 4 as libc::c_int,
         4 as libc::c_int, 7 as libc::c_int, 7 as libc::c_int,
         7 as libc::c_int, 2 as libc::c_int, 2 as libc::c_int,
         3 as libc::c_int];
    let mut param3: [libc::c_int; 10] =
        [71 as libc::c_int, 71 as libc::c_int, -(96 as libc::c_int),
         20 as libc::c_int, 0 as libc::c_int, 12 as libc::c_int,
         18 as libc::c_int, 20 as libc::c_int, 17 as libc::c_int,
         28 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if f_filled(param0[i as usize], param1[i as usize],
                    param2[i as usize], param3[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize],
                      param2[i as usize], param3[i as usize]) {
            n_success += 1 as libc::c_int
        }
        i += 1
    }
    printf(b"#Results:\x00" as *const u8 as *const libc::c_char,
           b" \x00" as *const u8 as *const libc::c_char, n_success,
           b", \x00" as *const u8 as *const libc::c_char,
           len(param0.as_mut_ptr() as *mut libc::c_int));
    return 0 as libc::c_int;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
