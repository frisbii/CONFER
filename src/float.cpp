#include <stdio.h>
#include <fstream>

#include "ap_int.h"

#define VIVADO_BACKEND
#include "hint.hpp"
#include "ieeefloats/ieeetype.hpp"
#include "ieeefloats/ieee_adder.hpp"
#include "ieeefloats/ieee_multiplier.hpp"

#include "params.hpp"

#define WE WIDTH/2
#define WF WIDTH-WE-1
    
ap_uint<WIDTH> compute
(
    IEEENumber<WE, WF, hint::VivadoWrapper> in1,
    IEEENumber<WE, WF, hint::VivadoWrapper> in2
)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
    #ifdef ADD
	    auto add = ieee_add_sub_impl(in1, in2);
        return add.unravel();
    #else
	    auto mul = ieee_product(in1, in2);
        return mul.unravel();
    #endif
}