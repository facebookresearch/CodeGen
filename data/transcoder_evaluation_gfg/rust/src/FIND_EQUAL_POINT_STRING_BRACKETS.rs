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
    fn strlen(_: *const libc::c_char) -> libc::c_ulong;
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
pub unsafe extern "C" fn f_gold(mut str: *mut libc::c_char) -> libc::c_int {
    let mut len_0: libc::c_int =
        strlen(str as *const libc::c_char) as libc::c_int;
    let vla = (len_0 + 1 as libc::c_int) as usize;
    let mut open: Vec<libc::c_int> = ::std::vec::from_elem(0, vla);
    let vla_0 = (len_0 + 1 as libc::c_int) as usize;
    let mut close: Vec<libc::c_int> = ::std::vec::from_elem(0, vla_0);
    let mut index: libc::c_int = -(1 as libc::c_int);
    memset(open.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla * ::std::mem::size_of::<libc::c_int>()) as libc::c_ulong);
    memset(close.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla_0 * ::std::mem::size_of::<libc::c_int>()) as libc::c_ulong);
    *open.as_mut_ptr().offset(0 as libc::c_int as isize) = 0 as libc::c_int;
    *close.as_mut_ptr().offset(len_0 as isize) = 0 as libc::c_int;
    if *str.offset(0 as libc::c_int as isize) as libc::c_int == '(' as i32 {
        *open.as_mut_ptr().offset(1 as libc::c_int as isize) =
            1 as libc::c_int
    }
    if *str.offset((len_0 - 1 as libc::c_int) as isize) as libc::c_int ==
           ')' as i32 {
        *close.as_mut_ptr().offset((len_0 - 1 as libc::c_int) as isize) =
            1 as libc::c_int
    }
    let mut i: libc::c_int = 1 as libc::c_int;
    while i < len_0 {
        if *str.offset(i as isize) as libc::c_int == '(' as i32 {
            *open.as_mut_ptr().offset((i + 1 as libc::c_int) as isize) =
                *open.as_mut_ptr().offset(i as isize) + 1 as libc::c_int
        } else {
            *open.as_mut_ptr().offset((i + 1 as libc::c_int) as isize) =
                *open.as_mut_ptr().offset(i as isize)
        }
        i += 1
    }
    let mut i_0: libc::c_int = len_0 - 2 as libc::c_int;
    while i_0 >= 0 as libc::c_int {
        if *str.offset(i_0 as isize) as libc::c_int == ')' as i32 {
            *close.as_mut_ptr().offset(i_0 as isize) =
                *close.as_mut_ptr().offset((i_0 + 1 as libc::c_int) as isize)
                    + 1 as libc::c_int
        } else {
            *close.as_mut_ptr().offset(i_0 as isize) =
                *close.as_mut_ptr().offset((i_0 + 1 as libc::c_int) as isize)
        }
        i_0 -= 1
    }
    if *open.as_mut_ptr().offset(len_0 as isize) == 0 as libc::c_int {
        return len_0
    }
    if *close.as_mut_ptr().offset(0 as libc::c_int as isize) ==
           0 as libc::c_int {
        return 0 as libc::c_int
    }
    let mut i_1: libc::c_int = 0 as libc::c_int;
    while i_1 <= len_0 {
        if *open.as_mut_ptr().offset(i_1 as isize) ==
               *close.as_mut_ptr().offset(i_1 as isize) {
            index = i_1
        }
        i_1 += 1
    }
    return index;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut str: *mut libc::c_char) -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [[libc::c_char; 100]; 10] =
        [*::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"(())))(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"))\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"((\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"))(()(()()(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b")((()(()\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"))(()\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"()))\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"()\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"1100110\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
         *::std::mem::transmute::<&[u8; 100],
                                  &mut [libc::c_char; 100]>(b"dhfSnebD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if f_filled(param0[i as usize].as_mut_ptr()) ==
               f_gold(param0[i as usize].as_mut_ptr()) {
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
