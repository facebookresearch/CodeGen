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
    fn memset(_: *mut libc::c_void, _: libc::c_int, _: libc::c_ulong)
     -> *mut libc::c_void;
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
pub unsafe extern "C" fn f_gold(mut N: libc::c_int, mut insert: libc::c_int,
                                mut remove: libc::c_int,
                                mut copy: libc::c_int) -> libc::c_int {
    if N == 0 as libc::c_int { return 0 as libc::c_int }
    if N == 1 as libc::c_int { return insert }
    let vla = (N + 1 as libc::c_int) as usize;
    let mut dp: Vec<libc::c_int> = ::std::vec::from_elem(0, vla);
    memset(dp.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla * ::std::mem::size_of::<libc::c_int>()) as libc::c_ulong);
    let mut i: libc::c_int = 1 as libc::c_int;
    while i <= N {
        if i % 2 as libc::c_int == 0 as libc::c_int {
            *dp.as_mut_ptr().offset(i as isize) =
                min(*dp.as_mut_ptr().offset((i - 1 as libc::c_int) as isize) +
                        insert,
                    *dp.as_mut_ptr().offset((i / 2 as libc::c_int) as isize) +
                        copy)
        } else {
            *dp.as_mut_ptr().offset(i as isize) =
                min(*dp.as_mut_ptr().offset((i - 1 as libc::c_int) as isize) +
                        insert,
                    *dp.as_mut_ptr().offset(((i + 1 as libc::c_int) /
                                                 2 as libc::c_int) as isize) +
                        copy + remove)
        }
        i += 1
    }
    return *dp.as_mut_ptr().offset(N as isize);
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut N: libc::c_int, mut insert: libc::c_int,
                                  mut remove: libc::c_int,
                                  mut copy: libc::c_int) -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_int; 10] =
        [59 as libc::c_int, 66 as libc::c_int, 98 as libc::c_int,
         63 as libc::c_int, 99 as libc::c_int, 45 as libc::c_int,
         60 as libc::c_int, 11 as libc::c_int, 96 as libc::c_int,
         54 as libc::c_int];
    let mut param1: [libc::c_int; 10] =
        [75 as libc::c_int, 68 as libc::c_int, 55 as libc::c_int,
         4 as libc::c_int, 37 as libc::c_int, 28 as libc::c_int,
         53 as libc::c_int, 96 as libc::c_int, 95 as libc::c_int,
         6 as libc::c_int];
    let mut param2: [libc::c_int; 10] =
        [12 as libc::c_int, 32 as libc::c_int, 69 as libc::c_int,
         41 as libc::c_int, 98 as libc::c_int, 59 as libc::c_int,
         40 as libc::c_int, 50 as libc::c_int, 48 as libc::c_int,
         50 as libc::c_int];
    let mut param3: [libc::c_int; 10] =
        [45 as libc::c_int, 41 as libc::c_int, 5 as libc::c_int,
         12 as libc::c_int, 55 as libc::c_int, 7 as libc::c_int,
         52 as libc::c_int, 50 as libc::c_int, 84 as libc::c_int,
         82 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr()) {
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
           len(param0.as_mut_ptr()));
    return 0 as libc::c_int;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
