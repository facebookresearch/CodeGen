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
pub unsafe extern "C" fn f_gold(mut a: libc::c_longlong,
                                mut b: libc::c_longlong) -> bool {
    if a == 0 as libc::c_int as libc::c_longlong ||
           b == 0 as libc::c_int as libc::c_longlong {
        return 0 as libc::c_int != 0
    }
    let mut result: libc::c_longlong = a * b;
    if a == result / b {
        return 0 as libc::c_int != 0
    } else { return 1 as libc::c_int != 0 };
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut a: libc::c_longlong,
                                  mut b: libc::c_longlong) -> bool {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_long; 10] =
        [37 as libc::c_int as libc::c_long, 10000000000 as libc::c_long,
         10000000000 as libc::c_long,
         999999999 as libc::c_int as libc::c_long,
         39 as libc::c_int as libc::c_long, 92 as libc::c_int as libc::c_long,
         14 as libc::c_int as libc::c_long, 19 as libc::c_int as libc::c_long,
         14 as libc::c_int as libc::c_long,
         88 as libc::c_int as libc::c_long];
    let mut param1: [libc::c_long; 10] =
        [80 as libc::c_int as libc::c_long, -(10000000000 as libc::c_long),
         10000000000 as libc::c_long,
         999999999 as libc::c_int as libc::c_long,
         36 as libc::c_int as libc::c_long, 56 as libc::c_int as libc::c_long,
         21 as libc::c_int as libc::c_long, 38 as libc::c_int as libc::c_long,
         82 as libc::c_int as libc::c_long,
         41 as libc::c_int as libc::c_long];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if f_filled(param0[i as usize] as libc::c_longlong,
                    param1[i as usize] as libc::c_longlong) as libc::c_int ==
               f_gold(param0[i as usize] as libc::c_longlong,
                      param1[i as usize] as libc::c_longlong) as libc::c_int {
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
