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
    #[no_mangle]
    fn abs(_: libc::c_int) -> libc::c_int;
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
pub unsafe extern "C" fn f_gold(mut input: libc::c_int,
                                mut unlock_code: libc::c_int) -> libc::c_int {
    let mut rotation: libc::c_int = 0 as libc::c_int;
    let mut input_digit: libc::c_int = 0;
    let mut code_digit: libc::c_int = 0;
    while input != 0 || unlock_code != 0 {
        input_digit = input % 10 as libc::c_int;
        code_digit = unlock_code % 10 as libc::c_int;
        rotation +=
            min(abs(input_digit - code_digit),
                10 as libc::c_int - abs(input_digit - code_digit));
        input /= 10 as libc::c_int;
        unlock_code /= 10 as libc::c_int
    }
    return rotation;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut input: libc::c_int,
                                  mut unlock_code: libc::c_int)
 -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_int; 10] =
        [71 as libc::c_int, 90 as libc::c_int, 28 as libc::c_int,
         41 as libc::c_int, 32 as libc::c_int, 39 as libc::c_int,
         33 as libc::c_int, 89 as libc::c_int, 50 as libc::c_int,
         92 as libc::c_int];
    let mut param1: [libc::c_int; 10] =
        [46 as libc::c_int, 65 as libc::c_int, 84 as libc::c_int,
         23 as libc::c_int, 58 as libc::c_int, 82 as libc::c_int,
         58 as libc::c_int, 32 as libc::c_int, 51 as libc::c_int,
         77 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr()) {
        if f_filled(param0[i as usize], param1[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize]) {
            n_success += 1 as libc::c_int
        }
        i += 1
    }
    printf(b"#Results:\x00" as *const u8 as *const libc::c_char,
           b" \x00" as *const u8 as *const libc::c_char, n_success,
           b", \x00" as *const u8 as *const libc::c_char,
           len(param0.as_mut_ptr()));
    return 0 as libc::c_int;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
