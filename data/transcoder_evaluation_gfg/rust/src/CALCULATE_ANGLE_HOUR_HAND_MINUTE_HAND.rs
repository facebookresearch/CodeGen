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
pub unsafe extern "C" fn f_gold(mut h: libc::c_double, mut m: libc::c_double)
 -> libc::c_int {
    if h < 0 as libc::c_int as libc::c_double ||
           m < 0 as libc::c_int as libc::c_double ||
           h > 12 as libc::c_int as libc::c_double ||
           m > 60 as libc::c_int as libc::c_double {
        printf(b"Wrong input\x00" as *const u8 as *const libc::c_char);
    }
    if h == 12 as libc::c_int as libc::c_double {
        h = 0 as libc::c_int as libc::c_double
    }
    if m == 60 as libc::c_int as libc::c_double {
        m = 0 as libc::c_int as libc::c_double
    }
    let mut hour_angle: libc::c_int =
        (0.5f64 * (h * 60 as libc::c_int as libc::c_double + m)) as
            libc::c_int;
    let mut minute_angle: libc::c_int =
        (6 as libc::c_int as libc::c_double * m) as libc::c_int;
    let mut angle: libc::c_int = abs(hour_angle - minute_angle);
    angle = min(360 as libc::c_int - angle, angle);
    return angle;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut h: libc::c_double,
                                  mut m: libc::c_double) -> libc::c_int {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_double; 10] =
        [7322.337365895532f64, -0.5025472034247969f64, 8735.336068205026f64,
         -5478.862697905712f64, 8264.126919165505f64, -9671.311773842834f64,
         9995.328351000411f64, -5274.574323066984f64, 1310.8711644223736f64,
         -2829.678131972794f64];
    let mut param1: [libc::c_double; 10] =
        [6996.326968156217f64, -2910.070017192333f64, 1910.3752934680874f64,
         -9470.18148108585f64, 7058.937313484608f64, -3867.070379361206f64,
         2145.339179488316f64, -3583.7503371694124f64, 5214.059687285893f64,
         -9371.556600288217f64];
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
