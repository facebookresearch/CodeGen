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
pub unsafe extern "C" fn f_gold(mut str: *mut libc::c_char,
                                mut n: libc::c_int) -> libc::c_int {
    let vla = n as usize;
    let vla_0 = n as usize;
    let mut dp: Vec<libc::c_int> = ::std::vec::from_elem(0, vla * vla_0);
    memset(dp.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla * vla_0 * ::std::mem::size_of::<libc::c_int>()) as
               libc::c_ulong);
    let vla_1 = n as usize;
    let vla_2 = n as usize;
    let mut P: Vec<bool> = ::std::vec::from_elem(false, vla_1 * vla_2);
    memset(P.as_mut_ptr() as *mut libc::c_void, 0 as libc::c_int,
           (vla_1 * vla_2 * ::std::mem::size_of::<bool>()) as libc::c_ulong);
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < n {
        *P.as_mut_ptr().offset(i as isize * vla_2 as isize).offset(i as isize)
            = 1 as libc::c_int != 0;
        i += 1
    }
    let mut i_0: libc::c_int = 0 as libc::c_int;
    while i_0 < n - 1 as libc::c_int {
        if *str.offset(i_0 as isize) as libc::c_int ==
               *str.offset((i_0 + 1 as libc::c_int) as isize) as libc::c_int {
            *P.as_mut_ptr().offset(i_0 as isize *
                                       vla_2 as
                                           isize).offset((i_0 +
                                                              1 as
                                                                  libc::c_int)
                                                             as isize) =
                1 as libc::c_int != 0;
            *dp.as_mut_ptr().offset(i_0 as isize *
                                        vla_0 as
                                            isize).offset((i_0 +
                                                               1 as
                                                                   libc::c_int)
                                                              as isize) =
                1 as libc::c_int
        }
        i_0 += 1
    }
    let mut gap: libc::c_int = 2 as libc::c_int;
    while gap < n {
        let mut i_1: libc::c_int = 0 as libc::c_int;
        while i_1 < n - gap {
            let mut j: libc::c_int = gap + i_1;
            if *str.offset(i_1 as isize) as libc::c_int ==
                   *str.offset(j as isize) as libc::c_int &&
                   *P.as_mut_ptr().offset((i_1 + 1 as libc::c_int) as isize *
                                              vla_2 as
                                                  isize).offset((j -
                                                                     1 as
                                                                         libc::c_int)
                                                                    as isize)
                       as libc::c_int != 0 {
                *P.as_mut_ptr().offset(i_1 as isize *
                                           vla_2 as isize).offset(j as isize)
                    = 1 as libc::c_int != 0
            }
            if *P.as_mut_ptr().offset(i_1 as isize *
                                          vla_2 as isize).offset(j as isize)
                   as libc::c_int == 1 as libc::c_int {
                *dp.as_mut_ptr().offset(i_1 as isize *
                                            vla_0 as isize).offset(j as isize)
                    =
                    *dp.as_mut_ptr().offset(i_1 as isize *
                                                vla_0 as
                                                    isize).offset((j -
                                                                       1 as
                                                                           libc::c_int)
                                                                      as
                                                                      isize) +
                        *dp.as_mut_ptr().offset((i_1 + 1 as libc::c_int) as
                                                    isize *
                                                    vla_0 as
                                                        isize).offset(j as
                                                                          isize)
                        + 1 as libc::c_int -
                        *dp.as_mut_ptr().offset((i_1 + 1 as libc::c_int) as
                                                    isize *
                                                    vla_0 as
                                                        isize).offset((j -
                                                                           1
                                                                               as
                                                                               libc::c_int)
                                                                          as
                                                                          isize)
            } else {
                *dp.as_mut_ptr().offset(i_1 as isize *
                                            vla_0 as isize).offset(j as isize)
                    =
                    *dp.as_mut_ptr().offset(i_1 as isize *
                                                vla_0 as
                                                    isize).offset((j -
                                                                       1 as
                                                                           libc::c_int)
                                                                      as
                                                                      isize) +
                        *dp.as_mut_ptr().offset((i_1 + 1 as libc::c_int) as
                                                    isize *
                                                    vla_0 as
                                                        isize).offset(j as
                                                                          isize)
                        -
                        *dp.as_mut_ptr().offset((i_1 + 1 as libc::c_int) as
                                                    isize *
                                                    vla_0 as
                                                        isize).offset((j -
                                                                           1
                                                                               as
                                                                               libc::c_int)
                                                                          as
                                                                          isize)
            }
            i_1 += 1
        }
        gap += 1
    }
    return *dp.as_mut_ptr().offset(0 as libc::c_int as isize *
                                       vla_0 as
                                           isize).offset((n -
                                                              1 as
                                                                  libc::c_int)
                                                             as isize);
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut str: *mut libc::c_char,
                                  mut n: libc::c_int) -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0_0: [libc::c_char; 17] =
        ['E' as i32 as libc::c_char, 'E' as i32 as libc::c_char,
         'J' as i32 as libc::c_char, 'P' as i32 as libc::c_char,
         'T' as i32 as libc::c_char, 'U' as i32 as libc::c_char,
         'X' as i32 as libc::c_char, 'Y' as i32 as libc::c_char,
         'Z' as i32 as libc::c_char, 'e' as i32 as libc::c_char,
         'f' as i32 as libc::c_char, 'h' as i32 as libc::c_char,
         'l' as i32 as libc::c_char, 'm' as i32 as libc::c_char,
         'n' as i32 as libc::c_char, 'o' as i32 as libc::c_char,
         'z' as i32 as libc::c_char];
    let mut param0_1: [libc::c_char; 28] =
        ['8' as i32 as libc::c_char, '7' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '9' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '4' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '6' as i32 as libc::c_char, '8' as i32 as libc::c_char,
         '2' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '8' as i32 as libc::c_char, '3' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '2' as i32 as libc::c_char,
         '8' as i32 as libc::c_char, '6' as i32 as libc::c_char,
         '6' as i32 as libc::c_char, '3' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '7' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '7' as i32 as libc::c_char];
    let mut param0_2: [libc::c_char; 42] =
        ['0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char];
    let mut param0_3: [libc::c_char; 40] =
        ['f' as i32 as libc::c_char, 'E' as i32 as libc::c_char,
         'e' as i32 as libc::c_char, 'z' as i32 as libc::c_char,
         'B' as i32 as libc::c_char, 'o' as i32 as libc::c_char,
         'i' as i32 as libc::c_char, 'v' as i32 as libc::c_char,
         'K' as i32 as libc::c_char, 'u' as i32 as libc::c_char,
         'P' as i32 as libc::c_char, 'C' as i32 as libc::c_char,
         'z' as i32 as libc::c_char, 'f' as i32 as libc::c_char,
         'k' as i32 as libc::c_char, 'J' as i32 as libc::c_char,
         't' as i32 as libc::c_char, 'R' as i32 as libc::c_char,
         't' as i32 as libc::c_char, 'A' as i32 as libc::c_char,
         'f' as i32 as libc::c_char, 'G' as i32 as libc::c_char,
         'D' as i32 as libc::c_char, 'X' as i32 as libc::c_char,
         'H' as i32 as libc::c_char, 'e' as i32 as libc::c_char,
         'p' as i32 as libc::c_char, 'l' as i32 as libc::c_char,
         'l' as i32 as libc::c_char, 'k' as i32 as libc::c_char,
         'Z' as i32 as libc::c_char, 'Y' as i32 as libc::c_char,
         'u' as i32 as libc::c_char, 'g' as i32 as libc::c_char,
         'H' as i32 as libc::c_char, 'C' as i32 as libc::c_char,
         'f' as i32 as libc::c_char, 'J' as i32 as libc::c_char,
         'H' as i32 as libc::c_char, 'W' as i32 as libc::c_char];
    let mut param0_4: [libc::c_char; 37] =
        ['0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '2' as i32 as libc::c_char,
         '2' as i32 as libc::c_char, '2' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '3' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '3' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '4' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '4' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '4' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '6' as i32 as libc::c_char,
         '6' as i32 as libc::c_char, '7' as i32 as libc::c_char,
         '7' as i32 as libc::c_char, '9' as i32 as libc::c_char,
         '9' as i32 as libc::c_char, '9' as i32 as libc::c_char,
         '9' as i32 as libc::c_char, '9' as i32 as libc::c_char,
         '9' as i32 as libc::c_char];
    let mut param0_5: [libc::c_char; 46] =
        ['1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char];
    let mut param0_6: [libc::c_char; 13] =
        ['C' as i32 as libc::c_char, 'C' as i32 as libc::c_char,
         'D' as i32 as libc::c_char, 'F' as i32 as libc::c_char,
         'L' as i32 as libc::c_char, 'M' as i32 as libc::c_char,
         'P' as i32 as libc::c_char, 'X' as i32 as libc::c_char,
         'a' as i32 as libc::c_char, 'f' as i32 as libc::c_char,
         'i' as i32 as libc::c_char, 'j' as i32 as libc::c_char,
         'w' as i32 as libc::c_char];
    let mut param0_7: [libc::c_char; 21] =
        ['7' as i32 as libc::c_char, '9' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '2' as i32 as libc::c_char,
         '8' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '7' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '9' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '5' as i32 as libc::c_char, '4' as i32 as libc::c_char,
         '8' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '9' as i32 as libc::c_char, '5' as i32 as libc::c_char,
         '3' as i32 as libc::c_char, '2' as i32 as libc::c_char,
         '4' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '2' as i32 as libc::c_char];
    let mut param0_8: [libc::c_char; 44] =
        ['0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '0' as i32 as libc::c_char,
         '0' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char,
         '1' as i32 as libc::c_char, '1' as i32 as libc::c_char];
    let mut param0_9: [libc::c_char; 4] =
        ['m' as i32 as libc::c_char, 'X' as i32 as libc::c_char,
         'N' as i32 as libc::c_char, 'M' as i32 as libc::c_char];
    let mut param0: [*mut libc::c_char; 10] =
        [param0_0.as_mut_ptr(), param0_1.as_mut_ptr(), param0_2.as_mut_ptr(),
         param0_3.as_mut_ptr(), param0_4.as_mut_ptr(), param0_5.as_mut_ptr(),
         param0_6.as_mut_ptr(), param0_7.as_mut_ptr(), param0_8.as_mut_ptr(),
         param0_9.as_mut_ptr()];
    let mut param1: [libc::c_int; 10] =
        [11 as libc::c_int, 27 as libc::c_int, 23 as libc::c_int,
         27 as libc::c_int, 35 as libc::c_int, 43 as libc::c_int,
         9 as libc::c_int, 16 as libc::c_int, 32 as libc::c_int,
         3 as libc::c_int];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if f_filled(param0[i as usize], param1[i as usize]) ==
               f_gold(param0[i as usize], param1[i as usize]) {
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
