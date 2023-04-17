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
pub unsafe extern "C" fn f_gold(mut x1: libc::c_float, mut y1: libc::c_float,
                                mut x2: libc::c_float, mut y2: libc::c_float)
 -> libc::c_float {
    return (y2 - y1) / (x2 - x1);
}
#[no_mangle]
pub unsafe extern "C" fn f_filled(mut x1: libc::c_float,
                                  mut y1: libc::c_float,
                                  mut x2: libc::c_float,
                                  mut y2: libc::c_float) -> libc::c_float {
    panic!("Reached end of non-void function without returning");
}
unsafe fn main_0() -> libc::c_int {
    let mut n_success: libc::c_int = 0 as libc::c_int;
    let mut param0: [libc::c_float; 10] =
        [236.27324548309292f32, -9201.144918204123f32, 3480.4716834445326f32,
         -6915.538971485092f32, 8887.97173657486f32, -3785.5177159369946f32,
         3037.6696554256832f32, -7925.458496016523f32, 1404.2919985268031f32,
         -4748.744241168378f32];
    let mut param1: [libc::c_float; 10] =
        [5792.493225762838f32, -2716.3347716140406f32, 3577.9608612055613f32,
         -4113.601103381095f32, 1678.4080012662428f32, -3084.67461899163f32,
         4432.445827549f32, -3350.27411882042f32, 8971.636233373416f32,
         -675.557388148954f32];
    let mut param2: [libc::c_float; 10] =
        [7177.837879115863f32, -5161.142121227645f32, 8611.515262945342f32,
         -748.3462104020822f32, 8709.574949883017f32, -7415.76208254121f32,
         8387.304165588026f32, -5619.767086756504f32, 3039.112051378511f32,
         -5998.241086029875f32];
    let mut param3: [libc::c_float; 10] =
        [1289.5700425822731f32, -3205.784279961129f32, 6744.864707668983f32,
         -9245.271700539257f32, 8548.492675510739f32, -887.5389305564152f32,
         611.3373507518394f32, -1185.7423219907591f32, 1947.6756252708972f32,
         -4236.658178504375f32];
    let mut i: libc::c_int = 0 as libc::c_int;
    while i < len(param0.as_mut_ptr() as *mut libc::c_int) {
        if (abs((1 as libc::c_int as libc::c_double -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize], param1[i as usize],
                                     param2[i as usize], param3[i as usize])
                                  as libc::c_int) as libc::c_double) /
                         (abs(f_filled(param0[i as usize], param1[i as usize],
                                       param2[i as usize], param3[i as usize])
                                  as libc::c_int) as libc::c_double +
                              0.0000001f64)) as libc::c_int) as libc::c_float)
               < 0.001f32 {
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
