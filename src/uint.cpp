#include <stdio.h>
#include <fstream>

#include "ap_int.h"
#include "params.hpp"

void compute
(
    ap_uint<WIDTH> in0,
    ap_uint<WIDTH> in1,
    #ifdef ADD
        ap_uint<WIDTH> *out
    #else
        ap_uint<WIDTH> *out
    #endif
)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
    #ifdef ADD
	    *out = in0 + in1;
    #else
	    *out = in0 * in1;
    #endif
}
