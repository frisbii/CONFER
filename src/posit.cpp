#include <stdio.h>
#include <fstream>

#include "ap_int.h"

#define VIVADO_BACKEND
#include "hint.hpp"
#include "posit/posit_dim.hpp"

#include "params.hpp"

#if WIDTH >= 64
    #define WES 3
#elif WIDTH >= 32
    #define WES 2
#elif WIDTH >= 16
    #define WES 1
#else  
    #define WES 0
#endif

ap_uint<WIDTH> compute
(
    PositEncoding<WIDTH, WES, hint::VivadoWrapper> in1,
    PositEncoding<WIDTH, WES, hint::VivadoWrapper> in2
)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
    #ifdef ADD
	    auto add = in1 + in2;
        return add.unravel();
    #else
	    auto mul = in1 * in2;
        return mul.unravel();
    #endif
}
