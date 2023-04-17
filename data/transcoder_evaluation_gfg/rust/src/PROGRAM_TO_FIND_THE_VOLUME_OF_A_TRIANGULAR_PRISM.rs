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
pub unsafe extern "C" fn f_gold(mut l: libc::c_float, mut b: libc::c_float,
                                mut h: libc::c_float) -> libc::c_float {
    let mut volume: libc::c_float =
        l * b * h / 2 as libc::c_int as libc::c_float;
    return volume;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut l: libc::c_float, mut b: libc::c_float,
                                  mut h: libc::c_float) -> libc::c_float {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_float; 10] =
        [8448.900678262902f32, -1849.728957491451f32, 412.667844022232f32,
         -5954.835911765373f32, 8437.913444665008f32, -7183.181663518317f32,
         2340.7905920227954f32, -7281.157547371143f32, 471.3930826982504f32,
         -7550.426360065503f32];
    let mut param1: [libc::c_float; 10] =
        [8135.461799983198f32, -4240.89241631363f32, 9798.083992381831f32,
         -661.8872499003203f32, 8182.675681595904f32, -6846.746446198541f32,
         5479.00956987109f32, -615.8705455524116f32, 1357.3753126091392f32,
         -2693.2262997056355f32];
    let mut param2: [libc::c_float; 10] =
        [6577.239053611328f32, -9953.518310747193f32, 1449.9204200270522f32,
         -8049.6051526695055f32, 9863.296545513396f32, -971.2199894221352f32,
         7073.449591910562f32, -3343.0245192607968f32, 1907.815700915636f32,
         -9110.64755244532f32];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if (abs((1 as libc::c_int as libc::c_double -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize], param1[i as usize],
                                     param2[i as usize]) as libc::c_int) as
                              libc::c_double) /
                         (abs(f_filled(param0[i as usize], param1[i as usize],
                                       param2[i as usize]) as libc::c_int) as
                              libc::c_double + 0.0000001f64)) as libc::c_int)
                as libc::c_float) < 0.001f32 {
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
