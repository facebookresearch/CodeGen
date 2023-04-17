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
pub unsafe extern "C" fn f_gold(mut n: libc::c_uint) -> libc::c_uint {
    let vla = n as usize;
    let mut ugly: Vec<libc::c_uint> = ::std::vec::from_elem(0, vla);
    let mut i2: libc::c_uint = 0 as libc::c_int as libc::c_uint;
    let mut i3: libc::c_uint = 0 as libc::c_int as libc::c_uint;
    let mut i5: libc::c_uint = 0 as libc::c_int as libc::c_uint;
    let mut next_multiple_of_2: libc::c_uint =
        2 as libc::c_int as libc::c_uint;
    let mut next_multiple_of_3: libc::c_uint =
        3 as libc::c_int as libc::c_uint;
    let mut next_multiple_of_5: libc::c_uint =
        5 as libc::c_int as libc::c_uint;
    let mut next_ugly_no: libc::c_uint = 1 as libc::c_int as libc::c_uint;
    *ugly.as_mut_ptr().offset(0 as libc::c_int as isize) =
        1 as libc::c_int as libc::c_uint;
    let mut i: libc::c_int = 1 as libc::c_int;
    while (i as libc::c_uint) < n {
        next_ugly_no =
            min(next_multiple_of_2 as libc::c_int,
                min(next_multiple_of_3 as libc::c_int,
                    next_multiple_of_5 as libc::c_int)) as libc::c_uint;
        *ugly.as_mut_ptr().offset(i as isize) = next_ugly_no;
        if next_ugly_no == next_multiple_of_2 {
            i2 = i2.wrapping_add(1 as libc::c_int as libc::c_uint);
            next_multiple_of_2 =
                (*ugly.as_mut_ptr().offset(i2 as
                                               isize)).wrapping_mul(2 as
                                                                        libc::c_int
                                                                        as
                                                                        libc::c_uint)
        }
        if next_ugly_no == next_multiple_of_3 {
            i3 = i3.wrapping_add(1 as libc::c_int as libc::c_uint);
            next_multiple_of_3 =
                (*ugly.as_mut_ptr().offset(i3 as
                                               isize)).wrapping_mul(3 as
                                                                        libc::c_int
                                                                        as
                                                                        libc::c_uint)
        }
        if next_ugly_no == next_multiple_of_5 {
            i5 = i5.wrapping_add(1 as libc::c_int as libc::c_uint);
            next_multiple_of_5 =
                (*ugly.as_mut_ptr().offset(i5 as
                                               isize)).wrapping_mul(5 as
                                                                        libc::c_int
                                                                        as
                                                                        libc::c_uint)
        }
        i += 1
    }
    return next_ugly_no;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut n: libc::c_uint) -> libc::c_uint {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_int; 10] =
        [27 as libc::c_int, 64 as libc::c_int, 93 as libc::c_int,
         90 as libc::c_int, 85 as libc::c_int, 86 as libc::c_int,
         72 as libc::c_int, 86 as libc::c_int, 32 as libc::c_int,
         1 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr()) {
        if f_filled(param0[i as usize] as libc::c_uint) ==
               f_gold(param0[i as usize] as libc::c_uint) {
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
