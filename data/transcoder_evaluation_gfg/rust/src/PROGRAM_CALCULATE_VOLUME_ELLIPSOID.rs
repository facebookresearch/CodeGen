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
pub unsafe extern "C" fn f_gold(mut r1: libc::c_float, mut r2: libc::c_float,
                                mut r3: libc::c_float) -> libc::c_float {
    let mut pi: libc::c_float = 3.14f64 as libc::c_float;
    return (1.33f64 * pi as libc::c_double * r1 as libc::c_double *
                r2 as libc::c_double * r3 as libc::c_double) as libc::c_float;
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut r1: libc::c_float,
                                  mut r2: libc::c_float,
                                  mut r3: libc::c_float) -> libc::c_float {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_float; 10] =
        [3287.4842316041018f32, -3707.427510963942f32, 8980.643174783816f32,
         -2698.0187368852694f32, 8627.156664162168f32, -7316.329924623669f32,
         7857.3846206400485f32, -6502.657905007728f32, 4468.400513325576f32,
         -7231.864791620428f32];
    let mut param1: [libc::c_float; 10] =
        [4503.332888443404f32, -6671.335781753231f32, 3584.781688607942f32,
         -1004.7289573934537f32, 9572.27618966978f32, -6591.043206581106f32,
         3671.761679299217f32, -1412.2240121470609f32, 2272.1999139470304f32,
         -8036.087711033032f32];
    let mut param2: [libc::c_float; 10] =
        [8590.24729914204f32, -2780.4954870801926f32, 2818.469507143102f32,
         -9602.530725071243f32, 4783.930377855004f32, -9760.465488363216f32,
         2534.5825334137794f32, -6135.238350044512f32, 4753.075799180736f32,
         -6456.263512521035f32];
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
