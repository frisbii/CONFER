#include <stdio.h>
#include <fstream>

#include "ap_int.h"
#include "params.hpp"

void compute
(
    ap_ufixed<WIDTH, INT_BITS> in0,
    ap_ufixed<WIDTH, INT_BITS> in1,
    #ifdef ADD
        ap_ufixed<WIDTH, INT_BITS> *out
    #else
        ap_ufixed<WIDTH, INT_BITS> *out
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
