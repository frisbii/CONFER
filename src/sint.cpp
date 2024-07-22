#include <stdio.h>
#include <fstream>

#include "ap_int.h"
#include "params.hpp"

void compute
(
    ap_int<WIDTH> in0,
    ap_int<WIDTH> in1,
    #ifdef ADD
        ap_int<WIDTH> *out
    #else
        ap_int<WIDTH> *out
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
