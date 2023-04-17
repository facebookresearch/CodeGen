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
pub unsafe extern "C" fn f_gold(mut n: libc::c_int) -> libc::c_longlong {
    let vla = 10 as libc::c_int as usize;
    let vla_0 = (n + 1 as libc::c_int) as usize;
    let mut dp: Vec<libc::c_longlong> = ::std::vec::from_elem(0, vla * vla_0);
    memset(dp.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla * vla_0 * ::std::mem::size_of::<libc::c_longlong>()) as
               libc::c_ulong);
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < 10 as libc::c_int {
        *dp.as_mut_ptr().offset(i as isize *
                                    vla_0 as
                                        isize).offset(1 as libc::c_int as
                                                          isize) =
            1 as libc::c_int as libc::c_longlong;
        i += 1
    }
    let mut digit: libc::c_int = 0 as libc::c_int;
    while digit <= 9 as libc::c_int {
        let mut len_0: libc::c_int = 2 as libc::c_int;
        while len_0 <= n {
            let mut x: libc::c_int = 0 as libc::c_int;
            while x <= digit {
                *dp.as_mut_ptr().offset(digit as isize *
                                            vla_0 as
                                                isize).offset(len_0 as isize)
                    +=
                    *dp.as_mut_ptr().offset(x as isize *
                                                vla_0 as
                                                    isize).offset((len_0 -
                                                                       1 as
                                                                           libc::c_int)
                                                                      as
                                                                      isize);
                x += 1
            }
            len_0 += 1
        }
        digit += 1
    }
    let mut count: libc::c_longlong = 0 as libc::c_int as libc::c_longlong;
    let mut i_0: libc::c_int = 0 as libc::c_int;
    while i_0 < 10 as libc::c_int {
        count +=
            *dp.as_mut_ptr().offset(i_0 as isize *
                                        vla_0 as isize).offset(n as isize);
        i_0 += 1
    }
    return count;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut n: libc::c_int) -> libc::c_longlong {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_int; 10] =
        [21 as libc::c_int, 40 as libc::c_int, 83 as libc::c_int,
         93 as libc::c_int, 43 as libc::c_int, 98 as libc::c_int,
         35 as libc::c_int, 86 as libc::c_int, 76 as libc::c_int,
         88 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr()) {
        if f_filled(param0[i as usize]) == f_gold(param0[i as usize]) {
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
