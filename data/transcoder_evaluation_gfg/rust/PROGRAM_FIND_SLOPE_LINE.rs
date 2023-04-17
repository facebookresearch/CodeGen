#![feature(main)]
// Copyright (c) 2019-present, Facebook, Inc.
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.
//

#[no_mangle]
pub unsafe fn abs(mut x: i32)
 -> i32 {
    return x.abs();
}

#[no_mangle]
pub unsafe fn min(mut x: i32, mut y: i32)
 -> i32 {
    return if x < y { x } else { y };
}
#[no_mangle]
pub unsafe fn max(mut x: i32, mut y: i32)
 -> i32 {
    return if x > y { x } else { y };
}

pub unsafe fn f_gold(mut x1: f32, mut y1: f32,
                                mut x2: f32, mut y2: f32)
 -> f32 {
    return (y2 - y1) / (x2 - x1);
}
//TOFILL
unsafe fn main_0() -> i32 {
    let mut n_success: i32 = 0 as i32;
    let mut param0: [f32; 10] =
        [236.27324548309292f32, -9201.144918204123f32, 3480.4716834445326f32,
         -6915.538971485092f32, 8887.97173657486f32, -3785.5177159369946f32,
         3037.6696554256832f32, -7925.458496016523f32, 1404.2919985268031f32,
         -4748.744241168378f32];
    let mut param1: [f32; 10] =
        [5792.493225762838f32, -2716.3347716140406f32, 3577.9608612055613f32,
         -4113.601103381095f32, 1678.4080012662428f32, -3084.67461899163f32,
         4432.445827549f32, -3350.27411882042f32, 8971.636233373416f32,
         -675.557388148954f32];
    let mut param2: [f32; 10] =
        [7177.837879115863f32, -5161.142121227645f32, 8611.515262945342f32,
         -748.3462104020822f32, 8709.574949883017f32, -7415.76208254121f32,
         8387.304165588026f32, -5619.767086756504f32, 3039.112051378511f32,
         -5998.241086029875f32];
    let mut param3: [f32; 10] =
        [1289.5700425822731f32, -3205.784279961129f32, 6744.864707668983f32,
         -9245.271700539257f32, 8548.492675510739f32, -887.5389305564152f32,
         611.3373507518394f32, -1185.7423219907591f32, 1947.6756252708972f32,
         -4236.658178504375f32];
    let mut i: i32 = 0 as i32;
    while i < param0.len() as i32 {
        if (abs((1 as i32 as f64 -
                     (0.0000001f64 +
                          abs(f_gold(param0[i as usize], param1[i as usize],
                                     param2[i as usize], param3[i as usize])
                                  as i32) as f64) /
                         (abs(f_filled(param0[i as usize], param1[i as usize],
                                       param2[i as usize], param3[i as usize])
                                  as i32) as f64 +
                              0.0000001f64)) as i32) as f32)
               < 0.001f32 {
            n_success += 1 as i32
        }
        i += 1
    }
    println!("{} {} {} {} {}", "#Results:", " ", n_success, ", ", param0.len() as i32);
    return 0 as i32;
}
#[main]
pub fn main() { unsafe { ::std::process::exit(main_0() as i32) } }
